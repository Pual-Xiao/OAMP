# oamp — Obsidian Automated Memory Palace

> Not another folder template. A derivation system that takes you from "what do I like?" to "what do I actually care about?"

## What's New

### v1.0 (2026-06-06) — Initial Release

- 12 execution rules embedded in SKILL.md, active on install, zero configuration
- 13 design principles + M0 through M11 (12 derivation methods), complete reference system
- Three processing paths — Structure-First / Exploration-First / User-Material — auto-matched to your fragment count
- 9 Python scripts covering the full lifecycle from creation to expansion
- One-line install: `npx skills add Pual-Xiao/Obsidian-Automation`

## Understand oamp Through One Example

What follows is a **real conversation** — a user said one sentence, and oamp took it from there, through the full process from fragments to knowledge structure. Every concept is explained as it naturally emerges.

### Starting point: one sentence

> "I don't know why, but blue just attracts me. I love the blue of the sea, the blue of the sky, Sayram Lake — pure, flawless blue."

One fragment. oamp won't ask you to create a "Colors → Blue" folder. That's filing. Not thinking.

oamp's work starts here.

### Step 1: Deep probe — find design questions, not categories

oamp's first move isn't organizing. It's **questioning**. Three angles:

**Positive examples**: Sayram Lake — blue in a natural body of water. Light penetrates water, gets absorbed, scattered, refracted. Every layer of blue encodes depth and mineral information.

**Counterexample**: oamp asks "is there a blue you don't like?" — "The blue glass curtain walls on buildings — I don't like them at all." Blue on glass is a coating reflecting the sky — the blue isn't inside the glass, it's on the surface. The glass refused to participate. The blue is a photocopy of the sky.

**Cross-domain comparison**: oamp continues — "besides blue, does anything else give you the same feeling?" — "Black. Natural black contains so much information beyond just black. Man-made black is mixed from RGB — digital black, I don't like it."

Natural black has shadows and texture — black isn't a color, it's the **residue** of light blocked by objects. RGB black `#000000` is a lightswitch turned off. Zero information.

**Cross-sensory verification**: oamp digs further — "beyond the visual, any similar experiences?" — "Sound. Hearing a singer perform live versus a digital recording — they're not the same thing at all."

A live voice passes through the singer's body, breath, muscle tension — the sound carries **the full state of that body in that moment**. Digital strips all of that away. Your headphones and my headphones hear the same string of 0s and 1s.

### Step 2: Emergence — find what you didn't say out loud

After five rounds of probing, there are enough fragments. oamp lays the design questions side by side:

| Fragment | Design question | Key difference |
|----------|----------------|----------------|
| Sayram Lake blue | Light penetrates water — each shade of blue differs by depth and minerals | Blue **carries the light's travel log** |
| Glass curtain wall blue | Coating bounces sky — blue has zero causal relationship with glass | Blue **lost its causal history** |
| Natural black | Shadows have shape — black is evidence that "something blocked the light" | Black **contains the full record of the occlusion event** |
| RGB black `#000000` | Pixels commanded not to emit — no light, no object, no space | Black **is an instruction, with no past** |
| Live singing | Sound passes through body and air — every detail is the result of a physical state | Sound **lets you reverse-engineer the singer's state in that moment** |
| Digital recording | File gets decoded — the speaker is arbitrarily replaceable | Sound **carries nothing of the process that produced it** |

oamp isn't asking you to sort things into "blue things" and "not-blue things." It's doing something entirely different: **finding the underlying commonality that crosses vision, hearing, and touch.**

Then oamp feeds the discovery back to you:

> "You don't care about color. Or sound. Or the medium itself. What you care about is: **can you read a thing's history off the thing itself?**"
>
> Sayram Lake's blue isn't a color — it's light's biography in water. You can reverse-engineer water depth and mineral content from the blue's layers. The blue carries **causal history**.
>
> Glass curtain wall blue has no biography. The blue tells you the sky's color, but has zero causal relationship with the glass — **the causal chain has been severed**.
>
> You don't reject glass, or digital recordings, or `#000000`. You reject — a perfectly clean **result that has been stripped of its production history**, no matter how perfect it looks.

