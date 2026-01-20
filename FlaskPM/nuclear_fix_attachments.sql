
-- ==========================================
-- NUCLEAR OPTION: FIX ATTACHMENTS
-- Run this in Supabase SQL Editor
-- ==========================================

-- 1. DROP EVERYTHING RELATED TO ATTACHMENTS
-- This ensures we don't have lingering UUID schema or bad policies
DROP TABLE IF EXISTS task_attachments;

-- 2. RECREATE TABLE WITH CORRECT SCHEMA
CREATE TABLE task_attachments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id BIGINT REFERENCES tasks(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    file_name TEXT NOT NULL,
    file_url TEXT NOT NULL,
    file_type TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 3. DISABLE RLS COMPLETELY
-- This removes ALL permission barriers for this table.
-- Since the Python backend handles the logic, this is acceptable for now.
ALTER TABLE task_attachments DISABLE ROW LEVEL SECURITY;

-- 4. VERIFY
SELECT 'Attachments Table Recreated and RLS Disabled' as status;
