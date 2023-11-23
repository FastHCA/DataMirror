CREATE TRIGGER update_user_info_trigger
AFTER INSERT ON orders
FOR EACH ROW
EXECUTE FUNCTION update_user_info();
