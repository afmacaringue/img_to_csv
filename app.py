import os
import csv
from PIL import Image, ExifTags
import pillow_heif  # Adiciona suporte ao formato HEIC

def get_exif_data(image):
    """Extrai os dados EXIF de uma imagem."""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            tag_name = ExifTags.TAGS.get(tag, tag)
            if tag_name == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_tag = ExifTags.GPSTAGS.get(t, t)
                    gps_data[sub_tag] = value[t]
                exif_data[tag_name] = gps_data
            else:
                exif_data[tag_name] = value
    return exif_data

def get_lat_lon(gps_info):
    """Converte os dados GPS para latitude e longitude."""
    def convert_to_degrees(value):
        d, m, s = value
        return d + (m / 60.0) + (s / 3600.0)
    
    if not gps_info:
        return None, None

    lat = gps_info.get("GPSLatitude")
    lat_ref = gps_info.get("GPSLatitudeRef")
    lon = gps_info.get("GPSLongitude")
    lon_ref = gps_info.get("GPSLongitudeRef")

    if lat and lon and lat_ref and lon_ref:
        lat = convert_to_degrees(lat)
        if lat_ref != "N":
            lat = -lat

        lon = convert_to_degrees(lon)
        if lon_ref != "E":
            lon = -lon

        return lat, lon
    return None, None

def process_images(folder_path, output_csv):
    """Lê as fotos da pasta e cria um CSV com latitude e longitude."""
    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["File Name", "Latitude", "Longitude"])

        for filename in os.listdir(folder_path):
            if filename.lower().endswith((".jpg", ".jpeg", ".png", ".heic")):
                image_path = os.path.join(folder_path, filename)
                try:
                    # Abre a imagem, suportando HEIC
                    if filename.lower().endswith(".heic"):
                        heif_file = pillow_heif.read_heif(image_path)
                        img = Image.frombytes(
                            heif_file.mode, heif_file.size, heif_file.data
                        )
                    else:
                        img = Image.open(image_path)

                    exif_data = get_exif_data(img)
                    gps_info = exif_data.get("GPSInfo")
                    lat, lon = get_lat_lon(gps_info)
                    writer.writerow([filename, lat, lon])
                except Exception as e:
                    print(f"Erro ao processar {filename}: {e}")

# Uso do algoritmo
folder_path = "STP/PS Aeroporto (PRPGRPT)"
output_csv = "fotos_com_coordenadas.csv"
process_images(folder_path, output_csv)

print(f"Arquivo CSV gerado: {output_csv}")
