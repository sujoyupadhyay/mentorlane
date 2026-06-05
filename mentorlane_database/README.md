# MentorLane Flask Starter

A minimal Flask application with a single route and HTML template.

## Project structure

```
.
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── teaching_modes.py
│   └── templates/
│       └── index.html
├── requirements.txt
└── run.py
```

## Getting started

1. (Optional) Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```powershell
   python run.py
   ```

The app will be live at http://127.0.0.1:5000/.

Visit http://127.0.0.1:5000/apidocs/ for Swagger UI documenting the available endpoints.

### Teaching modes API

- `POST /api/teaching-modes` (implemented in `app/teaching_modes.py`) accepts JSON payloads with `teaching_mode` and optional `description`, inserting them into the local `teaching_modes` table.

## MySQL connection helper

- Use `app.database.get_connection()` to obtain a PyMySQL connection to the local `MentorLane` schema.
- A context manager `mysql_session()` is also provided for automatic commit/rollback handling.
- Override connection parameters with environment variables: `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`.
