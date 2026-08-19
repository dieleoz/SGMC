import { supabase } from "./supabase";

/**
 * Convierte un data URL base64 en un Blob
 */
function base64ToBlob(base64Data: string): Blob {
  const parts = base64Data.split(";base64,");
  const contentType = parts[0].split(":")[1] || "image/webp";
  const raw = window.atob(parts[1]);
  const rawLength = raw.length;
  const uInt8Array = new Uint8Array(rawLength);

  for (let i = 0; i < rawLength; ++i) {
    uInt8Array[i] = raw.charCodeAt(i);
  }

  return new Blob([uInt8Array], { type: contentType });
}

/**
 * Sube una fotografía comprimida en WebP al bucket de evidencias
 */
export async function subirFotoEvidencia(
  base64Data: string,
  otid: string,
  fotoId: string
): Promise<string | null> {
  try {
    const blob = base64ToBlob(base64Data);
    const date = new Date();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const filePath = `fotos/${year}/${month}/${otid}_${fotoId}.webp`;

    const { data, error } = await supabase.storage
      .from("evidencias-sgmc")
      .upload(filePath, blob, {
        contentType: "image/webp",
        upsert: true,
      });

    if (error) {
      console.error("[Storage] Error subiendo fotografía:", error);
      return null;
    }

    const { data: urlData } = supabase.storage
      .from("evidencias-sgmc")
      .getPublicUrl(filePath);

    return urlData.publicUrl;
  } catch (err) {
    console.error("[Storage] Excepción en subida de foto:", err);
    return null;
  }
}

/**
 * Sube una firma manuscrita en PNG al bucket de evidencias
 */
export async function subirFirmaDigital(
  base64Data: string,
  otid: string
): Promise<string | null> {
  try {
    const blob = base64ToBlob(base64Data);
    const date = new Date();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const filePath = `firmas/${year}/${month}/${otid}_firma.png`;

    const { data, error } = await supabase.storage
      .from("evidencias-sgmc")
      .upload(filePath, blob, {
        contentType: "image/png",
        upsert: true,
      });

    if (error) {
      console.error("[Storage] Error subiendo firma:", error);
      return null;
    }

    const { data: urlData } = supabase.storage
      .from("evidencias-sgmc")
      .getPublicUrl(filePath);

    return urlData.publicUrl;
  } catch (err) {
    console.error("[Storage] Excepción en subida de firma:", err);
    return null;
  }
}
