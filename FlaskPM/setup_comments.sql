
-- Rebuild Comments Table
-- REASON: The 'task_id' must be BIGINT to match your 'tasks' table.
-- WARNING: This will delete existing comments!

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
