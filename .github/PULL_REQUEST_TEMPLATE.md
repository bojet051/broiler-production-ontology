## Summary
- [ ] This PR updates ontology content
- [ ] This PR updates curation candidates/prompts only
- [ ] This PR updates docs only

Describe the change briefly:

## LLM Curation Inputs (if applicable)
- Candidate file(s):
  - `curation/candidates/...` (or link)
- Prompt assets used:
  - `curation/prompts/system-prompt.md`
  - `curation/prompts/candidate-generation-prompt.md`
  - `curation/prompts/self-check-prompt.md`

## Review Checklist (Required for ontology changes)
Reference: `curation/review-checklist.md`

- [ ] Candidate schema compliance confirmed
- [ ] Evidence quality reviewed
- [ ] Semantic fit reviewed
- [ ] Backward compatibility assessed
- [ ] Candidate review status updated

## Validation
- [ ] `cd src/ontology && sh ./run.sh make test` passed locally
- [ ] GitHub CI (`qc.yml`) passed
- [ ] Docs workflow passed (if docs changed)

## Notes for Reviewers
Anything reviewers should focus on:
