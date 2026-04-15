# Release Notes

## Version 1.0 (Current)

**Release Date:** April 15, 2026

### Overview
Initial release of the Industrial Broiler Production Ontology, successfully migrated to the Ontology Development Kit (ODK) framework.

### Features
- ✅ Core classes for broiler production domain
- ✅ Comprehensive object and datatype properties
- ✅ Individual-based modeling for production phases and characteristics
- ✅ Cardinality constraints for data consistency
- ✅ Backward-compatible deprecated properties
- ✅ Multi-format releases (OWL, Turtle)
- ✅ Automated validation and QC checks
- ✅ GitHub Actions CI/CD pipeline
- ✅ Comprehensive documentation

### Classes
- **Broiler** - Main entity representing individual birds
- **Bird** - Superclass for avian entities
- **BroilerBreed** - Genetic classifications
- **Gender** - Binary sex classification
- **ProductionLifecycle** - Production phases
- **Infrastructure** - Facilities and equipment
- **Sensor** - Monitoring devices
- **Observation** - Measurement records
- **SensorObservation** - Automated sensor readings
- **ObservableCharacteristic** - Measurable properties
- **TimeInstant** - Temporal annotations
- And 8+ domain-specific classes

### Object Properties
- 30+ properties with inverse relations
- Cardinality constraints on critical properties
- Clear domain and range specifications
- Inverse properties for bidirectional queries

### Individuals
- **BroodingPhase**, **GrowingPhase**, **PreProcessing** - Production phases
- **Male**, **Female** - Gender classifications
- **LiveWeightCharacteristic**, **TemperatureCharacteristic** - Observable traits

### Validation
- ✅ OWL 2 DL profile compliance
- ✅ ELK reasoner consistency check
- ✅ SPARQL QC checks (4 validation rules)
- ✅ All tests PASSED with 0 violations

### Documentation
- Getting Started guide
- Ontology structure reference
- Development workflow guide
- Contributing guidelines
- This release notes document

### Known Limitations
- IRI namespace uses example.org (can be updated to production IRI when ready)
- No module imports configured yet (available for future extension)
- Genetics, health, and economics modules are design sketches

### Backward Compatibility
Deprecated properties maintained for legacy data support:
- `hasBreed` → Use `hasBreedLine`
- `hasFeed` → Use `hasFeedBatch`
- `isBreedOf` → Use `isBreedLineOf`
- `isInPhase` → Use `hasCurrentPhase`

### File Formats

| Format | File | Status |
|--------|------|--------|
| OWL | `broiler-production-ontology.owl` | ✅ Released |
| Turtle | `broiler-production-ontology.ttl` | ✅ Released |
| OWL (Full) | `broiler-production-ontology-full.owl` | ✅ Released |
| Turtle (Full) | `broiler-production-ontology-full.ttl` | ✅ Released |

### Platform Support
- ✅ Protégé 5.x
- ✅ OWL Tools
- ✅ RDF/Turtle parsers (rdflib, Jena, etc.)
- ✅ SPARQL Query Endpoints
- ✅ Web-based ontology browsers

### Migration Notes

This release represents the successful migration of the standalone Broiler Production ontology into the ODK framework:

1. **Before:** Standalone Turtle file with manual validation
2. **After:** ODK-managed project with:
   - Automated build pipeline
   - Integrated QC framework
   - GitHub Actions CI/CD
   - Professional documentation

See `ODK_IMPLEMENTATION_GUIDE.md` for detailed migration steps.

### Next Steps

Planned for future releases:

- **v1.1** - Add genetics module with breed-specific traits
- **v1.2** - Health and disease management module
- **v1.3** - Economics and productivity metrics
- **v2.0** - Extended namespace (purl.obolibrary.org IRI)
- **v2.1** - Full OBO Library compliance

### How to Cite

If you use this ontology in your research, please cite:

```bibtex
@ontology{IBPO2026,
  title={Industrial Broiler Production Ontology},
  author={bojet051},
  year={2026},
  url={https://github.com/bojet051/broiler-production-ontology}
}
```

### Contributors

- **bojet051** - Primary developer and maintainer

### Support

- **Issues:** https://github.com/bojet051/broiler-production-ontology/issues
- **Discussions:** https://github.com/bojet051/broiler-production-ontology/discussions
- **Documentation:** [See docs/](../docs/)

### License

[Specify your license here - e.g., CC BY 4.0, MIT, Apache 2.0]

---

**Thank you for using the Industrial Broiler Production Ontology!**

For questions or feedback, please open an issue on GitHub.
