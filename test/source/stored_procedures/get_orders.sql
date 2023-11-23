CREATE OR REPLACE FUNCTION get_orders()
  RETURNS TABLE (
    id INTEGER,
    user_id INTEGER,
    product VARCHAR(100),
    quantity INTEGER
  )
AS $$
BEGIN
  RETURN QUERY SELECT id, user_id, product, quantity FROM orders;
END;
$$ LANGUAGE plpgsql;
