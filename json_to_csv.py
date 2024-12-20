import json
import csv

def flatten_json(json_obj, parent_name='', separator=' > '):
    """
    Achata um JSON hierárquico em uma lista de dicionários.
    """
    flat_data = []
    
    def recurse(obj, parent_name):
        if isinstance(obj, dict):
            if 'children' in obj:
                # Concatena o nome atual ao nome do pai
                current_name = f"{parent_name}{separator}{obj['name']}" if parent_name else obj['name']
                for child in obj['children']:
                    recurse(child, current_name)
            else:
                # Coleta as coordenadas se disponíveis
                coordinates = obj.get('geometry', {}).get('coordinates', [])
                flat_data.append({
                    'path': parent_name,
                    'name': obj.get('name'),
                    'id': obj.get('id'),
                    'latitude': coordinates[1] if len(coordinates) > 1 else None,
                    'longitude': coordinates[0] if len(coordinates) > 1 else None
                })
    
    recurse(json_obj, parent_name)
    return flat_data

def json_to_csv_hierarchical(json_file, csv_file):
    try:
        # Lê o arquivo JSON com UTF-8
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Achata o JSON
        flat_data = flatten_json(data)
        
        # Verifica se há dados para converter
        if flat_data:
            # Abre o arquivo CSV para escrita com UTF-8
            with open(csv_file, 'w', encoding='utf-8', newline='') as csvfile:
                # Define os campos do CSV
                fieldnames = ['path', 'name', 'id', 'latitude', 'longitude']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Escreve os cabeçalhos
                writer.writeheader()
                # Escreve os dados
                writer.writerows(flat_data)

            print(f"Arquivo CSV '{csv_file}' gerado com sucesso.")
        else:
            print("O JSON não contém dados válidos para exportar.")
    except Exception as e:
        print(f"Erro ao converter JSON para CSV: {e}")

# Uso do script
json_file = 'metadata.json'  # Substitua pelo caminho do seu arquivo JSON
csv_file = 'output_with_coordinates.csv'              # Substitua pelo caminho onde deseja salvar o CSV

json_to_csv_hierarchical(json_file, csv_file)
