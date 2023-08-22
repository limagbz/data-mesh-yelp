CREATE TABLE IF NOT EXISTS reviews (
   id VARCHAR(22) PRIMARY KEY,
   business_id VARCHAR(22) NOT NULL,
   user_id VARCHAR(22) NOT NULL,
   stars SMALLINT NOT NULL CHECK(stars >= 0 AND stars <= 5),
   review_date DATE NOT NULL,
   content VARCHAR NOT NULL,
   useful_count INT NOT NULL,
   funny_count INT NOT NULL,
   cool_count INT NOT NULL
);

CREATE TABLE IF NOT EXISTS tips (
   business_id VARCHAR(22) NOT NULL,
   user_id VARCHAR(22) NOT NULL,
   tips_date DATE NOT NULL,
   content VARCHAR NOT NULL,
   compliment_count INT NOT NULL
);
