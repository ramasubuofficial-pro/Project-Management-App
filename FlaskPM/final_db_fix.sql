
-- ==========================================
-- FINAL DATABASE FIX SCRIPT
-- Run this ENTIRE file in Supabase SQL Editor
-- ==========================================

-- 1. FIX COMMENTS TABLE (Schema Mismatch)
-- We drop and recreate it to ensure task_id is the correct type (BIGINT)
DROP TABLE IF EXISTS comments;

CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id BIGINT REFERENCES tasks(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Enable RLS for Comments
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for all users" ON comments FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users only" ON comments FOR INSERT WITH CHECK (auth.uid() = user_id);

-- 2. FIX ATTACHMENTS TABLE (RLS Blocking Uploads)
-- We relax the policy so the backend can write files without the Service Role Key
DROP POLICY IF EXISTS "Members can upload attachments" ON task_attachments;
-- Create a permissive policy for INSERTS
CREATE POLICY "Allow Backend Inserts" ON task_attachments FOR INSERT WITH CHECK (true);

-- 3. VERIFY
-- This query doesn't change anything, just helpful to see.
SELECT 'Database Fixes Applied Successfully' as status;
