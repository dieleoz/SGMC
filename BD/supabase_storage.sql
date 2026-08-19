-- ============================================================================
-- SGMC v2 — BUCKET DE SUPABASE STORAGE Y POLÍTICAS DE ACCESO
-- Implementación de ESPEC-013 / ORDEN-013
-- ============================================================================

-- 1. Crear el bucket 'evidencias-sgmc' si no existe
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'evidencias-sgmc',
    'evidencias-sgmc',
    true,
    5242880, -- 5 MB máximo por archivo (las fotos WebP ocupan < 150 KB)
    ARRAY['image/webp', 'image/png', 'image/jpeg']
)
ON CONFLICT (id) DO UPDATE SET
    public = true,
    file_size_limit = 5242880,
    allowed_mime_types = ARRAY['image/webp', 'image/png', 'image/jpeg'];

-- 2. Políticas RLS en storage.objects para el bucket evidencias-sgmc

DROP POLICY IF EXISTS "Lectura publica evidencias" ON storage.objects;
CREATE POLICY "Lectura publica evidencias" ON storage.objects
FOR SELECT USING (bucket_id = 'evidencias-sgmc');

DROP POLICY IF EXISTS "Subida de evidencias autorizada" ON storage.objects;
CREATE POLICY "Subida de evidencias autorizada" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'evidencias-sgmc');

DROP POLICY IF EXISTS "Actualizacion evidencias" ON storage.objects;
CREATE POLICY "Actualizacion evidencias" ON storage.objects
FOR UPDATE USING (bucket_id = 'evidencias-sgmc');
