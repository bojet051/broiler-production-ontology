# Candidate Generation Prompt

Use this prompt with the system prompt in `curation/prompts/system-prompt.md`.

---

Generate **one** ontology curation candidate for the Broiler Production Ontology.

## Inputs
- Subdomain: {{subdomain}}
- Desired change type: {{action}} (`add` | `update` | `deprecate` | `replace`)
- Seed concept(s): {{seed_concepts}}
- Evidence notes/sources: {{evidence_notes}}
- Reviewer focus: {{review_focus}}

## Output Contract
- Output YAML only.
- Must conform to `curation/candidate-schema.json`.
- Set `candidate_id` as `CAND-YYYY-NNN`.
- Set `created_at` in ISO-8601 UTC.
- Set `review.status` to `proposed`.
- Include `qa.confidence` in range [0,1].
- Include at least one evidence item with non-empty relevance statement.

## Generation Rules
1. Prefer backward-compatible modeling.
2. Keep naming style consistent with existing ontology entities.
3. Add deprecation links if replacing older terms.
4. If evidence is weak or partial, reduce confidence and mark `needs_review`.
5. Ensure every required field is present.

## Domain-Specific Guardrails
- Respect current restrictions and existing key relations around broiler, lifecycle, feed, observation, gender, and time modeling.
- Avoid proposing changes that conflict with cardinality assumptions unless explicitly requested.
- Preserve legacy compatibility pattern (deprecated terms retained where applicable).

Now generate the candidate.
