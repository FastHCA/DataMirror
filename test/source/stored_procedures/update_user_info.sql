-- This is just an example and doesn't have any practical effect.
CREATE OR REPLACE FUNCTION update_user_info()
  RETURNS TRIGGER
AS $$
BEGIN
  UPDATE users
  SET name = (SELECT name FROM users WHERE id = NEW.user_id),
      email = (SELECT email FROM users WHERE id = NEW.user_id),
      age = (SELECT age FROM users WHERE id = NEW.user_id)
  WHERE id = NEW.user_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;