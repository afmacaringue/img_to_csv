import os
from PIL import Image
import pillow_heif
import piexif

def preserve_metadata_and_convert_heic_to_jpg(input_folder, output_folder):
    """Converte imagens HEIC para JPG, preservando os metadados."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".heic"):
            heic_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".jpg")
            try:
                # Lê o arquivo HEIC
                heif_file = pillow_heif.read_heif(heic_path)
                img = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data)

                # Extrai os metadados EXIF
                exif_data = heif_file.metadata.get("exif", None)

                # Salva como JPG, mantendo os metadados
                img.save(output_path, "JPEG")
                if exif_data:
                    piexif.insert(exif_data, output_path)

                print(f"Convertido com metadados: {filename} -> {output_path}")
            except Exception as e:
                print(f"Erro ao converter {filename}: {e}")

# Uso do algoritmo
input_folder = "Centro de Saúde de Luanda"
output_folder = "Centro de Saúde de Luanda"
preserve_metadata_and_convert_heic_to_jpg(input_folder, output_folder)

print("Conversão com preservação de metadados concluída!")