You confirmed: "That's it."

### Step 3: Synthesis — one sentence

The moment you confirm, oamp compresses the entire conversation into **one sentence**:

> Preference for things that carry their own causal history — where the result is a fossil of the process, where the product contains readable traces of its own origin. Rejection of results stripped of their production history.

This is your **core interest**. Every downstream decision — what folders to create, what fields to use, what to write — must trace back to this sentence. More than one sentence = not thought through yet.

### Step 4: Derive dimensions — three independent pillars

With the core interest locked in, oamp extracts keywords and reverse-derives **dimensions**.

A dimension is an **independent information axis**. Like database columns: each column tracks a different thing, and you can browse any column independently and find a complete story.

| Keyword | Derived dimension | Explanation |
|---------|------------------|-------------|
| "causal history""production history" | **Generation mode** | How did the thing come to be? Physical interaction / biological process / signal transmission / digital command |
| "readable traces""process fossil" | **Causal readability** | Can you reverse-engineer the production process from the result? Full → partial → none |
| "carries itself""stripped" | **Temporal embedding** | Is the result bound to a specific moment/place, or infinitely reproducible? |

Four checks — all four passed:

| Check | Result |
|-------|--------|
| Orthogonal | Mode (what happened) ≠ Readability (how much is visible) ≠ Time (when) — no overlap |
| Independently navigable | Browsing by "physically produced things" works alone; by "fully readable processes" works alone; by "moment-bound events" works alone |
| Complete coverage | Every keyword has a home dimension |
| Irreducible | Delete any one — specific queries become impossible |

**Key distinction — an instance is not a dimension**: Sayram Lake is "physical process × fully causally readable × temporally bound" — it's the **intersection** of three dimensions, not a new one. An instance is the **product** of dimensions crossing. Store one file, reach it via `[[wikilink]]` from all relevant dimensions.

### Step 5: Folder numbering — the numbers ARE the narrative

oamp names folders with numbered prefixes. The numbers aren't random — **the numbering IS the causal narrative**:

```
00-entry/              ← Index, seen first
01-generation-mode/    ← Causal start: process type determines everything downstream
02-causal-readability/ ← Downstream: how much readable trace did the process leave?
03-temporal-embedding/ ← Further downstream: can the result exist apart from its moment?
04-instances/          ← The product of three dimensions intersecting
05-cross-topics/       ← Cross-dimensional themes (e.g. "authenticity in the age of digital reproduction")
06-cross-links/        ← Beyond the domain (e.g. "preserving original traces in artifact restoration")
07-output/             ← Output + source materials
```

Causal chain: generation mode → trace quantity → time binding. Reverse any one, the narrative breaks. **If reordering doesn't change the thought, it's just filing — oamp doesn't do filing.**

### Step 6: Template derivation (M6) — every field needs a birth certificate

With the dimensional structure in place, oamp designs **templates** — the frontmatter fields each note type uses.

**What's M6?** oamp has 12 numbered methods (M = Method). Each defines: input → output → blocking conditions (what must be true before moving forward). M6 is the "template field derivation method." They're numbered because steps depend on each other — M2's output is M3's input, and you can't skip.

M6's core rule: **Every template field must trace to a keyword in the core interest sentence. Can't trace → delete.**

Instance template fields:

| Field | Traces to which keyword | Why |
|-------|------------------------|-----|
| `generation_mode` | "causal history""production history" | Physical process / signal transmission / digital command |
| `causal_readability` | "readable traces""process fossil" | full / partial / none |
| `temporal_embedding` | "carries itself""stripped" | bound (to a moment) / transferable / independent |
| `medium_necessity` | "carries itself" | irreplaceable (medium matters) / replaceable / irrelevant |
| `trace_evidence` | "readable traces" | What specific traces allow reverse-engineering the process? (e.g. blue layers → mineral content → depth) |

