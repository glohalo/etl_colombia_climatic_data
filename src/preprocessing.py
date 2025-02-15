import pandas as pd
import time
import os
import zipfile

def extract_zip_file(file_path, output_path_bronze):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_path_bronze)
            print(f"Extracted content of {file_path} to {output_path_bronze}")
    except zipfile.BadZipFile:
        print(f'Error: {file_path} is not a valid zip file.')
    except Exception as e:
        print(f'An error ocurried: {e}')

def get_csv_files(file_path, output_path_bronze):
    os.makedirs(output_path_bronze, exist_ok=True)
    extract_zip_file(file_path, output_path_bronze)
    data_path = os.listdir(output_path_bronze)
    csv_files = [file for file in data_path if file.endswith('.csv')]
    print(csv_files)
    return csv_files
def load_csv_data(output_path_bronze, file_path):
    csv_files = get_csv_files(file_path, output_path_bronze)
    data = []
    for file in csv_files:
        data_csv = pd.read_csv(os.path.join(output_path_bronze, file))
        data.append(data_csv)
    print(data)
    return data[0]
def filtering_data(output_path_bronze:str, output_path_silver, file_path:str):
    temperature = load_csv_data(output_path_bronze, file_path)
    print(temperature.NivelAprobacion.unique())
    #most of the data "Preliminar" is from the the 2024
    # "Definitivo" corresponds to the last years
    #reanrranging values
    temperature = temperature[['Fecha', 'Valor']]
    temperature.loc[:,'Fecha'] = pd.to_datetime(temperature['Fecha'], errors='coerce')
    #Format to datetime
    temperature.loc[:,'Fecha'] = pd.to_datetime(temperature['Fecha'])
    temperature.to_csv(f'{output_path_silver}/dailymaxtemperature.csv', index=False)
    return temperature

