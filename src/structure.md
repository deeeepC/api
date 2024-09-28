api/
│
├── src/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── can data endpoints
│   │   │   │   ├── sensor data endpoints
│   │   │   │   ├── camera data endpoints
│   │   │   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config settings
│   │   ├── authentication, if needed
│   ├── models/
│   │   ├── __init__.py
│   │   ├── can data model
│   │   ├── sensor data model
│   │   ├── camera data model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── can data schema
│   │   ├── sensor data schema
│   │   ├── camera data schema
│   ├── services/
│   │   ├── __init__.py
│   │   ├── can data processing
│   │   ├── sensor data processing
│   │   ├── camera data processing
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base ORM models
│   │   ├── db connection
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test can data
│   │   ├── test sensor data
│   │   ├── test camera data
│   ├── utils/  # Utilities for data parsing, etc.
│   │   ├── __init__.py
│   │   ├── util for parsing and validating incoming data
│   ├── app entry point
│   ├── __init__.py
│
├── Dockerfile
├── .env
├── .gitignore
├── commands.md
├── readme.md
└── version.md
