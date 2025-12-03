CREATE SCHEMA IF NOT EXISTS app;

CREATE SCHEMA IF NOT EXISTS events;

DO
$$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles WHERE rolname = 'app_user'
    ) THEN
        CREATE ROLE app_user LOGIN PASSWORD 'app_password';
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON SCHEMA app TO app_user;
GRANT ALL PRIVILEGES ON SCHEMA events TO app_user;

CREATE TABLE IF NOT EXISTS app.health_check (
    id SERIAL PRIMARY KEY,
    status VARCHAR(20) NOT NULL DEFAULT 'ok',
    checked_at TIMESTAMP NOT NULL DEFAULT NOW()
);

app_user / app_password
