CREATE TABLE IF NOT EXISTS livros (
    id BIGSERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE livros ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Usuário ver seus próprios livros"
    ON livros FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Usuário insere seus próprios livros"
    ON livros FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Usuário atualiza seus próprios livros"
    ON livros FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Usuário deleta seus próprios livros"
    ON livros FOR DELETE USING (auth.uid() = user_id);

CREATE INDEX IF NOT EXISTS idx_livros_user_id ON livros(user_id);
CREATE INDEX IF NOT EXISTS idx_livros_created_at ON livros(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_livros_titulo ON livros USING gin(to_tsvector('portuguese', titulo));

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END; $$;

DROP TRIGGER IF EXISTS update_livros_updated_at ON livros;
CREATE TRIGGER update_livros_updated_at
BEFORE UPDATE ON livros
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();