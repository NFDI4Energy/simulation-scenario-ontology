# mosaik scenario configuration based on OEO co-sim module

## Requirements

The easiest way of running this code is uv: https://docs.astral.sh/uv/getting-started/installation/

## LinkML 

Generate UML Diagram from LinkML model:

`uv run gen-plantuml --directory .\export\UML\ .\mosaik_scenario.yaml`

Generate whole project from LinkML model (containing for example JSONLD context, OWL file, Python dataclass): 

`uv run gen-project -d .\export\ .\mosaik_scenario.yaml`

## Test script

Execute the test script to instantiate a mosaik scenario and dump it to JSONLD file:

``uv run test_script.py``

