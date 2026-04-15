# Human Review Checklist (LLM-Assisted Curation)

Use this checklist for any PR that includes LLM-generated ontology candidates.

## 1) Candidate Intake
- [ ] Candidate file is attached in `curation/candidates/` (or linked in PR).
- [ ] Candidate conforms to `curation/candidate-schema.json`.
- [ ] Candidate references evidence with concrete relevance statements.
- [ ] Candidate has `review.status: proposed` before review.

## 2) Semantic Review
- [ ] Proposed entity type matches intended use (class/property/individual).
- [ ] Parent target is semantically appropriate.
- [ ] Labels and definitions are clear and domain-accurate.
- [ ] Axioms/restrictions do not conflict with current ontology patterns.
- [ ] Backward compatibility impact is explicitly documented.

## 3) Risk and Quality
- [ ] `qa.confidence` and `risk_level` are reasonable for evidence quality.
- [ ] High-risk changes have explicit reviewer escalation.
- [ ] Any breaking change includes migration/deprecation notes.

## 4) Implementation Review
- [ ] Ontology edits are made only in `src/ontology/broiler-production-ontology-edit.ttl`.
- [ ] No unintended edits to generated artifacts.
- [ ] Candidate decision status updated (`accepted` or `rejected`) with notes.

## 5) Validation Gate
- [ ] Local command executed: `cd src/ontology && sh ./run.sh make test`.
- [ ] CI QC workflow passed (`.github/workflows/qc.yml`).
- [ ] If docs changed, docs workflow passed (`.github/workflows/docs.yml`).

## 6) Merge Decision
- [ ] Reviewer name and decision date recorded.
- [ ] PR includes rationale for merge/reject outcome.
- [ ] Post-merge follow-up tasks (if any) are tracked.
