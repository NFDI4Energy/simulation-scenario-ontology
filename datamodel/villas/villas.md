# VILLAS Framework

**Website**: https://villas.fein-aachen.org/
**Documentation**: https://villas.fein-aachen.org/docs/
**Language**: C/C++ (Python tools)
**License**: Apache 2.0 / GPLv3

VILLASframework is a toolset for local and geographically distributed real-time co-simulation, primarily designed for hardware-in-the-loop (HiL) and geographically distributed real-time simulation (GD-RTS) of power systems.

## Overview

VILLAS consists of several independent components:

- **VILLASnode**: Modular gateway for simulation data (interface for equipment, databases, web services)
- **VILLASweb**: Web-based UI for scenario management and monitoring
- **VILLAScontroller**: Configuration and control of laboratory infrastructure
- **VILLASfpga**: FPGA-based real-time interfaces

VILLASnode is the core component for co-simulation scenario definition.

## Key Concepts

### Simulation Configuration

All configuration files that will be used to interconnect equipment for a specific experiment 


### Simulation Component (Node)

Nodes represent communication endpoints:

```json
"udp_node": {
  "type": "socket",
  "format": "villas.human",
  "layer": "udp",
  "verify_source": false,
  "in": {
    "address": "0.0.0.0:12000",
    "signals": [],
    "hooks": []
  },
  "out": {
    "address": "192.168.1.100:12000",
    "hooks": []
  },
  "vectorize": 1,
  "hooks": [],
  "builtin": true
}
```

### Simulation Model

Not represented.

### Model Component

Not represented.

### Simulation Connection Port

Input port configuration:
```json
"in": {
  "address": "0.0.0.0:12000",
  "signals": [],
  "vectorize": 1,
  "hooks": []
}
```

Output port configuration:
```json
"out": {
  "address": "192.168.1.100:12000",
  "netem": {},
  "multicast": {},
  "vectorize": 0,
  "hooks": []
}
```

### Simulation Connection (Paths)

Paths define data routing between nodes. They also define **how** the node types exchange messages (the direction and flow of data), not just *which* nodes are connected. The strings are the names of the nodes:

```json
"paths": [
  {
    "in": ["udp_node", "udp_node2"],
    "out": ["file_node"]
  },
  {
    "in": ["websocket_node"],
    "out": ["kafka_node"]
  }
]
```

### Message Schema (Signals Object and Format)

Signals define the data format:

```json
"format": "villas.human" 
"signals": [
  {
    "name": "tap_position",
    "type": "integer",
    "init": 0
  },
  {
    "name": "voltage",
    "type": "float",
    "unit": "V",
    "init": 230.0
  }
]
```

Each node has one `format` and the `signals` are defined in the `in`/`out` of the node definition.

### Message Attribute

A single signal object is an individual message attribute:

```json
{
  "name": "voltage",
  "type": "float",
  "unit": "V",
  "init": 230.0
}
```

### Format Types

Supported payload formats:

| Format | Description |
|--------|-------------|
| `villas.human` | Human-readable VILLAS format |
| `villas.binary` | Binary VILLAS format |
| `json` | JSON |
| `csv` | Comma-separated values |
| `protobuf` | Google Protocol Buffers |
| `raw` | Raw binary values |

### Message Modification (Hooks)

Hooks modify or process messages:

```json
"hooks": [
  {
    "type": "limit_rate",
    "rate": 5.5
  }
]
```

Available hook types: `limit_rate`, `scale`, `offset`, `statistics`, and more. Hooks can be a part of a node and of a path.

### Simulation Parameters (Global)

```json
{
  "http": {
    "port": 8081
  },
  "logging": {
    "level": "debug"
  },
  "stats": 2,
  "hugepages": 100,
  "affinity": 0,
  "priority": 0,
  "idle_stop": true,
  "uuid": "optional-uuid",
  "seed": 42
}
```

Global parameters for each configuration. 

| Parameter | Description |
|-----------|-------------|
| `http` | HTTP / WebSocket server configuration (e.g. `port`) |
| `logging` | Logging configuration (e.g. `level`) |
| `hugepages` | Number of reserved hugepages for real-time memory |
| `affinity` | CPU core affinity mask (pinning) |
| `priority` | Process scheduling priority |
| `idle_stop` | Stop on idle flag |
| `uuid` | Unique instance identifier |
| `seed` | Random number generator seed |
| `stats` | Statistics reporting interval |

### Simulation Component Parameters

Node-type specific parameters are defined directly in the node object (e.g. `type`, `format`, `layer`, `vectorize`, `builtin`, and the `in`/`out` port configurations):

```json
{
  "type": "socket",
  "format": "villas.human",
  "layer": "udp",
  "verify_source": false,
  "in": {},
  "out": {},
  "vectorize": 1,
  "hooks": [],
  "builtin": true
}
```
