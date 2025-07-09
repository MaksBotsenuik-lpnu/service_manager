-- Initialize database with extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create database if it doesn't exist (this will be handled by POSTGRES_DB env var)
-- The database 'computer_service' will be created automatically by PostgreSQL container 