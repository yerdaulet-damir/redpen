#!/usr/bin/env python3
"""Blind baseline-vs-Redpen preference evaluation.

Uses only the Python standard library. Set ANTHROPIC_API_KEY, then run:

    python benchmarks/eval.py --selftest
    python benchmarks/eval.py --run

The judge sees candidates in both orders. A case counts as a Redpen win only
when the mirrored verdicts agree and no hard gate fails.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "benchmarks" / "cases.json"
SKILL = ROOT / "skills" / "redpen" / "SKILL.md"
MODEL = os.environ.get("REDPEN_MODEL", "claude-sonnet-4-6")
PROVIDER = os.environ.get("REDPEN_PROVIDER", "api")

BASE_SYSTEM = """You are a capable marketing copywriter. Write clear, concise,
persuasive copy for the requested surface. Return only the finished copy."""

JUDGE_SYSTEM = """You are evaluating copy quality, not politeness or effort.
Compare two anonymous candidates for the supplied brief and facts. Judge what
the words actually cause in the target reader. Evaluate only the finished copy
at the start of each candidate. Ignore diagnostic notes, reader-moment labels,
scoring explanations, runner-ups, and prose after a horizontal rule. Those are
not part of the requested marketing surface and must never count as copy or as
a hard failure.

Score each 0-3 on: recognition, pull, trust, emotional_movement, ownability,
cadence. Hard failures: invented/upgraded fact, unclear meaning, fake customer
voice, generic copy that a competitor can sign, or emotion named instead of
caused. Prefer concrete, believable human writing over polished marketing
wallpaper. Quote each candidate's load-bearing or failing fragment.

