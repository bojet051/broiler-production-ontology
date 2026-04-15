# Contributing

Thank you for your interest in contributing to the Industrial Broiler Production Ontology!

## How to Contribute

### Reporting Issues
Found a bug or have a suggestion?

1. Check [existing issues](https://github.com/bojet051/broiler-production-ontology/issues) first
2. [Create a new issue](https://github.com/bojet051/broiler-production-ontology/issues/new) with:
   - Clear title and description
   - Steps to reproduce (if applicable)
   - Expected vs actual behavior

### Submitting Changes

#### For Small Changes
1. Fork the repository
2. Create a branch: `git checkout -b fix/issue-description`
3. Make changes to `src/ontology/broiler-production-ontology-edit.ttl`
4. Test locally (see [Development](development.md))
5. Commit with clear message: `git commit -m "Fix: [description]"`
6. Push and open a Pull Request

#### For Major Changes
1. Open an issue first to discuss the proposed changes
2. Get feedback from maintainers
3. Submit a detailed PR with:
   - Clear description of changes
   - Motivation and context
   - Test results

### Code Style & Conventions

#### Turtle Formatting
```turtle
# Use consistent indentation (spaces, not tabs)
@prefix : <http://example.org/broiler-ontology#> .

:ClassName a owl:Class ;
  rdfs:label "Class Name" ;
  rdfs:comment "Detailed description of the class." ;
  rdfs:subClassOf :ParentClass .

# Align properties for readability
:property1 rdfs:domain :ClassA ;
           rdfs:range :ClassB ;
           rdfs:comment "Property description." .
```

#### Naming Conventions
- **Classes**: CamelCase (e.g., `BroilerBreed`, `SensorObservation`)
- **Properties**: camelCase (e.g., `hasGender`, `observedAt`)
- **Individuals**: CamelCase with underscores (e.g., `BroodingPhase`, `Ross308_Assignment_001`)

#### Documentation
- Add `rdfs:label` to all classes and properties (English)
- Add `rdfs:comment` with clear, concise descriptions
- Include usage examples in comments when helpful

```turtle
:hasGender a owl:ObjectProperty ;
  rdfs:label "has gender" ;
  rdfs:comment "Relates a broiler to its biological sex (Male or Female). Each broiler has exactly one gender." ;
  rdfs:domain :Broiler ;
  rdfs:range :Gender .
```

### Testing Your Changes

Before submitting:

1. **Run validation tests**
   ```bash
   cd src/ontology
   sh ./run.sh make test
   ```

2. **Build release artifacts**
   ```bash
   sh ./run.sh make prepare_release
   ```

3. **Check output**
   - Verify no errors in test output
   - Confirm release files build successfully
   - Review QC reports in `reports/`

4. **Test with external tools** (optional)
   - Load into Protégé
   - Verify with SPARQL queries
   - Check reasoner output

### Pull Request Process

1. **Update documentation** if adding new concepts
   - Update [Ontology Structure](ontology-structure.md)
   - Add examples to [Getting Started](getting-started.md)

2. **Reference issues** in your PR description
   - Link related issues: `Fixes #123`
   - Explain the connection

3. **Provide context**
   - Why is this change needed?
   - What problem does it solve?
   - How does it align with ontology goals?

4. **Wait for review**
   - Maintainers will review your changes
   - Be responsive to feedback
   - Make requested changes in separate commits

5. **Merge**
   - Squash commits if requested
   - Merge to main
   - Your change will be included in the next release

### Documentation Contributions

Help improve documentation!

- Fix typos and unclear sections
- Add examples and use cases
- Improve explanations
- Translate documentation

Documentation changes:
- Edit `.md` files in `docs/` directory
- Check formatting in Markdown
- Test locally with `mkdocs serve` (if available)

### Design Discussions

For major design decisions:

1. Open a Discussion on GitHub
2. Explain the proposed change and rationale
3. Propose multiple solutions if applicable
4. Gather feedback from the community

## Development Setup

See [Development](development.md) for:
- Local environment setup
- Building and testing
- Common troubleshooting

## Legal

By contributing, you agree that:
- Your contributions can be used under the project's license
- You have the right to contribute
- Your work is original or properly attributed

## Questions?

- Open a GitHub issue with the `question` label
- Check [existing discussions](https://github.com/bojet051/broiler-production-ontology/discussions)
- Review [Ontology Structure](ontology-structure.md)

---

Thank you for helping improve the Broiler Production Ontology! 🎉
