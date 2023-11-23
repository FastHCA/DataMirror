CREATE TABLE "users" (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50),
  email VARCHAR(100),
  age INTEGER
);

CREATE INDEX IF NOT EXISTS "idx_users_name" ON "users" ("name");
