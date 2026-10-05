# OEO Simulation Scenario Datamodel

LinkML schemas describing the datamodel for  standardizing co-simulation frameworks 
(mosaik, VILLASframework, DaceDSX) based on the OEO simulation scenario ontology.

# Use LinkML
 
Execute the following commands in the datamodel directory with installed [uv](https://docs.astral.sh/uv/getting-started/installation/).
 
Validate oeo_scenario: ``uv run linkml validate oeo_scenario.yaml``

Create UML diagram: ``uv run gen-plantuml -d export/UML -f svg oeo_scenario.yaml``

Generate many different formats from LinkML data model into directory ``export``:

``uv run linkml generate project .\oeo_scenario.yaml -d export``