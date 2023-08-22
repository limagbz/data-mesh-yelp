CREATE TABLE IF NOT EXISTS business (
    id TEXT PRIMARY KEY CHECK(LENGTH(id) <= 22),
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL CHECK(LENGTH(state) <= 3),
    postal_code TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    is_open BOOLEAN NOT NULL,
    attributes JSON,
    categories TEXT,
    hours JSON
);
