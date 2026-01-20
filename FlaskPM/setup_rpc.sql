
-- Create a Secure Function to bypass RLS for uploads
CREATE OR REPLACE FUNCTION upload_attachment_secure(
    p_task_id BIGINT,
    p_user_id UUID,
    p_file_name TEXT,
    p_file_url TEXT,
    p_file_type TEXT
) 
RETURNS JSONB 
LANGUAGE plpgsql 
SECURITY DEFINER -- Run as database owner (bypasses RLS)
AS $$
DECLARE
    new_record JSONB;
BEGIN
    INSERT INTO task_attachments (task_id, user_id, file_name, file_url, file_type)
    VALUES (p_task_id, p_user_id, p_file_name, p_file_url, p_file_type)
    RETURNING to_jsonb(task_attachments.*) INTO new_record;
    
    RETURN new_record;
END;
$$;
