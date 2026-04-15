# Development

## Local Setup

### Prerequisites
- Docker (for ODK build system)
- Git
- Turtle/RDF-aware editor (optional: Protégé)

### Clone the Repository
```bash
git clone https://github.com/bojet051/broiler-production-ontology.git
cd broiler-production-ontology
```

## Building the Ontology

### Run Tests
```bash
cd src/ontology
sh ./run.sh make test
```

This runs:
- **Reasoning test** - ELK reasoner checks logical consistency
- **SPARQL QC checks** - Validates against known anti-patterns
- **OWL 2 DL Profile validation** - Ensures OWL compliance

### Build Release Artifacts
```bash
cd src/ontology
sh ./run.sh make prepare_release
```

Output files:
- `broiler-production-ontology.owl` - Reasoned OWL format
- `broiler-production-ontology.ttl` - Turtle format
- `broiler-production-ontology-full.owl` - Full with imports
- `broiler-production-ontology-full.ttl` - Full Turtle
- `reports/` - QC and statistical reports

## Editing the Ontology

### Edit Source File
The editable ontology source is:
```
src/ontology/broiler-production-ontology-edit.ttl
```

### File Format
- **Format**: Turtle (RDF/Turtle serialization)
- **Character Encoding**: UTF-8
- **Line Endings**: Unix (LF)

### Namespace Prefixes
Always use established prefixes:
```turtle
@prefix : <http://example.org/broiler-ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
```

### Adding a New Class
```turtle
:NewClass a owl:Class ;
  rdfs:label "New Class Label" ;
  rdfs:comment "Description of the class purpose and usage." ;
  rdfs:subClassOf :ParentClass .
```

### Adding a New Property
```turtle
:newProperty a owl:ObjectProperty ;
  rdfs:label "new property" ;
  rdfs:comment "Description of the property." ;
  rdfs:domain :DomainClass ;
  rdfs:range :RangeClass ;
  owl:inverseOf :inverseProperty .
```

### Adding Restrictions
```turtle
:Broiler rdfs:subClassOf [
  a owl:Restriction ;
  owl:onProperty :hasGender ;
  owl:cardinality "1"^^xsd:integer
] .
```

## Validation Rules

### SPARQL QC Checks
The following quality checks are automatically applied:

| Check | Description | Consequence |
|-------|-------------|-------------|
| `owldef-self-reference` | Classes shouldn't have circular definitions | FAIL test |
| `iri-range` | IRIs should not be in range positions | Advisory |
| `label-with-iri` | Labels shouldn't contain IRIs | Advisory |
| `multiple-replaced_by` | Avoid duplicate `replacedBy` annotations | Warning |

### Common Issues & Fixes

**Issue:** Test fails on reasoning
```
ERROR: Unsatisfiable class detected
```
**Fix:** Check for conflicting cardinality constraints or circular subclass relationships

**Issue:** SPARQL QC violations
```
WARN: missing_definition for [class]
```
**Fix:** Add rdfs:label and rdfs:comment to all classes/properties

## Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/add-new-concept
   ```

2. **Edit the ontology**
   ```bash
   # Edit in your preferred editor
   nano src/ontology/broiler-production-ontology-edit.ttl
   ```

3. **Test locally**
   ```bash
   cd src/ontology
   sh ./run.sh make test
   ```

4. **Fix any QC violations**
   - Review test output
   - Update ontology
   - Rerun tests

5. **Commit changes**
   ```bash
   git add src/ontology/broiler-production-ontology-edit.ttl
   git commit -m "Add new concept: [description]"
   ```

6. **Build release**
   ```bash
   cd src/ontology
   sh ./run.sh make prepare_release
   ```

7. **Push and create PR**
   ```bash
   git push origin feature/add-new-concept
   # Open PR on GitHub
   ```

8. **Merge and release**
   - GitHub Actions automatically runs QC
   - Upon merge to main, docs are updated
   - Tag releases on GitHub

## Troubleshooting

### Docker Not Running
```
ERROR: Cannot connect to Docker daemon
```
**Solution:** Start Docker Desktop, then retry

### Make Target Not Found
```
ERROR: No rule to make target 'test'
```
**Solution:** Ensure you're in `src/ontology/` directory

### Reasoning Timeout
```
TIMEOUT: Reasoning did not complete in time
```
**Solution:** Reduce reasoning scope or check for circular definitions

## Advanced Tasks

### Updating ODK Version
```bash
cd broiler_odk_bootstrap
sh seed-via-docker.sh -c -C broiler-odk.yaml
# Review generated changes
cd ..
git diff
git add -p  # Stage relevant changes
git commit -m "Update ODK to latest version"
```

### Custom SPARQL Queries
Add new QC rules in `src/sparql/`:
```sparql
# custom-check.sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?entity WHERE {
  # Your SPARQL pattern here
}
```

### Extending with Modules
Create modular sub-ontologies:
```turtle
# src/ontology/modules/genetics.ttl
@prefix genetics: <http://example.org/broiler-ontology/genetics#> .

:Broiler owl:imports <http://example.org/broiler-ontology/genetics> .
```

## Resources

- [ODK Documentation](https://github.com/INCATools/ontology-development-kit)
- [OWL 2 Specification](https://www.w3.org/TR/owl2-overview/)
- [SPARQL Query Language](https://www.w3.org/TR/sparql11-query/)
- [Protégé Ontology Editor](https://protege.stanford.edu/)
