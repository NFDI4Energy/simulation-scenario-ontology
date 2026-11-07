# OEO Simulation Scenario Datamodel

Every co-simulation framework describes its simulation scenarios in its own way — mosaik uses a
Python API, DaceDSX a JSON scenario file, VILLAS a set of configuration files. To standardize
scenario definition across frameworks, this repository collects both the **datamodel** that
describes these scenarios in terms of the Open Energy Ontology (OEO), and the
**per-framework documentation** that explains how each framework expresses the same concepts.

This README therefore serves two purposes: it tells you how to work with the LinkML datamodel and
where everything lives, and it presents the framework comparison and OEO alignment that drive the
ontology development. 

## Use LinkML

The datamodel is written in [LinkML](https://linkml.io/). Execute the following commands in the
datamodel directory with installed [uv](https://docs.astral.sh/uv/getting-started/installation/).

Validate oeo_scenario: ``uv run linkml validate oeo_scenario.yaml``

Create UML diagram: ``uv run gen-plantuml -d export/UML -f svg oeo_scenario.yaml``

Generate many different formats from LinkML data model into directory ``export``:

``uv run linkml generate project .\oeo_scenario.yaml -d export``

Framework-specific schema extensions live in their own subdirectory.
Each co-simulation framework has its own subdirectory, which collects the datamodel schemas and the 
framework-specific documentation and examples. 

## Co-Simulation Framework Comparison

To build a datamodel that covers all three frameworks, we first need a detailed look at how each
one expresses the same scenario concepts. The table below gives an overview of the frameworks; the
detailed per-framework descriptions follow in each framework's own subdirectory.

| Framework | Language  | Primary Use Case                                           | License |
|-----------|-----------|------------------------------------------------------------|---------|
| [mosaik](mosaik/README.md) | Python    | Time-stepped and event-based co-simulation for smart grids | LGPL-2.1 |
| [DaceDSX](dacedsx/README.md) | Java, C++, Python | Distributed, loosely-coupled simulation via Kafka          | MIT/Apache 2.0 |
| [VILLAS](villas/README.md) | C/C++     | Real-time HiL/GD-RTS for power systems                     | Apache 2.0/GPLv3 |

### Comparison Table

The following table summarizes the per-framework details in [`mosaik/README.md`](mosaik/README.md),
[`dacedsx/README.md`](dacedsx/README.md) and [`villas/README.md`](villas/README.md) by mapping
common scenario concepts across the three frameworks.

| # | Concept             | mosaik (Scenario API)                                                         | mosaik (Datamodel)                                                              | DaceDSX               | VILLAS |
|---|------------------------------|-------------------------------------------------------------------------------|---------------------------------------------------------------------------------|-----------------------|---|
| 1 | **Simulation Configuration** | Python file                                                                   | `Scenario` object aggregating `simulators`, `tesserae`, `connections`, `params` | JSON scenario file    | Set of config files (JSON or libconfig format) |
| 2 | **Simulation Component**     | `Simulator` via `world.start()`                                               | `Simulator` with `starter`, `init_params`, `plugin_name`                        | `buildingBlocks[]` array | `nodes{}` object with `type` field (e.g., "socket", "fpga") |
| 3 | **Simulation Model**         | `META.models` dict defined in simulator                                       | Not explicitly represented (part of simulator impl., referenced via `plugin_name`) | `type` field (wrapper name per building block) | - |
| 4 | **Model Component**          | `Entity` created via `Model.create(n)`                                        | `Tessera` grouping entities via `entity_sources` (`CreateSource` with `num`, `params`) | `responsibilities[]` array (list of model components like busses, streets) | - |
| 5 | **Connection Port (Input)**  | Attributes defined in `META` of simulator (implicit)                          | Not explicitly represented (implicit via `attr_pairs` of `Connection`)          | `observers[]` with consumer functionality, topics (implicit, publisher/subscriber) | `in{}` object defining input configuration |
| 6 | **Connection Port (Output)** | Attributes defined in `META` of simulator (implicit)                          | Not explicitly represented (implicit via `attr_pairs` of `Connection`)          | `observers[]` with publisher functionality, topics (implicit, publisher/subscriber) | `out{}` object defining output configuration |
| 7 | **Simulation Connection**    | `world.connect()` method                                                      | `Connection` with `source`, `dest`, `attr_pairs`, `relation`, `settings`        | Topics via Kafka pub/sub, `Translator` (same domain), `Projector` (different domains) | `paths[]` array defining routing between nodes (incl. direction of flow) |
| 8 | **Message Schema**           | Derived automatically from `world.connect()` calls (list of attribute tuples) | Not explicitly represented (derived from `attr_pairs` of `Connection`)          | Avro schema validated via a schema registry | `signals[]` array + `format` type (e.g., "villas.human", "json") |
| 9 | **Message Attribute**        | Tuple of `(src_attr, dest_attr)` strings                                      | One pair `(src_attr, dest_attr)` in `attr_pairs` list                           | Fields in Avro schema records | Signal object with `name`, `type`, `unit`, `init` |
| 10 | **Message Modification**     | Transform functions via `world.connect(..., transform=transform_func)`        | Not yet explicitly represented in datamodel                                     | `Translator` and `Projector` components | `hooks[]` array (e.g., `limit_rate`, `scale`) |
| 11 | **Simulation Parameter**     | Parameter of world.run(until=3600)                                            | `params` object → `ScenarioParams` (`until`, `rt_mode`, `rt_factor`, `rt_strict`, `print_progress`, `lazy_stepping`) | fields on top level of scenario config file | Global settings: `hugepages`, `affinity`, `priority`, `idle_stop`, `uuid`, `seed` |
| 12 | **Component Parameter**      | Parameter passed to `world.start()`                                           | `init_params` of the `Simulator`                                                | Building-block fields | Node-type specific parameters in node config |
| 13 | **Resources/Results**        | Output via `OutputSimulator`                                                  | Not modeled in datamodel                                                        | `resources{}` dict (input files), `results{}` dict (output config) | File paths in `file` node-type |

## OEO Alignment

The comparison above shows that the three frameworks express overlapping but inconsistent scenario
concepts. The goal of this project is to lift these concepts into the shared Open Energy Ontology
(OEO), so that the scenarios defined in the different framework can be better alignes and compared.
This section analyses how the concepts summarised in the [framework comparison](#co-simulation-framework-comparison)
align with the OEO, using the actual state of the OEO discussions and the concepts implemented so far
(see the [meta-issue #2089](https://github.com/OpenEnergyPlatform/ontology/issues/2089)).

It identifies:
1. which concepts are already implemented in the OEO,
2. which are in development,
3. misalignments in the local mappings stored in this repository, and
4. proposals for new OEO term definitions needed to represent scenario definitions of the three frameworks.

### 1. Current OEO implementation status

The co-simulation scenario concepts are contributed to the OEO via sub-issues of the meta-issue
[#2089](https://github.com/OpenEnergyPlatform/ontology/issues/2089). Status overview:

| OEO term                                                          | OEO ID | Status                  | Source |
|-------------------------------------------------------------------|--------|-------------------------|--------|
| simulation plan specification (the "simulation scenario" concept) | `OEO_00420000` | **implemented** (#2125) | #2071 |
| simulation configuration                                          | `OEO_00420001` | **implemented** (#2125) | #2071 |
| output creation objective                                         | `OEO_00420002` | **implemented** (#2125) | #2071 |
| output data creation objective                                    | `OEO_00420003` | **implemented** (#2125) | #2071 |
| simulation component role                                         | `OEO_00420005` | **implemented** (#2271) | #2072 |
| simulation component                                              | `OEO_00420006` | **implemented** (#2271) | #2072 |
| hardware simulation component                                     | `OEO_00420007` | **implemented** (#2271) | #2072 |
| device under test role                                            | `OEO_00420008` | **implemented** (#2271) | #2072 |
| controls hardware function of (object property)                   | `OEO_00420011` | **implemented** (#2271) | #2072 |
| electronic hardware (rename of hardware)                          | `OEO_00000206` | **renamed** (#2267)     | #2196 |
| material artifact (import from CCO)                               | `ont00000995` | **imported** (#2267)    | #2196 |

**Open / not yet started:**
- [#2111](https://github.com/OpenEnergyPlatform/ontology/issues/2111) — Add simulation connections
  (proposes `simulation connection port`, `simulation connection`, `message modification`,
  `message schema`, `message attribute`).
- [#2275](https://github.com/OpenEnergyPlatform/ontology/issues/2275) — add `electrical hardware`
  (as subclass of `material artifact`).
- [#2276](https://github.com/OpenEnergyPlatform/ontology/issues/2276) — move artificial objects to
  `material artifact`.
- [#2134](https://github.com/OpenEnergyPlatform/ontology/issues/2134) — software interface restructure.

### 2. Alignment of framework concepts to OEO terms

The framework comparison table defines 13 (plus "resources/results") concepts. The mapping below
shows their target OEO term(s) and implementation status.

| Framework concept | Proposed OEO term(s)                                                                         | Status                                                          |
|-------------------|----------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| Simulation Configuration | `simulation configuration`                                                 | implemented                                                     |
| Simulation Scenario (goal/objective of the scenario) | `simulation plan specification` + `output creation objective`  | implemented                                                     |
| Simulation Component | `simulation component` / `simulation hardware component`   | implemented                                                     |
| Simulation Model | `simulation components role` / existing `simulation model`                   | implemented                                                     |
| Model Component |                                             | not yet implemented                                             |
| Connection Port (Input/Output) | `simulation connection port`                                                                 | **not yet implemented** (#2111)                                 |
| Simulation Connection | `simulation connection`                                                                      | **not yet implemented** (#2111)                                 |
| Message Schema | `message schema`                                                                             | **not yet implemented** (#2111)                                 |
| Message Attribute | `message attribute`                                                                          | **not yet implemented** (#2111)                                 |
| Message Modification | `message modification`                                                                       | **not yet implemented** (#2111)                                 |
| Simulation Parameter | —                                                                                            | **gap** (not covered by any issue)                              |
| Component Parameter | —                                                                                            | **gap** (not covered by any issue)                              |
| Resources / Results | —                                                                                            | **gap** (discussed in the mapping spreadsheet as open question) |

### References

- OEO meta-issue: [#2089](https://github.com/OpenEnergyPlatform/ontology/issues/2089)
- Implemented: simulation scenario [#2071](https://github.com/OpenEnergyPlatform/ontology/issues/2071) / [#2125](https://github.com/OpenEnergyPlatform/ontology/pull/2125); hardware restructure [#2196](https://github.com/OpenEnergyPlatform/ontology/issues/2196) / [#2267](https://github.com/OpenEnergyPlatform/ontology/pull/2267); simulation component [#2072](https://github.com/OpenEnergyPlatform/ontology/issues/2072) / [#2271](https://github.com/OpenEnergyPlatform/ontology/pull/2271)
- Open: simulation connections [#2111](https://github.com/OpenEnergyPlatform/ontology/issues/2111), electrical hardware [#2275](https://github.com/OpenEnergyPlatform/ontology/issues/2275), artificial objects→material artifact [#2276](https://github.com/OpenEnergyPlatform/ontology/issues/2276), software interface [#2134](https://github.com/OpenEnergyPlatform/ontology/issues/2134)
