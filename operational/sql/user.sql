CREATE TABLE IF NOT EXISTS users (
   id VARCHAR(22) PRIMARY KEY,
   name VARCHAR NOT NULL,
   yelping_since DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS elite_members (
   user_id VARCHAR(22) REFERENCES users(id),
   year integer NOT NULL
);

CREATE TABLE IF NOT EXISTS friends (
    previous_user VARCHAR(22) REFERENCES users(id),
    next_user VARCHAR(22) REFERENCES users(id),
    PRIMARY KEY(previous_user, next_user)
);
