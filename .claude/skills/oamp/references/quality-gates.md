# Quality Gates

Blocking conditions. Each phase must pass before advancing to next. Fail → stay in current phase, do not advance.

---

## R2: Fragment Collection

- [ ] Each fragment has at least one design question assigned
- [ ] ≥ 3 fragments comparable at the design-question level
- [ ] Able to state: "this input answers the design question: [X]"

Fail → return to counterexample probing.

---

## Structure-First Path

### S1: Core Interest Synthesis

- [ ] Core interest definition ≤ 1 sentence
- [ ] Every keyword in the sentence can reverse-derive at least one information dimension

> 1 sentence OR keyword can't derive dimension → return to refinement.

### S2: Dimension Derivation

- [ ] 3-5 dimensions, each passes four checks (orthogonal, independently navigable, complete coverage, irreducible)
- [ ] Instances correctly identified as intersections, not misclassified as dimensions

---

## Exploration-First Path

### E1: Deep Probing

- [ ] At least 1 underlying design constraint or preference reached
- [ ] Counterexample has forced a boundary definition — "the boundary is here" confirmed

All fragments marked "undetermined" → return to probing.

### E3: Pattern Emergence

- [ ] ≥ 5 notes before finding patterns (do not force)
- [ ] User confirmed without hesitation ("sort of... but not quite" = fail)

---

## User-Material Path

### U2: Document Deconstruction

- [ ] Can state the document's design question in one sentence
- [ ] ≥ 2 implicit assumptions identified (author didn't state but relied on)
- [ ] ≥ 1 open question found (author raised but didn't answer)

Fail → return to U2 steps 2-3. Do not advance to U3.

### U3: Structured Restructuring (4 quality gates)

Missing any gate = U3 not complete:

- [ ] ≥ 1 callout marks a non-obvious insight or open question
- [ ] ≥ 1 Mermaid or structured list shows logic flow
- [ ] ≥ 3 redlinks are questions, not nouns (strip `[[]]` → complete question or explorable topic)
- [ ] Frontmatter includes tags (≥ 3)

---

## R4: Room Assembly (post-creation validation)

### File validation

- [ ] All `.md` frontmatter passes `yaml.safe_load`
- [ ] All `.canvas` passes `json.load` + edge integrity check + path prefix check
- [ ] All `.base` passes YAML parse
- [ ] `[[wikilink]]` reachability verified (or explicitly documented as intentional redlink)

### Template validation

- [ ] Each field traces to a core-interest keyword (see `template-protocol.md`)
- [ ] Same-name fields identical across all templates
- [ ] Base-referenced properties defined in template frontmatter

### Redlink validation

- [ ] Each wiki entry contains 2-3 redlinks
- [ ] Each redlink is a question, not a noun

---

## Phase 7: Expansion (iteration stop condition)

- [ ] Two consecutive scans yield zero new meaningful redlinks → room mature

Mature ≠ complete. Resume from step 1 when new input arrives.
