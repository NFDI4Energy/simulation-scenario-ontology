# Simulation Scenario Ontology

The simulation scenario ontology aims to provide structures for modeling of energy system simulation scenarios as part of the NFDI4Energy plattform.
We decided to implement the simulation scenario ontology directly in the Open Energy Ontology (OEO).
Thus, this repository is not containing the ontology itself, but gives an overview over requirements, documents, discussions, and the implemented concepts.

# Ontology Requirements Specification (ORSD)

The following section summarises the ontology requirements specification document for the simulation scenario ontology, defining its purpose, scope, intended users and uses, as well as the requirements it must fulfil.

| | |
|---|---|
| **Ontology Name** | NFDI4Energy Simulation Scenario Ontology |
| **Responsible Team** | Task Area 5, Measure 5.2 |
| **Purpose** | This ontology will represent simulation scenarios for distributed (co-)simulation in the energy domain. It should be used to align the scenario definition of different simulation frameworks. |
| **Scope** | This ontology will focus on scenario definition for mosaik, VILLAS, and DaceDSX. It should also be open for use with other simulation frameworks in the future. |
| **Implementation Language** | OWL |
| **Intended End-Users** | <ul><li>Measure 5.3 team: Developer of simulation frameworks (to align framework with this ontology)</li><li>Measure 5.4 team: Developer of Simulation as a Service (SimaaS) hub</li><li>TA6: Scenario definition of use cases</li><li>User of platform describing simulation scenarios based on ontology</li><li>Developer of other simulation frameworks</li></ul> |
| **Intended Uses** | <ul><li>Base for scenario definition in the simulation frameworks mosaik, VILLAS and DaceDSX</li><li>Interface specification for scenario definition</li><li>Base for NFDI4Energy platform / simulation-as-a-service</li><li>Potentially base for scenario definition of other tools?</li></ul> |

## Ontology Requirements

### A. Non-Functional Requirements

- Modularity
- Use Protege and Git
- Use automatic analysis tools (Oops, Foops, Ontoology, Fairchecker, etc.)
- Reuse ontology and mapping with existing ontology
- Should answer CQ (to be defined)
- Should cover use cases (to be defined)
- Should cover chosen co-simulation frameworks as instances
- Should be compatible with the other NFDI4Energy ontologies
- The language has to be English and maybe also German

### B. Functional Requirements: Groups of Competency Questions

See competency question Excel sheets.

## Pre-Glossary of Terms

- **A. Terms from Competency Questions**
- **B. Terms from Answers**
- **C. Objects**

# OEO

All discussions about simulation scenarios are collected in the meta issue: https://github.com/OpenEnergyPlatform/ontology/issues/2089

- how we do the development
- which concepts are already released
- which concepts are under development

# Integration of other co-simulation frameworks

In NFDI4Energy the focus lays on the co-simulation frameworks DaceDSX, VILLAS, and mosaik, but the outcomes aim to allow also the integration of other frameworks.

Thus, we will add instructions on how to use our developments with other frameworks here in the future.

# List of existing ontologies

As a first step towards developing the simulation scenario ontology, we reviewed existing ontologies and evaluated their relevance for definition of simulation scenarios.
The relevant ontologies are listed below and described in:

*Schwarz, J. S., Fuentes Grau, L., Liu, N., Pan, Z., Qussous, R., Schmurr, P., Seiwerth, C., Steinert, A., German, R., Hagenmeyer, V., Lehnhoff, S., Monti, A., Nieße, A., & Weidlich, A. (2025). D5.2.1.1 Registry of relevant domain ontologies for co-simulation scenario definition. Zenodo.* https://doi.org/10.5281/zenodo.14521502.

