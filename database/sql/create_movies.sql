PRAGMA temp_store = 2;              -- Store temp table in memory, not on disk

PRAGMA foreign_keys = OFF;          -- Disable the enforcement of foreign key constraints.

DROP TABLE IF EXISTS movies;

PRAGMA foreign_keys = ON;           -- Enable the enforcement of foreign key constraints.

CREATE TABLE IF NOT EXISTS movies
(
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       VARCHAR(100) NOT NULL,
  director   VARCHAR(100) NOT NULL,
  gender     VARCHAR(50)  NOT NULL,
  duration   VARCHAR(10)  NOT NULL,
  --  SQLite does not have a separate Boolean storage class. Instead, Boolean values are stored as integers 0 (false) and 1 (true).
  available  INTEGER      NOT NULL DEFAULT 0,
  created_on TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT  INTO movies
(
        name,
        director,
        gender,
        duration,
        available
)
VALUES
(
        'The Tomorrow War',
        'Chris McKay',
        'Science fiction',
        '2h 20min',
        1
);
