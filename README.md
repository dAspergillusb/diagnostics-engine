# Diagnostics Engine

A Flask-based educational diagnostics and assessment platform for managing subject-specific tests, student workflows, teacher tools, administrative functions, and reporting.

The project demonstrates a modular Python web application built with **Flask**, **SQLAlchemy**, **SQLite**, and server-rendered templates.

## Highlights

- Flask web application with modular endpoint registration
- separate student, teacher, and administrator workflows
- subject-specific assessment databases
- reusable test-generation and test-checking modules
- SQLAlchemy ORM with SQLite
- reporting and statistics utilities
- Excel processing with `openpyxl`
- server-rendered HTML templates and static assets
- dedicated modules for configuration, database access, business logic, endpoints, errors, and tests

## Tech Stack

### Backend

- Python
- Flask
- SQLAlchemy
- Werkzeug

### Database

- SQLite

### Data & Reporting

- openpyxl
- generated reports and statistics utilities

### Frontend

- HTML templates
- CSS
- JavaScript / static assets

## Architecture

The project is organized around a modular Flask application with separate packages for endpoints, database models, shared functions, reporting, and test logic.

```text
.
├── diagnostics/
│   ├── __init__.py
│   ├── modules/
│   │   ├── _types/
│   │   ├── databases/
│   │   ├── email_engine/
│   │   ├── endpoints/
│   │   ├── errors/
│   │   ├── functions/
│   │   └── tests_engine/
│   ├── static/
│   └── templates/
├── reports/
├── requirements.txt
└── supporting scripts
```

## Application Roles

The application contains separate workflows for:

- **Students** — access assessments and student-facing pages
- **Teachers** — manage test-related workflows and teacher tools
- **Administrators** — access administrative pages and system-level functions

The Flask application registers dedicated endpoint modules for each of these areas.

## Assessment & Subject Support

The project contains dedicated database modules for multiple school subjects, including:

- Informatics
- Mathematics
- Algebra
- Geometry
- Biology
- Chemistry
- Geography
- History
- Literature
- English

It also includes reusable modules for generating tests, checking results, and handling subject-specific assessment logic.

## Database Layer

SQLAlchemy is used as the ORM layer.

Subject databases are stored in SQLite and accessed through dedicated database classes. Each module encapsulates database initialization, question storage, querying, and update operations for its subject domain.

Example architecture:

```text
Flask endpoints
      │
      ▼
Business / test logic
      │
      ▼
SQLAlchemy ORM
      │
      ▼
SQLite databases
```

## Reporting

The repository contains utilities for collecting statistics and generating report data. `openpyxl` is included for Excel-oriented processing and reporting workflows.

## Local Setup

### Requirements

- Python 3.10+

Clone the repository:

```bash
git clone https://github.com/dAspergillusb/diagnostics-engine.git
cd diagnostics-engine
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Flask application from the project environment according to the current configuration in `diagnostics/__init__.py`.

## Project Context

This project was developed as an educational diagnostics platform and reflects practical work with backend architecture, modular Flask applications, relational data models, subject-specific assessment logic, reporting, and role-oriented user flows.

## Author

**Nikita Zelentsov**  
Python Backend Developer

GitHub: [@dAspergillusb](https://github.com/dAspergillusb)
