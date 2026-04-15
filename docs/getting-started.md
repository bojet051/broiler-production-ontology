# Getting Started

## Installation

The ontology is available in multiple formats:

- **OWL Format**: `broiler-production-ontology.owl`, `broiler-production-ontology-full.owl`
- **Turtle Format**: `broiler-production-ontology.ttl`, `broiler-production-ontology-full.ttl`

### Using the Ontology

**With Protégé:**
1. Download the ontology file (OWL or RDF/Turtle)
2. Open in [Protégé](https://protege.stanford.edu/)
3. Explore classes, properties, and individuals

**With Code:**
```python
from rdflib import Graph

# Load the ontology
g = Graph()
g.parse("broiler-production-ontology.ttl", format="turtle")

# Query classes
classes = g.subjects(predicate=RDF.type, object=OWL.Class)
for cls in classes:
    print(cls)
```

## Core Concepts

### Production Phases
- **BroodingPhase** - Young bird rearing (0-7 days)
- **GrowingPhase** - Growth and development (8-40 days)
- **PreProcessing** - Final stages before processing

### Broiler Properties
Each broiler has:
- `hasGender` (exactly 1) - Male or Female
- `hasCurrentPhase` (exactly 1) - Current production phase
- `hasBreedLine` (some) - Assigned breed (e.g., Ross308)
- `hasFeedBatch` (some) - Assigned feed rations
- `hasBroilerObservation` (some) - Health and performance measurements

### Observable Characteristics
- **LiveWeightCharacteristic** - Body weight measurements
- **TemperatureCharacteristic** - Ambient temperature readings
- **Custom characteristics** - Extensible for domain-specific measures

## Examples

### Creating a Broiler Individual
```turtle
@prefix : <http://example.org/broiler-ontology#> .

:Broiler_001 a :Broiler ;
  :hasGender :Male ;
  :hasCurrentPhase :GrowingPhase ;
  :hasBreedLine :Ross308_Assignment_001 ;
  :hasFeedBatch :FeedRation_GrowerPhase_001 .
```

### Recording an Observation
```turtle
:Observation_Weight_001 a :SensorObservation ;
  :observedAt :TimeInstant_2024_01_15_10_30 ;
  :observesCharacteristic :LiveWeightCharacteristic ;
  :observedOnBroiler :Broiler_001 ;
  :hasNumericValue "2.5"^^xsd:decimal .
```

## Next Steps

- Explore the [Ontology Structure](ontology-structure.md)
- See [Development](development.md) for building and validating changes
- Review [Contributing](contributing.md) to help improve the ontology
