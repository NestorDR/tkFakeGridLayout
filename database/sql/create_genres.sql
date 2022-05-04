PRAGMA temp_store = 2;              -- Store temp table in memory, not on disk

PRAGMA foreign_keys = OFF;          -- Disable the enforcement of foreign key constraints.

DROP TABLE IF EXISTS genres;

PRAGMA foreign_keys = ON;           -- Enable the enforcement of foreign key constraints.

CREATE TABLE IF NOT EXISTS genres
(
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       VARCHAR(100) NOT NULL,
  created_on TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT  INTO genres (name) 
VALUES  ('Action'),
        ('Adventure'),
        ('Comedy'),
        ('Crime and mystery'),
        ('Fantasy'),
        ('Historical'),
        ('Horror'),
        ('Romance'), 
        ('Satire'),
        ('Science fiction'),
        ('Thriller'), 
        ('Western')
