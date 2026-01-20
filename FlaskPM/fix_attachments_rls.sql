
-- Relax RLS Policy for task_attachments
-- This ensures the Flask Backend can insert records without needing a specific database user session.

-- 1. Drop the strict policy
DROP POLICY IF EXISTS "Members can upload attachments" ON task_attachments;

-- 2. Create a permissive policy for INSERTS
-- (Security is handled by the Flask API authentication check)
CREATE POLICY "Allow Backend Inserts" ON task_attachments FOR INSERT WITH CHECK (true);

-- 3. Verify RLS is enabled (It should be, but good to ensure)
ALTER TABLE task_attachments ENABLE ROW LEVEL SECURITY;
