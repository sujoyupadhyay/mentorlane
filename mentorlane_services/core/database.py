import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL connection string for local database
# Format: mysql+pymysql://username:password@localhost:3306/database_name
MYSQL_CONNECTION_STRING = os.getenv(
    "MYSQL_CONNECTION_STRING",
    "mysql+pymysql://root@localhost:3306/mentorlane"
)

# Create SQLAlchemy engine
try:
    engine = create_engine(
        MYSQL_CONNECTION_STRING,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False
    )
except Exception as e:
    print(f"Error creating database engine: {e}")
    print(f"Please check your MYSQL_CONNECTION_STRING environment variable.")
    print(f"Current connection string: {MYSQL_CONNECTION_STRING}")
    raise

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    """Get database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {e}")
        raise
    finally:
        db.close()

# Test database connection
def test_connection():
    """Test the database connection."""
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        print("Database connection successful!")
        return True
    except SQLAlchemyError as e:
        print(f"Database connection failed: {e}")
        print(f"Please check your MySQL credentials and ensure the server is running.")
        print(f"Connection string: {MYSQL_CONNECTION_STRING}")
        return False
    except Exception as e:
        print(f"Unexpected error testing database connection: {e}")
        return False
