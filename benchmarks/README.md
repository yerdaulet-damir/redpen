# Redpen behavior benchmark

The benchmark asks whether Redpen changes behavior, not whether its prompt
contains attractive rules.

It generates each case twice: once with a generic copywriter system prompt and
once with Redpen. A separate judge compares anonymous candidates in both
orders. Order-swapped disagreement is reported as unstable instead of silently
counted as a win.

The rubric measures recognition, pull, trust, emotional movement, ownability,
and cadence. Invented facts, fake customer voice, unclear meaning, copied
structures, and emotion named instead of caused are hard failures.

```bash
python -m unittest benchmarks/test_eval.py

# Claude subscription / OAuth login:
REDPEN_PROVIDER=claude-cli python benchmarks/eval.py --selftest
REDPEN_PROVIDER=claude-cli python benchmarks/eval.py --run
REDPEN_PROVIDER=claude-cli python benchmarks/eval.py --run --case screen-recorder

# Or direct API:
export ANTHROPIC_API_KEY=...
python benchmarks/eval.py --selftest
python benchmarks/eval.py --run
```

`--selftest` first checks that the judge consistently prefers "Like
console.log, but it arrives on your phone" over generic alert-platform copy.
If that pair does not survive the order swap, the benchmark refuses to treat
the judge as trustworthy.

`results.json` is generated output. It records the model, provider, UTC run
date, commit, skill, harness and case hashes, plus the raw mirrored verdicts.
Keep that metadata intact when publishing or comparing a run.

The verification run on 2026-08-02 with Claude Sonnet 4.6 produced six Redpen
wins in six stable mirrored cases. Treat that as a directional regression
baseline, not a permanent product score: model judges are noisy, which is why
future disagreement remains visible instead of becoming a win.