**Template iron rule**: Same-named fields must be IDENTICAL across all templates. `causal_readability` in this template means `causal_readability` in every other — never `CausalReadability`. Why? Obsidian database queries match on exact field names. One mismatch = two instances never appear in the same query result. This isn't a naming preference — it's **data accessibility**.

### Step 7: Redlinks — not bugs, but seeds

**What's a redlink?** In Obsidian, `[[some-page]]` is a wikilink. If `some-page.md` doesn't exist yet, the link appears red.

Traditional tools treat redlinks as bugs — broken links to fix. oamp treats them as **intent traces**: when you write `[[why does digital reproduction strip causal history?]]`, even though the page doesn't exist, you've **encoded a question you want to explore**. A redlink is a research task for your future self.

oamp requires every note to leave 2-3 redlinks behind, and each must be a **question**, not a noun:

- ✅ `[[why does RGB black contain zero physical information?]]` — strip `[[]]` and it's a complete question
- ❌ `[[RGB black]]` — strip `[[]]` and it's just a noun; you haven't said what you want to know

### Step 8: The expansion loop

The room is built. Then oamp enters the **expansion loop**:

```
Scan redlinks → find all [[pages that don't exist yet]]
    ↓
Decide per redlink: Fill / Describe / Skip
    ↓
Fill → write a new note → new note leaves new redlinks → return to scan
    ↓
Two consecutive scans with zero new meaningful redlinks → room mature
```

- **Fill**: redlink directly serves the core interest → write a full entry
- **Describe**: too common for its own page → explain in a sentence, remove the `[[]]`
- **Skip**: unsure → keep the redlink, re-evaluate next scan

Mature ≠ complete. New thoughts arrive, the loop resumes.

---

This example — from "I like blue" to a complete dimensional system, folder structure, and template fields — **is the output of a real conversation**, not something made up for a README. That's what oamp does.

## Why This Approach

Obsidian gives infinite freedom — and therefore zero built-in structure. You can organize folders any way. Every classification is reasonable, but **choosing a classification before you understand is locking in a way of seeing**. You haven't figured out what you care about, and the folder structure has already decided for you.

What oamp does is the opposite: **don't create folders first. Figure out what you care about first. Then derive the unique, causally coherent structure from that sentence.** Structure isn't how you organize files — structure is your thinking, encoded.

## From → To

| Traditional approach | oamp |
|---------------------|------|
| Create folders first, then decide what goes in them | Probe each fragment's design question first, then derive structure |
| Folders sorted alphabetically / by count / by popularity | Numbering IS the causal narrative: mode → trace → time. Change the order, change the thought |
| "Blue things go in the blue folder" | Sayram Lake is generation mode × causal readability × temporal embedding — file in instances, link from three dimensions |
| Copy template fields from another room | M6 derivation: every field must trace to THIS room's core interest keywords. Can't trace → delete |
| Redlinks are broken links to fix | Redlinks are intent traces: `[[why does digital reproduction strip causal history?]]` is a research task you gave yourself |
| Notes must be "correct" — don't write if you're unsure | Exploratory notes aren't for correctness — they're for exposing what you care about. Re-read. Patterns surface from what you actually wrote |
| Knowledge base maintenance is manual | 9 scripts: `freshness` perceive → `scaffold` create → `migrate` restructure → `validate` check → `wikilinks`/`redlinks` link → `unlink` clean |

## Quality Gates — Can't Proceed Without Passing

Every phase has blocking conditions. Previous step must pass before you can move forward:

| Phase | What blocks you | Why |
|-------|----------------|-----|
| Fragment collection | < 3 fragments, or can't state the design question behind each | Not enough information. Keep talking. Don't rush into structure |
| Deep probing | Haven't reached an underlying design constraint, or the counterexample didn't force a boundary definition | Still at the surface — haven't reached the design-question level |
| Core interest | Can't write one sentence, or keywords can't map to dimensions | Haven't thought it through. Go back and refine |
| Dimension derivation | Not 3-5, or any dimension fails the four checks | The dimensional skeleton is the most critical piece — orthogonal, independently navigable, complete coverage, irreducible — all four must pass |
| Pattern emergence | < 5 notes and already forcing patterns. User says "yeah... but not exactly" | < 5 is not enough to find patterns. Hesitation = not confirmed |
| Expansion stop | Two consecutive scans produce zero new meaningful redlinks | Known questions in this domain are covered — temporarily mature. New input resumes the loop anytime |

