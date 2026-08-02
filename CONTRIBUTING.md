# Contributing to Redpen

Redpen is an open attempt to give AI agents editorial taste — not by making
them imitate a quirky person, but by teaching them to find product truth,
reader recognition, tension, proof, and language worth keeping.

We want contributors with different industries, cultures, rhythms, and kinds
of taste. You do not need to be a professional copywriter. You do need to show
why the line works beyond "it sounds better."

## What belongs here

- **Real briefs** with enough product truth to write without invention.
- **Reader moments** drawn from an actual task, frustration, resistance, or
  decision — not a demographic persona.
- **Before/after examples** where the rewrite changes the argument or emotional
  movement, not merely the adjectives.
- **Benchmark cases** that expose generic, bloodless, copied, or over-polished
  model behavior.
- **Editorial methods** that can be explained, challenged, and tested.
- **Agent adapters** that preserve the same behavior in another tool.

Anonymized work is welcome. Remove private data, keep the concrete facts that
made the editorial decision possible, and label supplied facts as unverified.

## What does not belong

- Giant lists of words an AI is never allowed to use.
- Headline formulas presented as substitutes for understanding the product.
- Fake customer quotes, metrics, urgency, vulnerability, slang, or profanity.
- "Humanized" copy made human only through typos, fragments, and casual tone.
- Three rewrites that make the same argument with different nouns.
- A preferred output without the brief, evidence, or editorial reason.

The goal is not to hide that AI helped. The goal is to make the work specific,
truthful, attractive, and alive enough that a person would choose to read the
next line.

## Contribute an example

Add a Markdown file under `examples/` with this compact structure:

1. **Surface** — where the copy will appear and what it must do.
2. **Truth ledger** — observed, provided, inferred, and unknown.
3. **Reader moment** — scene, inner sentence, pressure, resistance, after-state.
4. **Original** — the line or draft being replaced.
5. **Three territories** — scene, fact/contrast, mechanism/identity.
6. **Preference result** — winning fragment and the named defect it beat.
7. **Final copy** — the smallest complete unit as it would actually appear.

Do not reverse-engineer the explanation after choosing a clever line. The
ledger and reader moment should make the final copy feel earned.

## Contribute a benchmark case

Benchmark briefs must be self-contained, contain no private information, and
make invented proof a hard failure. A useful case creates a real editorial
choice: two candidates should be plausibly good for different reasons.

When reporting results:

- keep candidates anonymous during judging;
- swap candidate order and require a stable verdict;
- record model, date, commit, and skill hash;
- quote the winning fragment and name the losing defect;
- treat results as regression evidence, not conversion proof.

See [`benchmarks/README.md`](benchmarks/README.md) for the current protocol.

## Pull requests

Keep each pull request about one behavioral improvement. Explain:

- what generic behavior the agent currently produces;
- what new evidence or editorial move changes that behavior;
- how another contributor can tell whether the change worked;
- which examples or benchmark cases demonstrate it.

Run the repository tests before opening the pull request:

```bash
python3 -m unittest discover -s benchmarks -p 'test_*.py'
```

If a contribution only makes Redpen longer, it is not finished. Any instruction
that is not changing the work is working against it.
