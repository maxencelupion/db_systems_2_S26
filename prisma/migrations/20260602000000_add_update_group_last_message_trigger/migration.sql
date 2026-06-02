-- CreateTrigger: Update Group lastMessageAt when a new message is created
CREATE TRIGGER update_group_last_message_at
AFTER INSERT ON Message
FOR EACH ROW
BEGIN
  UPDATE `Group` SET lastMessageAt = NOW() WHERE id = NEW.groupId;
END;
