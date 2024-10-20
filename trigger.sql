CREATE TRIGGER posts_fts_delete
AFTER DELETE ON posts
FOR EACH ROW
BEGIN
    DELETE FROM posts_fts WHERE id = OLD.id;
END
;