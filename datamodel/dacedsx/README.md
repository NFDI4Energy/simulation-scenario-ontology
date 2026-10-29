# DaceDSX Framework

**Repository**: https://github.com/cs7org/DaceDSX
**Documentation**: https://zenodo.org/records/15064826
**Language**: Java, C++, Python
**License**: MIT / Apache 2.0

DaceDSX is a data-centric distributed simulation framework that enables loose coupling between simulation tools using Apache Kafka for all communication.

## Overview

DaceDSX focuses on data and loose couplings via a topic-based publish/subscribe paradigm on top of Apache Kafka. It supports multiple simulation domains (power systems, traffic, etc.) and automatically handles data translation between different simulation layers and domains.

## Key Concepts

### Simulation Configuration

The simulation is defined as a JSON scenario file:

```json
{
  "scenarioID": "unique_scenario_id",
  "domainReferences": {},
  "simulationStart": "2023-01-01T00:00:00",
  "simulationEnd": "2023-01-01T01:00:00",
  "execution": {
    "randomSeed": 42,
    "constraints": [],
    "priority": 1,
    "syncedParticipants": 2
  },
  "buildingBlocks": [...],
  "translators": [...],
  "projectors": [...]
}
```

### Simulation Component (Building Block)

Building blocks represent simulator instances. 

```json
{
  "buildingBlocks": [
    {
      "instanceID": "unique_instance_id",
      "type": "SumoWrapper",
      "layer": "Traffic",
      "domain": "transportation",
      "stepLength": 1000,
      "parameters": {"configFile": "sumo_config.sumocfg"},
      "resources": {"netFile": "network.net.xml"},
      "results": {"outputFormat": "csv"},
      "synchronized": true,
      "isExternal": false,
      "responsibilities": ["bus_1", "bus_2", "street_a"],
      "observers": [
        {
          "task": "publish",
          "element": "Vehicle",
          "filter": ["bus_1", "bus_2"],
          "period": 1000,
          "type": "kafka"
        }
      ]
    }
  ]
}
```

You can have **multiple building blocks with the same `type`** (i.e. running the same wrapper), but their `responsibilities` should be **distinct** so that each block is responsible for a different set of model components.

### Simulation Model

The simulation model corresponds to the `type` field of a building block, i.e. the wrapper name (e.g. `SumoWrapper`, `PyPSAWrapper`, `pandapowerWrapper`). Multiple building blocks can run the **same** model (`type`), but with **distinct** `responsibilities`.

```json
{
  "buildingBlocks": [
    {
      "instanceID": "sumo_1",
      "type": "SumoWrapper",
      "layer": "Traffic"
    },
    {
      "instanceID": "sumo_2",
      "type": "SumoWrapper",
      "layer": "Traffic"
    }
  ]
}
```

### Model Component

Model components handled by a building block are listed in the `responsibilities` array (e.g. busses, streets, loads):

```json
"responsibilities": ["bus_1", "bus_2", "street_a"]
```

Each building block is responsible for a distinct set of model components; `responsibilities` of different blocks with the same `type` should not overlap.

### Simulation Connection Ports

Connection ports map to the **publisher/subscriber** mechanism, which is **rather implicit** (topics are not mentioned explicitly in the scenario file). An **`observer`** can be regarded as such a port, since it is often used to publish information about specific model components:

```json
"observers": [
  {
    "task": "publish",           // or "subscribe"
    "element": "Vehicle",
    "filter": ["bus_1", "bus_2"],
    "period": 1000,
    "trigger": "time_step",
    "type": "kafka"
  }
]
```

### Simulation Connection

Communication is via Kafka topics:
- **Same layer/domain**: Building blocks share topics directly
- **Different layers**: `Translators` handle data conversion
- **Different domains**: `Projectors` handle cross-domain translation

**Translator** (same domain, different layers):
```json
{
  "translators": [{
    "translatorID": "translator_1",
    "type": "PowerTrafficTranslator",
    "domain": "energy",
    "layerA": "distribution",
    "responsibilitiesA": ["substation_1"],
    "layerB": "transmission",
    "responsibilitiesB": ["bus_1"],
    "resources": {},
    "parameters": {}
  }]
}
```

**Projector** (different domains):
```json
{
  "projectors": [{
    "projectorID": "projector_1",
    "type": "TrafficToPowerProjector",
    "domainA": "transportation",
    "domainB": "energy",
    "responsibilitiesA": ["street_1"],
    "responsibilitiesB": ["load_1"],
    "parameters": {}
  }]
}
```

### Message Schema (Avro)

DaceDSX uses Apache Avro for message serialization. The message schema is defined as an Avro schema and used with a schema registry to validate the messages before they are published on topics. The schemas are only referenced explicitly in the wrapper currently.

Example (Battery):
```json
{
  "namespace": "eu.fau.cs7.daceDS.datamodel",
  "type": "record",
  "name": "Battery",
  "fields": [
    {"name": "power", "type": "float"},
    {"name": "current", "type": "float"},
    {"name": "voltage", "type": "float"},
    {"name": "soc", "type": "float"}
  ]
}
```

Other Avro schemas that exist in the repository:
- `PowerSystem.avsc` - Power system topology
- `bus.avsc` - Bus component data
- `SyncMsg.avsc` - Synchronization messages
- `SubMicro_flat.avsc` - Sub-micro grid data

### Message Attribute

A message attribute is a **field within the message schema** that has been filled out. For example, in the `Battery` schema above, the attributes are `power`, `current`, `voltage`, and `soc`, each with its own `name` and `type`.

### Message Modification

`Translators` and `Projectors` modify messages during runtime:
- Format conversion between Avro schemas
- Unit conversion
- Data aggregation/disaggregation

They modify the messages and publish them on a **different topic** (or between layers/domains) at runtime, so from an ontology perspective both map to the **Message Modification** concept.

### Simulation Parameters

- `scenarioID`: Unique identifier for the scenario
- `domainReferences`: References to the domains involved in the simulation (currently not regarded by the framework)
- `simulationStart`: ISO datetime string
- `simulationEnd`: ISO datetime string
- `execution.randomSeed`: Random seed for reproducibility
- `execution.constraints`: (rarely used) additional constraints
- `execution.priority`: Scheduling priority (when simulations run in parallel)
- `execution.syncedParticipants`: Number of blocks to synchronize

### Simulation Component Parameters

The component (building block) parameters are the fields of the building block object:

- `instanceID`: Unique identifier for this instance
- `type`: Name of the wrapper that will be run
- `layer`: Name of the layer in the domain model
- `domain`: Name of the domain (model)
- `stepLength`: Simulation step size
- `parameters`: Wrapper-specific configuration (e.g. `configFile`)
- `resources`: Input files or data sources
- `results`: Output configuration
- `synchronized`: Whether this block requires synchronization
- `isExternal`: Whether running on another machine
- `responsibilities`: Model components handled by this block
