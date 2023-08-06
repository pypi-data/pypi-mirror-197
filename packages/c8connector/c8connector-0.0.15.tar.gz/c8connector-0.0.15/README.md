# Implementing C8 Connectors.

Users can extend `C8Connector` interface and develop 3 types of connectors.

1. Source Connectors (Connectors that ingest data)
2. Target Connectors (Connectors that export data)
3. Integration Connectors (Generic integrations for other services)

When developing these connectors, developers must adhere to a few guidelines mentioned below.

## Naming the Connector

- Package name of the connector must be in the `macrometa-{type}-{connector}` format (i.e `macrometa-source-postgres`).
- Module name of the connector must be in the `macrometa_{type}_{connector}` format (i.e `macrometa_source_postgres`).

## Project structure (package names and structure)

- Project source code must follow the below structure.
```text
.
├── LICENSE
├── README.md
├── GETTING_STARTED.md
├── macrometa_{type}_{connector}
│        ├── __init__.py
│        └── main.py
│        └── {other source files or modules}
├── pyproject.toml
└── setup.cfg
```
- Within the `/macrometa_{type}_{connector}/__init__.py` there must be a class which implements `C8Connector` interface.

## Dependencies/Libraries and their versions to use.

- Connectors must only use following dependencies/libraries and mentioned versions' when developing.
```text
python = ">=3.7"
c8connector = "latest"
pipelinewise-singer-python = "1.2.0"
```
- Developers must not use `singer-sdk` or any other singer sdk variants other than `pipelinewise-singer-python`.

## Connector specific documentation

- Every connector project should have a GETTING_STARTED.md file, documenting the connector configuration and all other requirements for the connector.
  It should be formatted like a User-Facing document and it should also provide the necessary instructions for the end user to be able to use the connector.
  
  Developers can follow the Generic Template available [here](https://github.com/Macrometacorp/c8connector/blob/main/GETTING_STARTED.md) and apply any necessary changes required on top of it for the specific connector.


## Samples
- Postgres Source Connector: [Git Repository](https://github.com/Macrometacorp/macrometa-source-postgres)
- Oracle Source Connector: [Git Repository](https://github.com/Macrometacorp/macrometa-source-oracle)
- C8 Collections target Connector: [Git Repository](https://github.com/Macrometacorp/macrometa-target-collection)
