-- CreateTrigger: Update Group lastMessageAt when a new message is created
CREATE TRIGGER update_group_last_message_at
AFTER INSERT ON Message
FOR EACH ROW
BEGIN
  UPDATE `Group` SET lastMessageAt = NOW() WHERE id = NEW.groupId;
END;

-- CreateTrigger: user can not send empty message 
CREATE TRIGGER empty_message
BEFORE INSERT ON Message
FOR EACH ROW
BEGIN
  IF (NEW.content IS NULL OR NEW.content = '') THEN
     RAISE EXCEPTION 'can not send empty message';
  END IF;  
END;


CREATE PROCEDURE private_chat(
IN first_user INT
IN second_user INT)
BEGIN
  SELECT *
  FROM Message
  WHERE (senderId = first_user AND receiverId = second_user)
  OR
  (senderId = second_user AND receiverId = first_user);
END;
