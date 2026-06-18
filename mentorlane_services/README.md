# MentorLane API Documentation

This FastAPI application includes comprehensive Swagger/OpenAPI documentation.

## Features

- **Interactive API Documentation**: Swagger UI at `/docs`
- **Alternative Documentation**: ReDoc at `/redoc`
- **OpenAPI Schema**: Available at `/openapi.json`
- **Database Support**: MySQL database connection with SQLAlchemy
- **Detailed Descriptions**: Each endpoint includes summary, description, and response codes
- **API Versioning**: Structured with version prefixes (/api/v1/) for future scalability
- **Modular Structure**: Organized into separate API route files for better maintainability

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Database Setup

1. **Create MySQL Database**:
   ```sql
   CREATE DATABASE mentorlane;
   ```

2. **Configure Connection**:
   - Set the `MYSQL_CONNECTION_STRING` environment variable with your MySQL credentials
   - Or modify the default connection string in `core/database.py`
   - **Important**: Make sure your MySQL credentials are correct:
     - Username: Your MySQL username (often 'root')
     - Password: Your MySQL password (leave empty if no password)
     - Host: Usually 'localhost' or '127.0.0.1'
     - Port: Usually '3306' (default MySQL port)
     - Database: 'mentorlane' (or your database name)

3. **Default Connection String Format**:
   ```
   mysql+pymysql://username:password@localhost:3306/mentorlane
   ```

4. **Test Connection**:
   ```python
   from core.database import test_connection
   test_connection()
   ```

5. **Create Database Tables**:
   - Run the SQL script to create the teaching_modes table:
   ```bash
   mysql -u root -p mentorlane < database_schema.sql
   ```

## Running the Application

```bash
# Run the FastAPI server
uvicorn main:app --reload
```

## Accessing Documentation

Once the server is running, access the documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### General
- `GET /` - Root endpoint with welcome message
- `GET /health` - Health check endpoint

### Teaching Modes
- `GET /api/v1/teaching-modes/` - Get all teaching modes (with pagination)
- `GET /api/v1/teaching-modes/active` - Get only active teaching modes
- `GET /api/v1/teaching-modes/{teaching_mode_id}` - Get specific teaching mode by UUID
- `POST /api/v1/teaching-modes/` - Create new teaching mode
- `PUT /api/v1/teaching-modes/{teaching_mode_id}` - Update existing teaching mode
- `DELETE /api/v1/teaching-modes/{teaching_mode_id}` - Delete teaching mode
- `POST /api/v1/teaching-modes/{teaching_mode_id}/activate` - Activate teaching mode
- `POST /api/v1/teaching-modes/{teaching_mode_id}/deactivate` - Deactivate teaching mode
- `GET /api/v1/teaching-modes/search/{search_term}` - Search teaching modes by name

### Teaching Languages
- `GET /api/v1/teaching-languages/` - Get all teaching languages (with pagination)
- `GET /api/v1/teaching-languages/active` - Get only active teaching languages
- `GET /api/v1/teaching-languages/{teaching_languages_id}` - Get specific teaching language by UUID
- `POST /api/v1/teaching-languages/` - Create new teaching language
- `PUT /api/v1/teaching-languages/{teaching_languages_id}` - Update existing teaching language
- `DELETE /api/v1/teaching-languages/{teaching_languages_id}` - Delete teaching language
- `POST /api/v1/teaching-languages/{teaching_languages_id}/activate` - Activate teaching language
- `POST /api/v1/teaching-languages/{teaching_languages_id}/deactivate` - Deactivate teaching language
- `GET /api/v1/teaching-languages/search/{search_term}` - Search teaching languages by name

### Teaching Levels
- `GET /api/v1/teaching-levels/` - Get all teaching levels (with pagination)
- `GET /api/v1/teaching-levels/active` - Get only active teaching levels
- `GET /api/v1/teaching-levels/{teaching_levels_id}` - Get specific teaching level by UUID
- `POST /api/v1/teaching-levels/` - Create new teaching level
- `PUT /api/v1/teaching-levels/{teaching_levels_id}` - Update existing teaching level
- `DELETE /api/v1/teaching-levels/{teaching_levels_id}` - Delete teaching level
- `POST /api/v1/teaching-levels/{teaching_levels_id}/activate` - Activate teaching level
- `POST /api/v1/teaching-levels/{teaching_levels_id}/deactivate` - Deactivate teaching level
- `GET /api/v1/teaching-levels/search/{search_term}` - Search teaching levels by name or description

## Project Structure

