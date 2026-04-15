# Candidate Self-Check Prompt

Run this prompt **after** generating a candidate YAML and before opening a PR.

---

You are validating an ontology curation candidate for structural and semantic quality.

## Input
- Candidate YAML: {{candidate_yaml}}
- Optional ontology excerpt/context: {{ontology_context}}

## Tasks
1. Check schema completeness against `curation/candidate-schema.json`.
2. Verify all required fields are present and value domains are legal.
3. Check semantic consistency of:
   - entity type vs parent target,
   - domain/range/inverse coherence (if present),
   - change intent vs backward compatibility tag.
4. Check evidence quality:
   - at least one source,
   - relevance statement is concrete,
   - no fabricated specifics.
5. Evaluate risk and confidence alignment.

## Output
Return two blocks:

### A) Verdict
- `pass` or `needs_revision`

### B) Fix List
A numbered list of exact fixes, each with:
- field path,
- issue,
- corrected value suggestion.

## Hard Fail Conditions
Return `needs_revision` if any of the following occurs:
- Missing required fields
- Invalid enum values
- Confidence out of range
- Empty evidence list
- Unsupported breaking change without notes
- Contradiction with stated modeling constraints
