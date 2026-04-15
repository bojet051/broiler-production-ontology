# LLM Curation Guardrails

These guardrails define acceptance boundaries for LLM-assisted ontology proposals.

## Mandatory Requirements
1. Candidate file must conform to `curation/candidate-schema.json`.
2. Candidate must include at least one evidence item and explicit relevance.
3. Candidate must include a reviewer-ready rationale for key axioms.
4. Candidate must not silently remove or redefine existing semantics.
5. Any replacement must include backward compatibility strategy.

## Rejection Rules (Auto-Reject)
Reject candidate immediately if any applies:
- Missing required schema fields
- Unparseable YAML
- Unsupported enum values
- No evidence or vague/non-informative evidence
- Claims of certainty without supporting context
- Proposed breaking change without `breaking_change_notes`
- Direct conflict with established core restrictions/patterns without explicit migration plan

## High-Risk Rules (Manual Escalation)
Require senior reviewer when:
- Candidate touches high-impact core entities or constraints
- Candidate changes cardinality assumptions
- Candidate introduces broad refactoring across multiple branches
- Candidate deprecates terms currently used by downstream data

## Reviewer Checklist (Minimum)
- Structural validity confirmed
- Semantic fit to ontology patterns confirmed
- Evidence traceability confirmed
- Backward compatibility impact documented
- `make test` planned/passed before merge

## Merge Policy
A candidate can be merged only when:
1. Review status is updated from `proposed` to `accepted`
2. Ontology changes are applied in `src/ontology/broiler-production-ontology-edit.ttl`
3. Validation command succeeds (`sh ./run.sh make test` from `src/ontology`)
4. PR includes candidate artifact and review notes
