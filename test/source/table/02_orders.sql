CREATE TABLE "orders" (
  id SERIAL PRIMARY KEY,
  user_id INTEGER,
  product VARCHAR(100),
  quantity INTEGER,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE INDEX IF NOT EXISTS "idx_orders_product" ON "orders" ("product");
