# Broiler ODK Migration Notes

## Source ontology assessment
- Ontology IRI: http://example.org/broiler-ontology
- Version IRI: http://example.org/broiler-ontology/1.0
- Base / prefix: http://example.org/broiler-ontology#
- Canonical source file: Broiler Production.ttl

## Migration-critical patterns to preserve
- Deprecated legacy object properties remain backward-compatibility only:
  - hasBreed
  - hasFeed
  - isBreedOf
  - isInPhase
- Core class restrictions to preserve:
  - Broiler hasBreedLine some BroilerBreed
  - Broiler hasCurrentPhase exactly 1 ProductionLifecycle
  - Broiler hasFeedBatch some Feed
  - Broiler hasGender exactly 1 Gender
- Observation model to preserve:
  - Observation observesCharacteristic some ObservableCharacteristic
  - Observation observedAt some TimeInstant
  - SensorObservation hasNumericValue exactly 1
  - TimeInstant inXSDDateTime exactly 1
- Individual-based modeling to preserve:
  - BroodingPhase, GrowingPhase, PreProcessing
  - Male, Female
  - LiveWeightCharacteristic, TemperatureCharacteristic

## Provisional repository decisions
- GitHub owner: elyjunpates
- Repository name: broiler-production-ontology
- Default branch: main
- Primary release artifact: full
- Source strategy: keep the current Turtle as the canonical reference during migration, then copy it into the ODK source layout once scaffold generation is stable

## Recommended next steps
1. Bootstrap the ODK scaffold with the provisional repository values.
2. Move the Turtle content into the seeded source layout.
3. Run ROBOT validation and release generation locally.
4. Fix any ontology header or modeling issues before pushing.
5. Only then consider ROBOT templates for repetitive branches.
