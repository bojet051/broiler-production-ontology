# Prompt Pack Usage

This directory contains prompt assets for Step 3: prompt templates and guardrails.

## Files
- `system-prompt.md` — baseline behavior and safety constraints
- `candidate-generation-prompt.md` — produces one schema-compliant candidate YAML
- `self-check-prompt.md` — validates candidate quality before PR
- `guardrails.md` — merge/review policy and rejection criteria

## Recommended Flow
1. Generate candidate using:
   - `system-prompt.md` + `candidate-generation-prompt.md`
2. Run internal QA using:
   - `self-check-prompt.md`
3. If verdict is `pass`, submit candidate for human review.
4. If accepted, apply ontology changes and run:
   - `cd src/ontology && sh ./run.sh make test`

## Output Expectations
- Candidate output must follow `curation/candidate-schema.json`.
- Keep one candidate per file for traceable reviews.
- Attach candidate file to the PR that applies ontology edits.

## Naming Convention
Suggested candidate file naming:
- `curation/candidates/CAND-YYYY-NNN.yaml`

Example:
- `curation/candidate-example.yaml`
