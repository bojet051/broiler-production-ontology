# Ontology Structure

## Classes

### Core Domain Classes

#### Broiler
The main entity representing an individual bird in industrial production.

**Properties:**
- `hasGender` (exactly 1) - Reference to Male or Female
- `hasCurrentPhase` (exactly 1) - Current production lifecycle phase
- `hasBreedLine` (some) - Breed assignment individuals
- `hasFeedBatch` (some) - Feed ration assignments
- `hasBroilerObservation` (some) - Observations about this broiler

#### Bird
Superclass for all avian entities.

#### BroilerBreed
Classification of broiler genetics and characteristics.
- Examples: Ross308, Cobb500, Hubbard

#### Gender
Biological sex classification.
- Individuals: Male, Female

#### ProductionLifecycle
Phases in broiler development.
- Individuals: BroodingPhase, GrowingPhase, PreProcessing

#### Infrastructure
Physical equipment and facilities.
- Examples: Brooder, Ventilation System, Feeder

#### Sensor
Monitoring devices that record observations.
- Examples: Temperature Sensor, Weight Scale

#### Observation
Abstract base class for all measurements and observations.

#### SensorObservation
Automated measurements from sensors.
- **Properties:**
  - `hasNumericValue` (exactly 1) - Measured value
  - `observedAt` (some) - TimeInstant
  - `observesCharacteristic` (some) - What was measured

#### ObservableCharacteristic
Measurable properties and traits.
- Examples: LiveWeightCharacteristic, TemperatureCharacteristic

#### TimeInstant
Specific point in time for temporal data.
- **Properties:**
  - `inXSDDateTime` (exactly 1) - ISO 8601 datetime

## Object Properties

### Broiler Relations
| Property | Domain | Range | Inverse | Comments |
|----------|--------|-------|---------|----------|
| hasGender | Broiler | Gender | isGenderOf | Exactly 1 |
| hasCurrentPhase | Broiler | ProductionLifecycle | isCurrentPhaseOf | Exactly 1 |
| hasBreedLine | Broiler | BroilerBreed | isBreedLineOf | Some |
| hasFeedBatch | Broiler | Feed | isFeedBatchOf | Some |
| hasBroilerObservation | Broiler | Observation | - | Some |

### Infrastructure Relations
| Property | Domain | Range | Inverse | Comments |
|----------|--------|-------|---------|----------|
| controls | Controller | Infrastructure | controlledBy | - |
| hasBiosecurityProtocol | Infrastructure | Biosecurity | isBiosecurityProtocolFor | - |
| managedBy | Infrastructure | Manager | managesInfrastructure | - |
| monitoredBy | Infrastructure | Sensor | monitors | - |

### Observation Relations
| Property | Domain | Range | Comments |
|----------|--------|-------|----------|
| observesCharacteristic | Observation | ObservableCharacteristic | What was measured |
| observedAt | Observation | TimeInstant | When it was measured |
| observedOnBroiler | Observation | Broiler | Which bird |
| observedInInfrastructure | Observation | Infrastructure | Where measured |
| observedBySensor | Observation | Sensor | How it was measured |

## Deprecated Properties

The following properties are maintained for backward compatibility but should not be used in new models:

- **hasBreed** (deprecated) → Use `hasBreedLine` instead
- **hasFeed** (deprecated) → Use `hasFeedBatch` instead
- **isBreedOf** (deprecated) → Use `isBreedLineOf` instead
- **isInPhase** (deprecated) → Use `hasCurrentPhase` instead

## Individuals

### Production Phases
- `:BroodingPhase` - Young bird rearing (0-7 days)
- `:GrowingPhase` - Growth and muscle development (8-40 days)
- `:PreProcessing` - Final preparation (40-47 days)

### Genders
- `:Male` - Male birds
- `:Female` - Female birds

### Observable Characteristics
- `:LiveWeightCharacteristic` - Body weight
- `:TemperatureCharacteristic` - Ambient temperature

## Design Patterns

### Individual-Based Modeling
Production phases and observable characteristics are modeled as **named individuals**, not classes. This allows:
- Direct reference to specific phases in broiler observations
- Consistent terminology across the ontology
- Easier data integration

### Cardinality Constraints
Strategic use of cardinality constraints ensures:
- Each broiler has exactly 1 current phase
- Each broiler has exactly 1 gender
- Each observation has exactly 1 numeric value
- Each time instant has exactly 1 datetime

### Inverse Properties
Inverse properties are defined for bidirectional queries:
```sparql
# Find all broilers of a given gender
?broiler :hasGender ?gender .
# Same result, inverse direction
?gender :isGenderOf ?broiler .
```

## Modular Design

The ontology supports imports for domain-specific modules:
- **Genetics module** - Breed definitions and genetic traits
- **Health module** - Diseases, treatments, preventive protocols
- **Economics module** - Cost factors, productivity metrics

*(Currently available as examples; extend as needed)*

## Version Management

- **Ontology IRI**: http://example.org/broiler-ontology
- **Version IRI**: http://example.org/broiler-ontology/1.0
- **Format**: OWL 2 DL
- **Source Format**: Turtle (RDF/Turtle serialization)

For version history, see [Release Notes](releases.md).
