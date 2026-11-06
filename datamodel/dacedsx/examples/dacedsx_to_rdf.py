#!/usr/bin/env python3
"""DaceDSX-Scenario (JSON) -> RDF (Turtle), verlinkt mit der OEO-Scenario-Ontologie.

Die Klassen- und Property-IRIs werden zur Laufzeit aus dem LinkML-Schema
(oeo_scenario.yaml) gelesen (class_uri / slot_uri). Wenn dort die Platzhalter
"OEO_0042XXXX-..." durch echte IDs ersetzt werden, muss hier nichts geändert werden.

Requirements:
    pip install pyyaml rdflib

Aufruf:
    python dacedsx_to_rdf.py sce_pv_bat_ieee13_more_pv.json oeo_scenario.yaml -o scenario.ttl
"""
import argparse
import json
from urllib.parse import quote

import yaml
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD

# --------------------------------------------------------------------------
# Erweiterungen: Felder, für die das Schema (noch) keinen Slot hat.
# Bewusst in eigenem Namespace, damit sie leicht zu finden / zu ersetzen sind.
# --------------------------------------------------------------------------
EXT = Namespace("https://example.org/oeo-scenario-ext#")

BLOCK_LITERAL_FIELDS = {  # JSON-Feld -> (Property, Datentyp)
    "type": (EXT.wrapperType, XSD.string),
    "layer": (EXT.layer, XSD.string),
    "domain": (EXT.domain, XSD.string),
    "stepLength": (EXT.stepLength, XSD.decimal),
    "synchronized": (EXT.synchronized, XSD.boolean),
    "isExternal": (EXT.isExternal, XSD.boolean),
}
SCENARIO_PARAMS = {  # JSON-Pfad -> Parametername
    ("simulationStart",): "simulationStart",
    ("simulationEnd",): "simulationEnd",
    ("execution", "randomSeed"): "randomSeed",
    ("execution", "priority"): "priority",
    ("execution", "syncedParticipants"): "syncedParticipants",
}


class Schema:
    """Liest class_uri / slot_uri aus dem LinkML-YAML und expandiert CURIEs."""

    def __init__(self, path):
        with open(path, encoding="utf-8") as f:
            self.doc = yaml.safe_load(f)
        self.prefixes = self.doc["prefixes"]

    def _expand(self, curie):
        prefix, _, local = curie.partition(":")
        return URIRef(self.prefixes[prefix] + local)

    def cls(self, name):
        return self._expand(self.doc["classes"][name]["class_uri"])

    def slot(self, name):
        return self._expand(self.doc["slots"][name]["slot_uri"])


def seg(s):
    return quote(str(s).strip(), safe="")


def build_graph(scenario, schema, base):
    g = Graph()
    g.bind("oeo", schema.prefixes["oeo"])
    g.bind("bfo", schema.prefixes["bfo"])
    g.bind("ext", EXT)
    g.bind("rdfs", RDFS)

    sid = scenario["scenarioID"]
    root = URIRef(f"{base}{seg(sid)}")
    g.add((root, RDF.type, schema.cls("SimulationConfiguration")))
    g.add((root, RDFS.label, Literal(sid)))

    # --- Scenario-Parameter (Extension, da ScenarioParameter im Schema keine Slots hat)
    for path, name in SCENARIO_PARAMS.items():
        value = scenario
        for key in path:
            value = value.get(key) if isinstance(value, dict) else None
        if value is None or value == "":
            continue
        p = URIRef(f"{root}/param/{seg(name)}")
        g.add((p, RDF.type, schema.cls("ScenarioParameter")))
        g.add((p, EXT.name, Literal(name)))
        g.add((p, EXT.value, Literal(value)))
        g.add((root, EXT.hasScenarioParameter, p))

    # --- Model Components (aus "responsibilities"), dedupliziert über den Namen
    def model_component(name):
        iri = URIRef(f"{root}/entity/{seg(name)}")
        g.add((iri, RDF.type, schema.cls("MaterialArtifact")))
        g.add((iri, RDFS.label, Literal(name)))
        return iri

    # --- Building Blocks -> SimulationComponent (+ Observer -> Ports)
    ports_by_layer = {}  # layer -> [port-IRIs], für die Verknüpfung mit Translatoren
    for bb in scenario.get("buildingBlocks", []):
        comp = URIRef(f"{root}/{seg(bb['instanceID'])}")
        g.add((root, schema.slot("simulation_components"), comp))
        g.add((comp, RDF.type, schema.cls("SimulationComponent")))
        g.add((comp, RDFS.label, Literal(bb["instanceID"])))

        if bb.get("parameters"):
            # Platzhalter: schemakonform als String. Für Vergleichbarkeit besser
            # strukturiert (siehe Hinweise).
            g.add((comp, schema.slot("init_params"),
                   Literal(json.dumps(bb["parameters"], ensure_ascii=False, sort_keys=True))))

        for field, (prop, dtype) in BLOCK_LITERAL_FIELDS.items():
            if field in bb and bb[field] != "":
                g.add((comp, prop, Literal(bb[field], datatype=dtype)))

        for name in bb.get("responsibilities", []):
            g.add((comp, schema.slot("controls"), model_component(name)))

        for i, obs in enumerate(bb.get("observers", [])):
            is_pub = obs.get("task") == "publish"
            port = URIRef(f"{comp}/port/{i}")
            g.add((port, RDF.type, schema.cls(
                "SimulationConnectionOutputPort" if is_pub else "SimulationConnectionPort")))
            g.add((comp, schema.slot("has_connection_port"), port))
            for field in ("task", "element", "filter", "period", "trigger", "type"):
                if obs.get(field) not in (None, ""):
                    g.add((port, EXT["observer_" + field], Literal(obs[field])))
            ports_by_layer.setdefault(bb.get("layer"), []).append(port)

    # --- Translators / Projectors -> SimulationConnection
    def split(s):
        return [x.strip() for x in str(s).split(",") if x.strip()]

    for kind, key, idkey in (("translator", "translators", "translatorID"),
                             ("projector", "projectors", "projectorID")):
        for t in scenario.get(key, []):
            conn = URIRef(f"{root}/{kind}/{seg(t.get(idkey, kind))}")
            g.add((conn, RDF.type, schema.cls("SimulationConnection")))
            g.add((conn, RDFS.label, Literal(t.get(idkey, kind))))
            g.add((conn, EXT.connectionKind, Literal(kind)))
            if t.get("type"):
                g.add((conn, EXT.wrapperType, Literal(t["type"])))
            g.add((root, schema.slot("has_simulation_connection"), conn))
            for side in ("A", "B"):
                for layer in split(t.get("layer" + side, "")):
                    for port in ports_by_layer.get(layer, []):
                        g.add((port, schema.slot("has_simulation_connection"), conn))
                for name in t.get("responsibilities" + side, []):
                    g.add((conn, EXT["responsibility" + side], model_component(name)))
    return g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenario_json")
    ap.add_argument("schema_yaml")
    ap.add_argument("-o", "--out", default="-")
    ap.add_argument("--base", default="https://example.org/scenario/",
                    help="Namespace für die Instanz-IRIs")
    args = ap.parse_args()

    with open(args.scenario_json, encoding="utf-8") as f:
        scenario = json.load(f)
    g = build_graph(scenario, Schema(args.schema_yaml), args.base)
    ttl = g.serialize(format="turtle")
    if args.out == "-":
        print(ttl)
    else:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(ttl)


if __name__ == "__main__":
    main()