```
mentorlane_database/
├── app/
│   ├── __init__.py
│   └── v1/
│       ├── __init__.py
│       ├── teaching_modes_api.py    # API routes for teaching modes
│       ├── teaching_language_api.py # API routes for teaching languages
│       └── teaching_levels_api.py   # API routes for teaching levels
├── core/
│   ├── __init__.py
│   └── database.py                   # Database connection and configuration
├── models/
│   ├── __init__.py
│   ├── teaching_modes_model.py      # Pydantic models for teaching modes
│   ├── teaching_language_model.py   # Pydantic models for teaching languages
│   └── teaching_levels_model.py     # Pydantic models for teaching levels
├── repositories/
│   ├── __init__.py
│   ├── teaching_modes_repository.py  # Database operations for teaching modes
│   ├── teaching_language_repository.py # Database operations for teaching languages
│   └── teaching_levels_repository.py   # Database operations for teaching levels
├── services/
│   ├── __init__.py
│   ├── teaching_modes_service.py     # Business logic for teaching modes
│   ├── teaching_language_service.py  # Business logic for teaching languages
│   └── teaching_levels_service.py    # Business logic for teaching levels
├── main.py                           # Application entry point
├── requirements.txt                  # Python dependencies
├── schemas/
│   └── database_schema.sql           # Database schema
└── README.md                         # Documentation
```

## Architecture

The application follows a three-layer architecture pattern with API versioning:

### API Layer (`app/v1/`)
- FastAPI routers for endpoint organization
- API versioning structure (/api/v1/)
- Request/response handling
- HTTP status codes and error handling
- Dependency injection for database sessions
- Modular route files for different resources

### Service Layer (`services/`)
- Business logic implementation
- Data validation and transformation
- Calls repository methods
- Handles business rules and exceptions
- Additional functionality like search, activate/deactivate

### Repository Layer (`repositories/`)
- Database operations using SQLAlchemy
- CRUD operations (Create, Read, Update, Delete)
- Database session management
- Data persistence logic

### Models Layer (`models/`)
- Pydantic models for request/response validation
- SQLAlchemy ORM models for database mapping
- Data structure definitions

### Core Layer (`core/`)
- Database connection and configuration
- Shared utilities and configurations
- Session management

## Data Models

### Teaching Mode
```json
{
  "teaching_mode_id": "550e8400-e29b-41d4-a716-446655440000",
  "teaching_mode": "Online",
  "IsActive": true
}
```

### Create Teaching Mode
```json
{
  "teaching_mode": "Online",
  "IsActive": true
}
```

### Update Teaching Mode
```json
{
  "teaching_mode": "Online (Updated)",
  "IsActive": false
}
```

### Teaching Level
```json
{
  "teaching_levels_id": "550e8400-e29b-41d4-a716-446655440000",
  "teaching_level_name": "Beginner",
  "teaching_level_description": "Introductory level for beginners",
  "IsActive": true
}
```

### Create Teaching Level
```json
{
  "teaching_level_name": "Beginner",
  "teaching_level_description": "Introductory level for beginners",
  "IsActive": true
}
```

### Update Teaching Level
```json
{
  "teaching_level_name": "Beginner (Updated)",
  "teaching_level_description": "Updated description",
  "IsActive": false
}
```

## Customization

You can customize the Swagger documentation by modifying the FastAPI app configuration in `main.py`:

```python
app = FastAPI(
    title="Your API Title",
    description="Your API Description",
    version="1.0.0",
    docs_url="/docs",        # Swagger UI path
    redoc_url="/redoc",      # ReDoc path
    openapi_url="/openapi.json"  # OpenAPI schema path
)
```

## Troubleshooting

### Database Connection Issues

If you encounter authentication errors like `Access denied for user 'root'@'localhost'`:

1. **Check MySQL Credentials**:
   - Verify your MySQL username and password are correct
   - Update the connection string in `core/database.py` or set the `MYSQL_CONNECTION_STRING` environment variable
   - If you don't have a password, use: `mysql+pymysql://root@localhost:3306/mentorlane`
   - If you have a password, use: `mysql+pymysql://root:your_password@localhost:3306/mentorlane`

2. **Check MySQL Server**:
   - Ensure MySQL server is running
   - On Windows: Check Services for MySQL service
   - On Linux/Mac: `sudo systemctl status mysql` or `brew services list`

3. **Check Connection Details**:
   - Verify host (localhost vs 127.0.0.1)
   - Verify port (default is 3306, not 8080)
   - Ensure the database 'mentorlane' exists

4. **Test Connection**:
   ```python
   from core.database import test_connection
   test_connection()
   ```

5. **Common Connection String Formats**:
   - No password: `mysql+pymysql://root@localhost:3306/mentorlane`
   - With password: `mysql+pymysql://root:password@localhost:3306/mentorlane`
   - Different host: `mysql+pymysql://root:password@127.0.0.1:3306/mentorlane`
   - Different port: `mysql+pymysql://root:password@localhost:3307/mentorlane`
```