Return JSON only:
{"winner":"A|B|tie","a":{"scores":{"recognition":0,"pull":0,"trust":0,
"emotional_movement":0,"ownability":0,"cadence":0},"hard_failures":[],
"fragment":"","defect":""},"b":{"scores":{"recognition":0,"pull":0,
"trust":0,"emotional_movement":0,"ownability":0,"cadence":0},
"hard_failures":[],"fragment":"","defect":""},"reason":"one concrete line"}
"""


def api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        raise SystemExit("Set ANTHROPIC_API_KEY before running model evals.")
    return key


def api_call(system: str, user: str, max_tokens: int, temperature: float) -> str:
    body = json.dumps(
        {
            "model": MODEL,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }
    ).encode()
    request = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "x-api-key": api_key(),
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                result = json.loads(response.read())
            return result["content"][0]["text"]
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("unreachable")


def cli_call(system: str, user: str) -> str:
    executable = shutil.which("claude")
    if not executable:
        raise SystemExit("REDPEN_PROVIDER=claude-cli requires the claude executable.")
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8") as prompt_file:
        prompt_file.write(system)
        prompt_file.flush()
        result = subprocess.run(
            [
                executable,
                "-p",
                "--safe-mode",
                "--no-session-persistence",
                "--model",
                MODEL,
                "--tools",
                "",
                "--system-prompt-file",
                prompt_file.name,
                user,
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=180,
        )
    return result.stdout.strip()


def call(system: str, user: str, max_tokens: int = 1400, temperature: float = 0) -> str:
    if PROVIDER == "claude-cli":
        return cli_call(system, user)
    if PROVIDER == "api":
        return api_call(system, user, max_tokens, temperature)
    raise SystemExit("REDPEN_PROVIDER must be api or claude-cli.")


def task(case: dict) -> str:
    truths = "\n".join(f"- {item}" for item in case["truth"])
    return (
        f"SURFACE: {case['surface']}\nBRIEF: {case['brief']}\n"
        f"TARGET READER: {case['reader']}\nDESIRED ACTION: {case['desired_action']}\n"
        f"KNOWN TRUTH (do not add facts):\n{truths}"
    )


def parse_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError(f"No JSON object in judge output: {text[:160]}")
    return json.loads(match.group(0))


def eligible_vote(report: dict, labels: dict[str, str]) -> str:
    """Return the eligible winner after hard failures disqualify candidates."""
    failed = {
        labels[key.upper()]
        for key in ("a", "b")
        if report.get(key, {}).get("hard_failures")
    }
    eligible = {"baseline", "redpen"} - failed
    if not eligible:
        return "invalid"
    if len(eligible) == 1:
        return eligible.pop()
    return labels.get(report.get("winner"), "invalid")


def mirrored_winner(first: dict, second: dict) -> str:
    """Return an eligible verdict after swapping candidate order."""
    first_vote = eligible_vote(first, {"A": "baseline", "B": "redpen", "tie": "tie"})
    second_vote = eligible_vote(second, {"A": "redpen", "B": "baseline", "tie": "tie"})
    if first_vote == second_vote:
        return first_vote
    return "unstable"


def run_metadata(skill: str) -> dict:
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        commit = "unknown"
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "commit": commit,
        "skill_sha256": hashlib.sha256(skill.encode()).hexdigest(),
        "harness_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "cases_sha256": hashlib.sha256(CASES.read_bytes()).hexdigest(),
        "model": MODEL,
        "provider": PROVIDER,
    }


def judge(case: dict, baseline: str, redpen: str) -> tuple[dict, dict, str]:
    prompt = task(case)
    first = parse_json(call(JUDGE_SYSTEM, f"{prompt}\n\nA:\n{baseline}\n\nB:\n{redpen}"))
    second = parse_json(call(JUDGE_SYSTEM, f"{prompt}\n\nA:\n{redpen}\n\nB:\n{baseline}"))
    return first, second, mirrored_winner(first, second)


def selftest() -> int:
    case = {
        "surface": "landing-page hero",
        "brief": "Write a headline for an app that sends a phone alert when a background job reaches a marked line.",
        "reader": "A developer away from the laptop waiting for a job to finish.",
        "desired_action": "Install it.",
        "truth": ["One function call sends a Telegram message to the developer's phone."],
    }
    wallpaper = "Powerful, seamless alerts that empower developers to stay informed anywhere."
    specific = "Like console.log, but it arrives on your phone."
    first, second, winner = judge(case, wallpaper, specific)
    print(json.dumps({"winner": winner, "forward": first, "reversed": second}, indent=2))
    if winner != "redpen":
        print("Judge self-test failed; do not trust a benchmark run.")
        return 1
    print("Judge self-test passed.")
    return 0


def run(case_id: str | None = None) -> int:
    if selftest():
        return 1
    skill = SKILL.read_text(encoding="utf-8")
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    if case_id:
        cases = [case for case in cases if case["id"] == case_id]
        if not cases:
            raise SystemExit(f"Unknown case: {case_id}")
    results = []
    for case in cases:
        prompt = task(case)
        baseline = call(BASE_SYSTEM, prompt, temperature=0.7)
        redpen = call(skill, prompt, temperature=0.7)
        first, second, winner = judge(case, baseline, redpen)
        record = {
            "id": case["id"],
            "winner": winner,
            "baseline": baseline,
            "redpen": redpen,
            "forward": first,
            "reversed": second,
        }
        results.append(record)
        print(f"{case['id']}: {winner}", flush=True)
    output = ROOT / "benchmarks" / "results.json"
    output.write_text(
        json.dumps({**run_metadata(skill), "results": results}, indent=2),
        encoding="utf-8",
    )
    wins = sum(item["winner"] == "redpen" for item in results)
    stable = sum(item["winner"] in {"redpen", "baseline", "tie"} for item in results)
    print(f"Redpen wins: {wins}/{len(results)}; stable mirrored verdicts: {stable}/{len(results)}")
    print(f"Wrote {output}")
    return 0 if wins > len(results) / 2 else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--case", help="run one case id instead of the full matrix")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if args.run:
        return run(args.case)
    parser.error("choose --selftest or --run")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
