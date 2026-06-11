# Metrology — Derivation Methods

Each method: steps → input/output → blocking conditions → failure boundaries.

---

## M0. Perceive Before Act

**Referenced by**: Main Router R4

1. Run `python3 <skill-dir>/scripts/freshness.py --room "<name>"`
2. Writes `<project>/.oamp/freshness/<room>.json`
3. Downstream scripts scope changes from this snapshot

Without this snapshot, every downstream tool operates blind.

---

## M1. Extract Design Question from Fragment

**Referenced by**: Main Router R2

1. For each fragment, pick a representative case
2. Ask: *"What constraint was this case designed to solve?"*
3. Do NOT compare surface features (era, geography, scale) — compare design questions
4. List design questions side by side

**Input**: Raw interest fragments (user's own words)
**Output**: Per fragment — one sentence: "It answers the design question: [X]"

**Failure**: Category labels instead of design questions ("they're all architecture"); style labels instead of design questions ("they're all minimalist" → what constraint does minimalism answer?)

**Blocking**: < 3 fragments with clear design questions → keep probing, do not advance

---

## M2. Core Interest Synthesis

**Referenced by**: Structure-First S1 / Exploration E3 / User-Material U4

### M2a. Find Underlying Commonalities

1. Compare design questions across fragments — find shared judgment criteria
2. Not "do they look similar?" — "do they share an answer to what is right?"
3. Search space:
   - What constraint do they collectively value?
   - What do they collectively reject?
   - What pattern repeats? ("first to do X", "logic of the material itself", "form derived from constraints")

**Output**: 2-4 underlying commonalities. Each is one judgment criterion.

**Blocking**: < 2 shared judgment criteria → return to M1 with targeted probes

### M2b. Compress to Core Interest

1. Find the intersection of commonalities — what aspect of the same thing are they all pointing at?
2. Synthesize into one sentence: `{preference} for {what}, particularly {which aspect}`

**Quality checks**:
- A paragraph → not compressed enough
- Contains "and" joining two independent interests → two core interests, not one
- Can every downstream decision (dimensions, folders, template fields) trace back to this sentence?

**Blocking**: > 1 sentence or fails quality checks → do not advance

---

## M3. Dimension vs Instance

**Referenced by**: Structure-First S2 / Exploration E4 / User-Material U5

For any candidate entity, ask: *"Can it be described as a combination of existing dimensions?"*
- Yes → instance (intersection), not a dimension
- No → independent information axis, may be a dimension

**Order**: Dimensions first (navigation paths), instances second (destinations). Never reverse.

**Intuition correction**: The natural instinct is to classify by name — make the subject of study the primary dimension. But the subject is the intersection of multiple dimensions (who made it × what system × what material × what era). One file lives in one folder, but belongs to many navigation paths. Put it in the semantically best-match folder; other paths reach it via `[[]]`.

---

## M4. Dimension Derivation

**Referenced by**: Structure-First S2 / Exploration E4 / User-Material U5

### M4a. Reverse-Derive from Core Interest

1. Extract all keywords from the core interest sentence
2. For each keyword: to track this, what information dimension is needed?
3. Output: keyword → dimension candidate mapping

### M4b. Four Checks (all must pass)

| Check | Question | Fail → |
|-------|----------|--------|
| Orthogonal | Do dimensions A and B track the same thing? | Overlap → merge |
| Independently navigable | Does this dimension alone have a narrative arc? | No → subordinate info, cut |
| Complete coverage | Does every core-interest keyword have a corresponding dimension? | Missing path → add dimension |
| Irreducible | Remove it — what query becomes impossible? | Unimportant → cut; important → keep |

**Target**: 3-5 dimensions. Fewer = merged axes that shouldn't be merged. More = fragmentation.

---

## M5. Folder Structure Design

**Referenced by**: Structure-First S3 / Exploration E4 / User-Material U5

### Numbering Template

```
00-入口/              ← index, seen first
01-{dim-1}/           ← causal origin
02-{dim-2}/           ← downstream from 01
...
0N-{dim-N}/           ← causal terminus
0N+1-实例/            ← intersection product: dimensions interweave to form this
0N+2-交叉专题/        ← cross-dimensional themes
0N+3-跨界连接/        ← beyond domain boundary
0N+4-产出+资料/       ← output + source materials
```

Causal narrative: dimensions (01-0N) interweave → instance (0N+1) is their product → instance radiates influence outward (0N+2+). The numbering IS the narrative. Changing the order breaks the narrative.

### Causal Chain Determination

Find the categorial relationship between dimensions: actor produces paradigm → paradigm selects method → method determines implementation → implementation chooses medium. Write the chain explicitly before assigning numbers.

### Numbering Constraints

- Two-digit IDs: `00`, `01`, ... `0N`. Pad single digits.
- Folder names follow vault language. Chinese names use `-` separator (not `_` or space).
- Causal order must be explicit before folder creation. If uncertain, return to core interest.

### Forbidden

Alphabetical order, popularity order, entry-count order — no navigational semantics.

### Verification

After designing the structure, ask: if you changed the folder order, would the thought change? If not, the structure is organizing files, not encoding thought. The structure IS the thought — a correct structure cannot be reordered without breaking the narrative.

### MOC Principle

Store once, link everywhere. Each note lives in its semantically best-match dimension folder. Other dimensions reference it via `[[]]`. Never duplicate files.

No per-dimension MOC unless the dimension exceeds 20 notes.

Entry MOC skeleton:
```markdown
# {room-name}

## Dimension navigation
- [[01-{dim-1}/]] — {one-line description}
- [[02-{dim-2}/]] — {one-line description}
...

## Quick access
- Canvas view
- Database view
- Timeline
```

---

## M6. Template Field Derivation

**Referenced by**: Structure-First S4

Derive fields from this room's own dimensions. Do not copy template files from existing rooms. If user explicitly requests reuse: ask which room, read its templates, adapt — never copy verbatim.

1. For each entity type: what must it record to serve the core interest?
2. Every field traces back to at least one core-interest keyword
3. Cannot trace → delete

**Iron rule**: Same-named field must be IDENTICAL across all templates. `field_name` in template A is `field_name` in template B — never `fieldName` or `Field-Name`. Inconsistency = these two instances never appear in the same query result.

**Naming**: English snake_case, multi-word with underscores, list values in YAML list syntax (`- item`). Every field has a value or is absent — no empty strings `""`. Set display name in Base via `displayName`, not in frontmatter.

Full field protocol (traceability, enum values, tags hierarchy, Base sync): see `template-protocol.md`.

### Field Checklist

Design each field by asking:
- [ ] Which core-interest keyword does this field trace to?
- [ ] Is this field name identical across all templates?
- [ ] If it's a list field, is it YAML list syntax (`- item`)?
- [ ] If the value may contain `[[wikilink]]`, does the template note the single-quote requirement?

---

## M7. Redlink Write + Fill/Describe/Skip Decision

**Referenced by**: Main Router R4

### Write Rules

- 2-3 `[[redlinks]]` per wiki entry
- A redlink is a question, not a noun: `[[why did X decline]]` not `[[X]]`
- A non-existent link is not a bug — it is encoded but unrealized intent

### Scan Decision

After `python3 scripts/redlinks.py --vault <vault> --room <room>` scan:

| Decision | Condition | Action |
|----------|-----------|--------|
| Fill | Redlink directly serves core interest | Create entry with template |
| Describe | Concept too common for standalone entry | Plain text in body, no `[[]]` |
| Skip | Uncertain | Keep redlink, re-evaluate next scan |

Full expansion procedure (trigger, scan, decide, create, loop, prune, stop): see `expansion-engine.md`.

---

## M8. Deep Probing

**Referenced by**: Exploration E1

For each fragment, three angles:

1. **Design question**: "You like X — what constraint was X designed to solve?"
2. **Opposite**: "Is there an anti-X you dislike?"
3. **Co-occurrence**: "Why is the same person drawn to both?"

**Blocking** (both required):
- At least 1 underlying design constraint identified
- A counterexample has forced a boundary definition

---

## M9. Pattern Emergence

**Referenced by**: Exploration E3 / User-Material U4

1. Re-read all written content — find recurring words, contrasts, judgment criteria
2. List observed patterns
3. Present to user: "I notice [A], [B], [C]... what matters to you is [X] — correct?"
4. On confirmation → distill into core interest (M2b)

**Forbidden**:
- Force patterns with < 5 items
- Skip when user hesitates ("yeah..." ≠ confirmation)
- Pre-design patterns — patterns emerge, they are not designed

---

## M10. Document Deconstruction

**Referenced by**: User-Material U2, U3

### Deconstruct

1. Extract narrative skeleton — what it says, in what order, what it concludes
2. Identify assumptions — user judgments (probe-able) vs facts (verifiable)
3. Mark open questions — raised but unanswered
4. Map logic flow — steps/process/causality in prose

### Restructure

1. Reorder by causality/hierarchy — not original sequence
2. Make implicit assumptions explicit → `> [!question]` callout
3. Diagram logic flow → Mermaid or structured list
4. Introduce wikilinks — each is a question, not a noun
5. Mark replicability bottlenecks → `> [!warning]`
6. Frontmatter ≥ 3 domain tags

---

## M11. Expansion Cycle

**Referenced by**: Main Router R4

```
redlink scan → decide (fill/describe/skip) → create entries → new entries introduce new redlinks → loop
                                                    ↓
                                              prune unwanted nodes
```

**Cross-dimensional emergence**: After instances accumulate, cross-dimensional patterns surface naturally → create cross-cutting entries. Patterns emerge; they are not designed.

**Stop condition**: Two consecutive scans yield no new meaningful redlinks → room is mature.

Full procedure: see `expansion-engine.md`.