These gates aren't punishment — they're protection. They stop you from building folders you'll never use.

## Three Paths

Not everyone starts with structure. oamp matches the path to your state:

**Structure-First (S1-S5)**: Many fragments (≥ 6) and you can describe relationships → Build structure first, then fill content. The blue conversation above walks something close to this path — fragments came fast, depth was there from the start.

**Exploration-First (E1-E4)**: Just developing an interest, few fragments (< 6), unsure what you care about → Write "discovery notes": no classification, no dimensions, no templates, no frontmatter. Just write. After 5-10 notes, re-read everything. Patterns surface on their own from what you actually wrote.

**User-Material (U1-U5)**: You already have documents, notes, articles → Deconstruct the source (extract skeleton, separate judgments from facts, mark open questions), then restructure by causality into structured knowledge.

All three converge at the same exit: dimensions → folders → templates → wiki → expansion loop.

## What's in the Box

### 9 Scripts

| Script | What it does | When |
|--------|-------------|------|
| `freshness.py` | Snapshots the room's current state | Before every operation — no snapshot = operating blind |
| `scaffold.py` | Generates folder skeleton + entry index + registers the room | After dimensions are confirmed |
| `migrate.py` | Moves discovery notes from temp folder to dimension folders | After exploration phase ends (Phase 5X) |
| `validate.py` | Checks frontmatter formatting, detects empty notes | After every modification |
| `wikilinks.py` | Link reachability, redlink scan, orphan detection | Maintaining link health |
| `redlinks.py` | Scans redlinks, groups by dimension, sorts by reference count | First step of the expansion loop |
| `unlink.py` | Deletes notes and cleans up all references to them | When content needs removal |
| `example_builder.py` | Exports a room as an example | Showcasing your knowledge structure |
| `room_registry.py` | Manages the room registry | Multi-room management |

### 6 Reference Files

| File | Content |
|------|---------|
| `principles.md` | 13 design principles with full explanations + method mappings |
| `metrology.md` | M0-M11 derivation methods: steps, I/O, blocking conditions, failure boundaries |
| `tech-rules.md` | YAML/Mermaid/Canvas syntax, folder naming, CLI commands, SCHEMA protocol |
| `template-protocol.md` | Field traceability, same-name identity, enum values, tag hierarchy |
| `quality-gates.md` | Detailed blocking conditions per phase + validation checklist |
| `expansion-engine.md` | Complete expansion loop: scan → decide → create → prune → stop |

SKILL.md is the execution entry point. The LLM reads reference files on demand when executing the relevant step.

## Quick Start

```bash
# Install
npx skills add Pual-Xiao/Obsidian-Automation

# In Claude Code
/oamp → tell it what you want to organize → follow the flow
```

Permissions declared in SKILL.md. Auto-merged on install. No manual configuration.

## Design Sources

oamp doesn't come from any existing knowledge management framework. Every design decision is derived from first principles:

- **A file can only live in one folder** → but can be reached from many paths via `[[]]` → Dimension system: store once, link everywhere
- **Numbers that don't encode information are wasted** → must encode causal relationships to have navigational semantics → Alphabetical/popularity ordering forbidden
- **Inconsistent field names = data you can never query** → not a naming preference, it's data accessibility → Template iron rule: same-name fields absolutely consistent
- **Redlinks = variant seeds** → fill what serves, describe what's common, skip what's uncertain → Expansion engine
- **You don't know what you think until you see what you wrote** → Exploratory notes aren't for correctness, they're for exposure

No design decision is adopted because "everyone else does it this way."
