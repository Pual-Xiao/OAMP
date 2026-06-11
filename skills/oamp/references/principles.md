# Principles

13 principles. Each is a transferable judgment framework — not a rule, but a way to decide. Every principle maps to a method in `metrology.md`. Principle = why. Method = how.

---

## 1. Compare by design problem, not surface features

Era, geography, scale, style — all surface. What matters: what constraint was this fragment answering?

Counterexamples define boundaries more precisely than positive examples. "What you thought you should like but don't" reveals judgment criteria that "what you like" cannot.

**Method**: M1 Extract Design Question, M8 Deep Probing

---

## 2. Core interest must be one sentence

More than one sentence = not distilled. This sentence is the axis: change it and dimensions, numbering, templates, canvas all change.

Every downstream decision must trace back to this sentence. Cannot trace → the sentence is wrong, or the decision is wrong.

**Method**: M2 Core Interest Synthesis

---

## 3. Instances are dimension intersections, not dimensions

"Buildings go in the building folder" kills every other navigation path. An instance is the product of multiple dimensions intersecting. File it in its best-match folder. Reach it from all other dimensions via `[[]]`. One file, many paths.

**Method**: M3 Dimension vs Instance

---

## 4. Dimensional orthogonality

3-5 dimensions. Each must be: orthogonal (different thing), independently navigable (has a narrative arc alone), collectively exhaustive (every keyword has a home), irreducible (remove it and a query dies).

**Method**: M4 Dimension Derivation

---

## 5. Numbering encodes the full causal narrative

Dimensions (01-0N) interweave to form instances (0N+1). Instances radiate outward: cross-dimensional themes (0N+2), cross-boundary connections (0N+3), output (0N+4).

The numbering IS the narrative. Changing the order breaks the narrative.

**Method**: M5 Folder Structure Design

---

## 6. Architecture encodes thought

Folder structure does not represent your thinking — it IS your thinking. Dimensions, causal order, and how they interweave are not "organization" applied after thought. They are the thought itself, made navigable.

If you changed the folder order, the thought would change. Structure and content are inseparable.

**Method**: M5 Folder Structure Design

---

## 7. Principles are the real template

Any room derived from principles and methodology is already using the template at the thought level — whether or not you physically copy `.md` files. Template files are the terminal expression of a thought process. The thought process itself is the real template.

This is why every room, no matter how different its domain, uses the same template at the structural level — and why no two rooms should ever have identical template files.

**Method**: M6 Template Field Derivation

---

## 8. Derive, don't copy

Templates are born from a room's own dimensions. Every field traces to a core-interest keyword. Cannot trace → delete.

Copying templates from an existing room skips the derivation step. The result is fields that don't trace to the new room's core interest — query infrastructure that doesn't serve the room it's in. If the user explicitly insists on reuse: ask which room, read its templates, adapt. Never copy verbatim.

**Method**: M6 Template Field Derivation

---

## 9. Templates are query infrastructure

Same field name across all templates = queryable. One mismatch = two instances never appear in the same query result. This is not a naming preference — it is data accessibility.

Field traceability, same-name identity, enum values, tag hierarchy, Base-frontmatter sync: all serve the query.

**Method**: M6 + template-protocol.md

---

## 10. Redlinks are intent traces

`[[does-not-exist]]` is not a broken link — it is encoded but unrealized intent. It marks "worth investigating here."

Each wiki entry: 2-3 redlinks. Each redlink: a question, not a noun. Strip `[[]]` → complete question.

Fill what serves core interest. Describe the rest in plain text. Skip what is uncertain — re-evaluate next scan.

**Method**: M7 Redlink Write + Fill/Describe/Skip

---

## 11. Notes are probes, not answers

Exploratory notes are not written to be correct. They are written to expose what you care about. You write to discover your own dimensions.

After writing: re-read. Patterns emerge. Do not design them — they surface from what you actually wrote, not from what you intended to write.

**Method**: M8 Deep Probing, M9 Pattern Emergence

---

## 12. Expansion cycle

Write → leave redlinks → scan → fill → repeat. Two consecutive scans yield zero new meaningful redlinks → room mature.

Mature ≠ complete. New input → resume the cycle.

Patterns emerge; they are not designed. Cross-dimensional patterns surface naturally after ~30+ instances accumulate. Do not force them earlier.

**Method**: M11 Expansion Cycle, M7 Fill/Describe/Skip

---

## 13. Perceive before act

What changed since the last operation? Without knowing the delta, every downstream tool operates blind.

Always run `freshness.py` before room operations. Downstream scripts scope changes from this snapshot.

**Method**: freshness.py (pre-operation diagnostic)
