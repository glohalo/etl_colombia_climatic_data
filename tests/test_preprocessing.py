import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import pandas as pd
import zipfile
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
from src.preprocessing import extract_zip_file, get_csv_files, load_csv_data, filtering_data

class TestPreprocessing(unittest.TestCase):

    @patch('src.preprocessing.zipfile.ZipFile')
    def test_extract_zip_file(self, mock_zipfile):
        # Setup
        file_path = 'dummy.zip'
        output_path_bronze = 'output/'

        # Mock the zipfile.ZipFile context manager
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        # Call the function
        extract_zip_file(file_path, output_path_bronze)

        # Assertions
        mock_zip.extractall.assert_called_once_with(output_path_bronze)
        print(f"Extracted content of {file_path} to {output_path_bronze}")

    @patch('os.listdir')
    @patch('src.preprocessing.extract_zip_file')
    @patch('os.makedirs')
    def test_get_csv_files(self, mock_makedirs, mock_extract_zip_file, mock_listdir):
        # Setup
        file_path = 'dummy.zip'
        output_path_bronze = 'output/'
        mock_listdir.return_value = ['file1.csv', 'file2.txt', 'file3.csv']

        # Call the function
        csv_files = get_csv_files(file_path, output_path_bronze)

        # Assertions
        mock_makedirs.assert_called_once_with(output_path_bronze, exist_ok=True)
        mock_extract_zip_file.assert_called_once_with(file_path, output_path_bronze)
        self.assertEqual(csv_files, ['file1.csv', 'file3.csv'])
        print(csv_files)

    @patch('src.preprocessing.get_csv_files')
    @patch('pandas.read_csv')
    def test_load_csv_data(self, mock_read_csv, mock_get_csv_files):
        # Setup
        output_path_bronze = 'output/'
        file_path = 'dummy.zip'
        mock_get_csv_files.return_value = ['file1.csv', 'file2.csv']
        mock_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        mock_read_csv.return_value = mock_df

        # Call the function
        data = load_csv_data(output_path_bronze, file_path)

        # Assertions
        mock_get_csv_files.assert_called_once_with(file_path, output_path_bronze)
        mock_read_csv.assert_any_call(os.path.join(output_path_bronze, 'file1.csv'))
        mock_read_csv.assert_any_call(os.path.join(output_path_bronze, 'file2.csv'))
        self.assertTrue(data.equals(mock_df))
        print(data)

    @patch('src.preprocessing.load_csv_data')
    @patch('pandas.DataFrame.to_csv')
    def test_filtering_data(self, mock_to_csv, mock_load_csv_data):
        # Setup
        output_path_bronze = 'output_bronze/'
        output_path_silver = 'output_silver/'
        file_path = 'dummy.zip'
        mock_df = pd.DataFrame({
            'Fecha': ['2024-01-01', '2023-01-01'],
            'Valor': [10, 20],
            'NivelAprobacion': ['Preliminar', 'Definitivo']
        })
        mock_load_csv_data.return_value = mock_df

        # Call the function
        temperature = filtering_data(output_path_bronze, output_path_silver, file_path)

        # Assertions
        mock_load_csv_data.assert_called_once_with(output_path_bronze, file_path)
        mock_to_csv.assert_called_once_with(f'{output_path_silver}dailymaxtemperature.csv', index=False)
        self.assertTrue('Fecha' in temperature.columns)
        self.assertTrue('Valor' in temperature.columns)
        print(temperature)

if __name__ == '__main__':
    unittest.main()