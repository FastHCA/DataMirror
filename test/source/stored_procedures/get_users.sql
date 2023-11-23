CREATE OR REPLACE FUNCTION get_users()
  RETURNS TABLE (
    id INTEGER,
    name VARCHAR(50),
    email VARCHAR(100),
    age INTEGER
  )
AS $$
BEGIN
  RETURN QUERY SELECT id, name, email, age FROM users;
END;
$$ LANGUAGE plpgsql;
