# User Prompt Template — Candidate Generation

Use this text as the *user* message when calling an LLM for candidate generation. Paste the contents of `curation/prompts/system-prompt.md` into the system message, then paste the block below into the user/message box (replace the PDF excerpt placeholder with your selected 1–3 paragraphs).

Context: subdomain=lifecycle
Examples: BroodingPhase (http://example.org/broiler-ontology#BroodingPhase), GrowingPhase (http://example.org/broiler-ontology#GrowingPhase)

PDF excerpt:
[PASTE THE 1–3 PARAGRAPHS HERE]

Task:
- Propose exactly ONE candidate for the broiler ontology (class, property, or individual) grounded in the excerpt.
- Output EXACTLY one YAML document that conforms to `curation/candidate-schema.json`.
- Required fields: `candidate_id` (CAND-YYYY-NNN), `created_at` (ISO datetime), `source_context` (include `subdomain` and `generator`), `entity` (include `entity_type`, `local_name`, `proposed_iri` using prefix `http://example.org/broiler-ontology#`), `preferred_label`, `definition`, `evidence` (at least one item with `citation` and `relevance_statement`), and `review.status: proposed`.
- Do NOT include any explanation, extra text, or YAML comments — output only the YAML document.

Notes:
- Keep the excerpt short (1–3 paragraphs) to keep the LLM focused.
- Use one of the example terms above to demonstrate the naming/IRI pattern.
- If the LLM outputs extra text, ask it again with: "Output only the YAML document, no commentary." 

Save the model output as `curation/candidates/CAND-YYYY-NNN.yaml` and then run validation:

```bash
./.venv/bin/python scripts/apply_candidate.py --check \
  src/ontology/broiler-production-ontology-edit.ttl \
  curation/candidates/CAND-YYYY-NNN.yaml
```

If validation succeeds, run the self-check prompt (see `curation/prompts/self-check-prompt.md`) and attach the self-check output to the candidate record under `evidence` or `self_check`.