| **Ontology**                         | **Link**                                       | **Last Update** | **Open Source** | **License**  | **Literature** |
| ------------------------------------ | ---------------------------------------------- | --------------- | --------------- | ------------ | -------------- |
| COSMO                                | -                                              | -               | No              | No           | Y. M. Teo and C. Szabo, „CODES: An integrated approach to composable modeling and simulation“, Proc. - Simul. Symp., S. 103–110, 2008, doi: https://doi.org/10.1109/ANSS-41.2008.24.           |
| DEMO                                 | https://cobweb.cs.uga.edu/~jam/jsim/DeMO/      | ?               | Yes             | No           | G. A. Silver, J. a. Miller, M. Hybinette, G. Baramidze, und W. S. York, „DeMO: An Ontology for Discrete-event Modeling and Simulation“, Simulation, Bd. 87, Nr. 9, S. 747–773, 2011, doi: https://doi.org/10.1177/0037549710386843.            |
| OSMO                                 | http://www.molmod.info/semantics/osmo.ttl      | 2020            | Yes             | LGPL 3       | M. T. Horsch, D. Toti, S. Chiacchiera, M. A. Seaton, G. Goldbeck, und I. T. Todorov, „OSMO: Ontology for simulation, modelling, and optimization“, CEUR Workshop Proc., Bd. 2969, 2021.            |
| PIMODES                              | -                                              | -               | No              | No           | L. W. Lacy, „Interchanging Discrete event simulation Process Interaction Models using the Web Ontology Language-OWL“, University of Central Florida, 2006.            |
| Ontology for Urban Energy Simulation | https://github.com/Ja98/ues/tree/master        | 05/2023         | Yes             | No           |                |
| FMI ontology                         | https://github.com/UdSAES/fmi2rdf              | 02/2022         | Yes             | MIT          | M. Stüber and G. Frey, „Dynamic system models and their simulation in the Semantic Web“, Semantic Web, Bd. 1, S. 1–36, 2023, doi: https://doi.org/10.3233/sw-233359.     |
| SMS ontology                         | https://github.com/UdSAES/sms-ontology         | 09/2022         | Yes             | MIT          | M. Stüber and G. Frey, „Dynamic system models and their simulation in the Semantic Web“, Semantic Web, Bd. 1, S. 1–36, 2023, doi: https://doi.org/10.3233/sw-233359.     |
| SimWis                               | -                                              | ?               | No              | No           | J. Stolipin and S. Wenzel, „Ontologiebasierte Methodik zur Unterstützung der Nachnutzung von Simulationswissen“, at "Simulation in Produktion und Logistik" 2019, Auerbach, 2019.           |
| OEO                                  | https://github.com/OpenEnergyPlatform/ontology | 09/2024         | Yes             | CC0 1.0      | M. Booshehri et al., „Energy and AI Introducing the Open Energy Ontology : Enhancing data interpretation and interfacing in energy systems analysis“, Energy AI, Bd. 5, Nr. April, S. 100074, 2021, doi: https://doi.org/10.1016/j.egyai.2021.100074            |
| EnArgus                              | https://www.enargus.de/                        | 2017            | Yes             | CC BY-SA 3.0 | L. Oppermann et al., „Finding and analysing energy research funding data: The EnArgus system“, Energy AI, Bd. 5, S. 100070, Sep. 2021, doi: https://doi.org/10.1016/j.egyai.2021.100070.            |

# List of sources

- *Schwarz, J. S., Fuentes Grau, L., Liu, N., Pan, Z., Qussous, R., Schmurr, P., Seiwerth, C., Steinert, A., German, R., Hagenmeyer, V., Lehnhoff, S., Monti, A., Nieße, A., & Weidlich, A. (2025). D5.2.1.1 Registry of relevant domain ontologies for co-simulation scenario definition. Zenodo.* https://doi.org/10.5281/zenodo.14521502.
- *Schwarz, J. S., Fuentes Grau, L., Liu, N., Pan, Z., Qussous, R., Schmurr, P., Seiwerth, C., & Steinert, A. (2026). D5.2.2.1 Integrated NFDI4Energy simulation scenario ontology. Zenodo.* https://doi.org/10.5281/zenodo.19011136

# License
[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
