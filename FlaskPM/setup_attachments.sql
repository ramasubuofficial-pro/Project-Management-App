
-- Create task_attachments table
-- UPDATED: task_id is BIGINT to match the existing 'tasks' table schema in Supabase.
CREATE TABLE IF NOT EXISTS task_attachments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id BIGINT REFERENCES tasks(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    file_name TEXT NOT NULL,
    file_url TEXT NOT NULL,
    file_type TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Enable RLS (optional but recommended)
ALTER TABLE task_attachments ENABLE ROW LEVEL SECURITY;

-- Policy: Everyone can view
CREATE POLICY "Everyone can view attachments" ON task_attachments
    FOR SELECT USING (true);

-- Policy: Members can insert
CREATE POLICY "Members can upload attachments" ON task_attachments
    FOR INSERT WITH CHECK (auth.uid() = user_id);
