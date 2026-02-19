@echo off
echo Installing PostgreSQL driver...
echo.

pip install psycopg2-binary

echo.
echo ✓ PostgreSQL driver installed!
echo.
echo To use PostgreSQL locally:
echo 1. Install PostgreSQL from https://www.postgresql.org/download/
echo 2. Create database: createdb mine_safety_db
echo 3. Update .env with: DATABASE_URL=postgresql://username:password@localhost:5432/mine_safety_db
echo.
echo For Render deployment, PostgreSQL is auto-configured!
echo.
pause
