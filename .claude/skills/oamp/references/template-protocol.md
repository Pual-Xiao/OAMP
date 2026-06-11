# Template Protocol

Template fields = query infrastructure. Inconsistent fields = instances never appear in same query result.

## 1. Field Traceability

Every template field must trace to a core-interest keyword. Traceable source required.

- Design question: "Which core-interest keyword does this field trace to?"
- Cannot trace → delete the field. No decorative fields.
- Field appears in notes but not in any template → treat as bug.

## 2. Same-Name Identity

Same field name must be IDENTICAL across all templates.

| Fail | Pass |
|------|------|
| `structural_system` in tpl-building, `structure` in tpl-material | `structural_system` everywhere |
| `field_name` / `fieldName` / `Field-Name` mixed | `field_name` only |

**Naming rules**:
- English snake_case
- Multi-word with underscores
- List values: YAML list syntax (`- item`)
- No empty strings `""` — field has a value or is absent

Set display name via Obsidian Base `displayName`. Do not encode display names in frontmatter keys.

## 3. Classification Field Enum Values

Classification fields (e.g. `concept_type`) must enumerate allowed values in the template. Never invent values at write time.

- Same classification field uses same enum set across all templates
- New enum value → update all templates first, then use

## 4. Tag Hierarchy

Format: `<domain>/<subdomain>`

- Level 1: domain (e.g. `architecture`)
- Level 2: module (e.g. `structure-form`)
- Level 3+: granularity (e.g. `paradigm-shift`)
- All lowercase, hyphen-separated

Tags must not duplicate information already in frontmatter fields.

## 5. Base-Frontmatter Sync

Every property referenced in Base must be defined in the template's frontmatter.

- Base formula references a property → property exists in template
- Display name mismatch → Base shows wrong label
- Type mismatch → formula fails silently

## 6. Wikilink Field Quoting

Field value contains `[[wikilink]]` → MUST wrap in single quotes.

```yaml
# Correct
related: '[[brutalism]], [[modernism]]'

# Wrong — YAML parses [[ as flow sequence
related: [[brutalism]], [[modernism]]
```

Template must note this requirement for any field expected to contain wikilinks.
