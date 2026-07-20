<div align="center">

# ✍️ Redpen

### AI copywriting that doesn't sound like AI.

**Redpen turns your coding agent into a copywriter with taste.** Every line it writes has to pass three questions before it ships — so your headlines, landing pages, and taglines stop reading like generic AI filler and start reading like something a person would remember.

Works in Claude Code, Cursor, Cline, Windsurf, Copilot, and any agent that reads a rules file.

</div>

---

You know the copy. "A powerful, seamless, all-in-one platform that empowers creators to unlock their potential." It's grammatical. It's confident. And it says **nothing** — you can't picture it, you can't prove it, and any competitor could sign the exact same line.

That's slop. Not because it's wrong, but because it's forgettable.

Redpen is the old ad man with the red pen, living inside your agent. You hand him a paragraph; he reads it, says nothing, crosses out five words, and leaves one line you can actually see.

## The three questions (the whole engine)

Every sentence runs all three. A line that fails one gets cut *before* the draft is "done" — not after.

| Question | Fails | Passes |
|---|---|---|
| **1. Can I visualize it?** | "Change an entire industry" — you see nothing | "Worn by supermodels in London and dads in Ohio" — you see it |
| **2. Can I falsify it?** | "He has great values" — air | "He reads on the tube" — provably true or false, so you sit up |
| **3. Can nobody else say it?** | "Don't just get a job" — any recruiter can sign it | "Your car has five numbers on the speedometer. Volvo has six." — only Volvo can say it |

Three no's and you're writing rubbish. Three yes's and you're onto something.

## Before → after

Same product. Left fails a test; right passes all three.

| Slop | Redpen |
|---|---|
| "A powerful, seamless AI platform that empowers creators." | **"1,000 songs in your pocket."** |
| "The best all-in-one wellness supplement." | **"You're going to need a smaller cabinet."** |
| "A dating app for meaningful long-term connections." | **"The dating app designed to be deleted."** |
| "Learn copywriting and grow your business fast!" | **"You'll spend 22,000 hours writing. Spend 2 learning how."** |

Every line on the right you can picture, it's true or false, and no competitor can sign it. And it lands in two seconds flat.

## Install

Redpen is one ruleset with adapters for every major agent. Pick yours.

**Claude Code** — copy [`skills/redpen/SKILL.md`](skills/redpen/SKILL.md) into `.claude/skills/redpen/SKILL.md`, then invoke with `/redpen` or just write copy while it's active.

**Cursor** — copy [`.cursor/rules/redpen.mdc`](.cursor/rules/redpen.mdc) into your project's `.cursor/rules/`.

**Cline** — copy [`.clinerules/redpen.md`](.clinerules/redpen.md) into `.clinerules/`.

**Windsurf** — copy [`.windsurf/rules/redpen.md`](.windsurf/rules/redpen.md).

**GitHub Copilot** — copy [`.github/copilot-instructions.md`](.github/copilot-instructions.md).

**Any other agent** — point it at [`AGENTS.md`](AGENTS.md).

## How it works

Once active, Redpen holds every line to the three questions and a short set of reflexes:

- **Point, don't talk.** Don't say "great investment" — point at the 50-year price chart.
- **Facts over adjectives.** If in doubt, give a fact. A fact is precise, true, and you can build a story on it.
- **Any word that isn't working for you is working against you.** Cross it out.
- **Concrete over abstract.** "Songs in your pocket," not "songs in your media player."
- **Conflict.** Hinge the line on an unspoken *but*. "Designed to be deleted."
- **Shorter wins.** Cut to one line, then bold the rhythm.

Full ruleset: [`skills/redpen/SKILL.md`](skills/redpen/SKILL.md). Worked examples: [`examples/`](examples/).

## FAQ

**How do I stop my AI copy from sounding generic?**
Generic AI copy is abstract, unfalsifiable, and interchangeable — the three things median training data rewards. Redpen forces every line to be concrete (you can picture it), falsifiable (provably true or false), and ownable (no competitor could sign it). Those three constraints are what separate memorable copy from filler.

**What are the three questions to test a headline?**
Can I visualize it? Can I falsify it? Can nobody else say it? Run all three on every line; cut anything that fails one.

**Can Claude / Cursor write good marketing copy?**
On its own it defaults to the statistical average, which is slop. With a rule that enforces concrete, falsifiable, ownable language, the same model writes copy that resonates. That rule is what Redpen installs.

**What's the difference between concrete and abstract copy?**
Abstract copy ("a better way," "empower creators") can't be dropped on your foot — you can't see it, so you won't remember it. Concrete copy ("1,000 songs in your pocket") is a thing you can picture. Concrete wins every time.

**What are Harry Dry's three questions?**
Can I visualize it? Can I falsify it? Can nobody else say it? Harry Dry — of Marketing Examples — asks these of every sentence he writes. Three no's and you're writing rubbish; three yes's and you're onto something. Redpen runs all three on every line automatically.

**What is the Harry Dry copywriting method?**
Make it visual (something you can picture), make it falsifiable (provably true or false, not an adjective), and make it so specific no competitor could sign it. Then point, don't talk — show a fact instead of describing a feeling. He breaks it down in full in his [76-minute copywriting talk](https://www.youtube.com/watch?v=TUMjnmfsPeM) on the *How I Write* podcast. Redpen turns that method into a rule your AI agent follows on every line.

## The method behind Redpen

Redpen is the copywriting method of **Harry Dry** — creator of [Marketing Examples](https://marketingexamples.com), who has taught 100,000+ people to write copy that rips — turned into a rule your agent can't ignore.

The three questions come straight from his framework, laid out in his **[76-minute copywriting breakdown](https://www.youtube.com/watch?v=TUMjnmfsPeM)** on David Perell's *How I Write* podcast. If a line can't be visualized, can't be falsified, and could be signed by a competitor, it gets cut. Harry teaches it with the ads everyone remembers — New Balance's "supermodels in London and dads in Ohio," The Economist, Volkswagen, Hinge's "designed to be deleted," Couch to 5K — plus Kaplan's Law of Words: *any word that isn't working for you is working against you.*

Redpen doesn't replace him — it enforces his rules on every line, so you get the discipline without having to hold it in your head. If you want the human version, [watch the talk](https://www.youtube.com/watch?v=TUMjnmfsPeM) and read [Marketing Examples](https://marketingexamples.com); it's the best copywriting on the internet.

## License

MIT — use it, fork it, ship better copy.
