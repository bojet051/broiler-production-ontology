#!/usr/bin/env python3
"""Validate and apply LLM-assisted curation candidates.

This tool validates a candidate record against the repository schema and can
either preview or write a Turtle block into the editable ontology source.

Examples:
  python scripts/apply_candidate.py --check \
    src/ontology/broiler-production-ontology-edit.ttl \
    curation/candidate-example.yaml

  python scripts/apply_candidate.py --write \
    src/ontology/broiler-production-ontology-edit.ttl \
    curation/candidates/CAND-2026-002.yaml
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - handled in CI and setup docs
    raise SystemExit(
        "Missing dependency 'PyYAML'. Install with: python -m pip install -r requirements-curation.txt"
    ) from exc

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - handled in CI and setup docs
    raise SystemExit(
        "Missing dependency 'jsonschema'. Install with: python -m pip install -r requirements-curation.txt"
    ) from exc


ONT_BASE = "http://example.org/broiler-ontology#"


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def dump_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def load_candidate(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    raw = load_text(path)
    if suffix == ".json":
        data = json.loads(raw)
    else:
        data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError(f"Candidate file {path} did not parse to an object.")
    return data


def load_schema(path: Path) -> dict[str, Any]:
    data = json.loads(load_text(path))
    if not isinstance(data, dict):
        raise ValueError(f"Schema file {path} did not parse to an object.")
    return data


def validate_candidate(candidate: dict[str, Any], schema: dict[str, Any], candidate_path: Path) -> None:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(candidate), key=lambda err: list(err.path))
    if errors:
        message_lines = [f"Schema validation failed for {candidate_path}:"]
        for error in errors:
            location = "/".join(str(part) for part in error.path) or "<root>"
            message_lines.append(f"- {location}: {error.message}")
        raise ValueError("\n".join(message_lines))


def escape_turtle_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()


def iri_to_ref(value: str) -> str:
    if value.startswith(ONT_BASE):
        return ":" + value[len(ONT_BASE) :]
    if value.startswith("http://") or value.startswith("https://"):
        return f"<{value}>"
    return value


def title_label(value: str) -> str:
    return value.strip()


def candidate_block(candidate: dict[str, Any]) -> str:
    entity = candidate["entity"]
    qa = candidate.get("qa", {})
    review = candidate.get("review", {})
    source_context = candidate.get("source_context", {})
    evidence = candidate.get("evidence", [])
    axioms = candidate.get("axioms", [])

    local_name = entity["local_name"]
    label = title_label(entity["preferred_label"])
    definition = escape_turtle_string(entity["definition"])
    target_parent = entity.get("target_parent")
    entity_type = entity["entity_type"]
    iri = entity.get("proposed_iri") or f"{ONT_BASE}{local_name}"

    lines: list[str] = []
    lines.append(f"### Candidate {candidate['candidate_id']}")
    lines.append(f"# Status: {review.get('status', 'proposed')}")
    lines.append(
        f"# Source: {source_context.get('subdomain', 'unknown')} | {source_context.get('prompt_version', 'n/a')} | {source_context.get('generator', 'n/a')}"
    )
    lines.append(f"# IRI: {iri}")
    lines.append(
        f"# QA: confidence={qa.get('confidence', 'n/a')} risk={qa.get('risk_level', 'n/a')} consistency={qa.get('semantic_consistency_check', 'n/a')}"
    )
    lines.append("# Evidence:")
    for item in evidence:
        citation = item.get("citation", "")
        relevance = item.get("relevance_statement", "")
        lines.append(f"# - {citation}: {relevance}")
    if axioms:
        lines.append("# Candidate axioms:")
        for axiom in axioms:
            lines.append(
                f"# - {axiom.get('axiom_type', 'unknown')}: {axiom.get('expression_manchester', '')}"
            )

    subject = f":{local_name}"
    lines.append(f"{subject} rdf:type owl:{'Class' if entity_type == 'class' else 'ObjectProperty' if entity_type == 'object_property' else 'DatatypeProperty' if entity_type == 'datatype_property' else 'NamedIndividual'} ;")
    lines.append(f'    rdfs:label "{escape_turtle_string(label)}" ;')
    lines.append(f'    rdfs:comment "{definition}" ;')

    if entity_type == "class" and target_parent:
        lines.append(f"    rdfs:subClassOf {iri_to_ref(target_parent)} ;")
    elif entity_type in {"object_property", "datatype_property"} and target_parent:
        lines.append(f"    rdfs:subPropertyOf {iri_to_ref(target_parent)} ;")
    elif entity_type == "individual" and target_parent:
        lines.append(f"    rdf:type {iri_to_ref(target_parent)} ;")

    if entity.get("domain"):
        lines.append(f"    rdfs:domain {iri_to_ref(entity['domain'])} ;")
    if entity.get("range"):
        lines.append(f"    rdfs:range {iri_to_ref(entity['range'])} ;")
    if entity.get("inverse_of"):
        lines.append(f"    owl:inverseOf {iri_to_ref(entity['inverse_of'])} ;")

    if candidate.get("change_intent", {}).get("action") == "deprecate":
        lines.append("    owl:deprecated true ;")

    if entity.get("synonyms"):
        for synonym in entity["synonyms"]:
            lines.append(f'    rdfs:comment "Synonym: {escape_turtle_string(str(synonym))}" ;')

    if review.get("decision_notes"):
        lines.append(f'    rdfs:comment "Review notes: {escape_turtle_string(review["decision_notes"])}" ;')

    lines[-1] = lines[-1].removesuffix(" ;") + " ."
    return "\n".join(lines) + "\n"


def upsert_block(existing: str, candidate_id: str, block: str) -> str:
    marker = f"### Candidate {candidate_id}"
    idx = existing.find(marker)
    if idx >= 0:
        return existing[:idx].rstrip() + "\n\n" + block

    if existing and not existing.endswith("\n"):
        existing += "\n"
    if existing and not existing.endswith("\n\n"):
        existing += "\n"
    return existing + block


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--schema",
        default="curation/candidate-schema.json",
        help="Path to the candidate JSON Schema.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Validate only and do not modify files.")
    mode.add_argument("--write", action="store_true", help="Write the generated block into the ontology file.")
    parser.add_argument("ontology", help="Path to the editable ontology Turtle file.")
    parser.add_argument("candidates", nargs="+", help="Candidate YAML/JSON file(s).")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    schema_path = Path(args.schema)
    ontology_path = Path(args.ontology)
    candidate_paths = [Path(item) for item in args.candidates]

    schema = load_schema(schema_path)
    ontology_text = load_text(ontology_path) if ontology_path.exists() else ""

    for candidate_path in candidate_paths:
        candidate = load_candidate(candidate_path)
        validate_candidate(candidate, schema, candidate_path)
        block = candidate_block(candidate)

        if args.check:
            print(f"[ok] {candidate_path}")
            continue

        if args.write:
            ontology_text = upsert_block(ontology_text, candidate["candidate_id"], block)
            continue

        print(block, end="")

    if args.write:
        dump_text(ontology_path, ontology_text)
        print(f"Updated {ontology_path} with {len(candidate_paths)} candidate block(s).")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())