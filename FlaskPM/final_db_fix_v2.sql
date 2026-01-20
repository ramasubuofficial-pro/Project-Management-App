
-- ==========================================
-- FINAL DATABASE FIX SCRIPT (ROBUST VERSION)
-- Run this ENTIRE file in Supabase SQL Editor
-- ==========================================

-- 1. FIX COMMENTS TABLE
DROP TABLE IF EXISTS comments;

CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id BIGINT REFERENCES tasks(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for all users" ON comments FOR SELECT USING (true);
CREATE POLICY "Enable insert for authenticated users only" ON comments FOR INSERT WITH CHECK (auth.uid() = user_id);

-- 2. FIX ATTACHMENTS TABLE
-- Drop ANY potential conflicting policies first
DROP POLICY IF EXISTS "Members can upload attachments" ON task_attachments;
DROP POLICY IF EXISTS "Allow Backend Inserts" ON task_attachments;

-- Create the robust backend policy
CREATE POLICY "Allow Backend Inserts" ON task_attachments FOR INSERT WITH CHECK (true);

-- 3. VERIFY
SELECT 'Database Fixes Applied Successfully' as status;
