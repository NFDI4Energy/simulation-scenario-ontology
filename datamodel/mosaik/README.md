# mosaik Framework

**Website**: https://mosaik.offis.de/
**Documentation**: https://mosaik.readthedocs.io/
**GitLab**: https://gitlab.com/mosaik
**Language**: Python

mosaik is a flexible smart-grid co-simulation framework developed by OFFIS that allows combining existing simulation models into large-scale scenarios with thousands of entities.

mosaik 3 uses a Python API for scenario definition. 
Currently, mosaik 4 is in development and will provide also a declarative JSON-LD format for serialization.

## Key Concepts

The alignment of the Python scenario API and the new data model are shown in the following.
The ontology term is used as headline with the mosaik term in brackets.

### Simulation Configuration (Scenario)

#### Scenario API

The whole Python file including the parts described in the rest of the document.

```python
SIM_CONFIG = {
    "OEP": {
        "python": "mosaik_components.oep:OEPSimulator",
    },
}
```

#### Datamodel

The whole scenario is a `Scenario` object that aggregates the simulators, tesserae, connections and parameters:

```json
{
  "$type": "Scenario",
  "simulators": {…},
  "tesserae": {…},
  "connections": {…},
  "params": {…}
}
```

### Simulation Component (Simulator)

#### Scenario API

Simulators are started via `world.start()`:

```python
oep_sim_2 = world.start(
    "OEP",
    step_size=3600,
    dataset="iai_active_power_pv_202303",
    datetime_column="datetime",
    index_column="id",
)
```

#### Datamodel

A `Simulator` is configured by its starter, init parameters and a plugin name:

```json
"simulators": {
  "pandapower": {
    "$type": "Simulator",
    "starter": "mosaik_components.pandapower:Simulator",
    "init_params": {
      "step_size": 900
    },
    "plugin_name": "pandapower"
  }
}
```

### Simulation Model

#### Scenario API

Each simulator declares the models it can provide in its `META` (`META.models`). A single simulator can provide different models, and multiple instances of a model can be created:

```python
META = {
    "type": "hybrid",
    "models": {
        "PV": {...},
        "Grid": {...},
    },
}
```

#### Datamodel

The models available to a simulator are **not explicitly represented** in the datamodel — they are part of the simulator implementation (referenced via `plugin_name`), and instances are created through the `entity_sources` of a `Tessera`.

### Model Component (Entity)

#### Scenario API

Entities are created from the simulator's models. There can be multiple instances of a model, and a simulator can provide different models:

```python
pv_data_2 = oep_sim_2.OEPDataSource()
```

#### Datamodel

Entities are grouped into a **Tessera** — a grouping concept for visualization that contains multiple entities of the same model. A Tessera can be just one instance (`num: 1`):

```json
"tesserae": {
  "grid": {
    "$type": "Tessera",
    "simulator": "pandapower",
    "model": "Grid",
    "entity_sources": {
      "grid-source": {
        "$type": "CreateSource",
        "num": 1,
        "params": {"network_function": "example_simple"}
      }
    }
  }
}
```

### Simulation Connection Port

#### Scenario API

Connection ports are **implicit** in mosaik. They are defined by the `META` of each simulator, which lists the potential in- and outputs of its models (classified as `non-trigger`, `trigger`, `persistent` and `non-persistent` attributes). This META is part of the simulator implementation and is only accessed from within the simulation scenario.

The META is **created dynamically** for some simulators (e.g., mosaik-csv builds it based on the columns of the CSV file):

```python
META = {
    "type": "hybrid",
    "models": {
        "PV": {
            "public": True,
            "params": ["efficiency", "area"],
            "non-trigger": ["DNI[W/m2]"],
            "trigger": ["max_power[MW]"],
            "persistent": ["P[MW]"],
            "non-persistent": [],
        },
    },
}
```

#### Datamodel

Connection ports are **not explicitly represented** in the datamodel. As in the scenario API, they are implicit, being defined by the simulator's `META` and referenced indirectly through the `attr_pairs` of a `Connection`.

### Simulation Connection

#### Scenario API

Connections are established between entities:

```python
world.connect(pv_data_2, load, ("power_kw", "P"))
```

#### Datamodel

A `Connection` is defined by its source and destination tesserae, the attribute pairs, a relation type and settings:

```json
{
  "connections": {
    "conn_pv": {
      "$type": "Connection",
      "source": "pvs",
      "dest": "buses",
      "attr_pairs": [["P[MW]", "P_gen[MW]"]],
      "relation": {"$type": "OneToOneRelation"},
      "settings": {"time_shifted": false}
    }
  }
}
```

### Message Schema

#### Scenario API

The message schema itself is **not directly defined** in the scenario, but is automatically derived by mosaik based on the connections defined via `world.connect()` calls.

#### Datamodel

Message schemas are **not explicitly represented** in the datamodel. They are automatically derived by mosaik from the `attr_pairs` of the defined `Connection` objects.

### Message Attribute

#### Scenario API

An individual message attribute maps to an **attribute tuple** `(src_attr, dest_attr)` of strings used in a `world.connect()` call.

#### Datamodel

An individual message attribute corresponds to one attribute pair `(src_attr, dest_attr)` in the `attr_pairs` list of a `Connection`.

### Message Modification

#### Scenario API

Transform functions can modify data during transfer:

```python
world.connect(pv_data_2, load, ("power_kw", "P"), transform=my_transform_func)
```

#### Datamodel

Message modifications are not yet explicitly represented in the datamodel.

### Simulation Parameters

#### Scenario API

Runtime parameters such as the simulation end time are passed to `world.run()`:

```python
world.run(until=3600)
```

#### Datamodel

The scenario parameters are stored in the `params` object of the `Scenario`:

```json
{
  "$type": "Scenario",
  "params": {
    "$type": "ScenarioParams",
    "until": 3600,
    "rt_mode": false,
    "rt_factor": 1.0,
    "rt_strict": false,
    "print_progress": true,
    "lazy_stepping": true
  }
}
```

### Simulation Component Parameters

#### Scenario API

Component parameters are passed via `world.start()`:

```python
oep_sim_2 = world.start(
    "OEP",
    step_size=3600,
    dataset="iai_active_power_pv_202303",
    datetime_column="datetime",
    index_column="id",
)
```

#### Datamodel

They are stored as the `init_params` of the respective `Simulator`:

```json
{
  "$type": "Scenario",
  "simulators": {
    "PV": {
      "$type": "Simulator",
      "init_params": {
        "step_size": 900,
        "start_date": "2014-03-17 13:13:13"
      }
    }
  }
}
```

## OEO Alignment

See the LinkML schema [`mosaik_scenario.yaml`](./mosaik_scenario.yaml)
for the authoritative OEO term mappings (`class_uri`/`slot_uri`), and the
OEO alignment analysis and current implementation status in the [framework comparison](../README.md#oeo-alignment).
