import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from src.orchestrator import main

base_dir = os.path.abspath(os.path.join(os.getcwd(), '.', '..'))
path_bronze = os.path.join(base_dir, 'data', 'bronze')
path_silver = os.path.join(base_dir, 'data', 'silver')
file_name = 'report.zip'
file_path = os.path.join(path_bronze, file_name)
print(file_path)

class TestOrchestrator(unittest.TestCase):

    @patch('src.orchestrator.filtering_data')
    @patch('src.orchestrator.handle_terms_and_conditions_and_download')
    def test_orchestrator(self, mock_handle_terms_and_conditions_and_download, mock_filtering_data):
        # Setup
        mock_handle_terms_and_conditions_and_download.return_value = None
        mock_filtering_data.return_value = None

        # Call the main function
        main()

        # Assertions
        mock_handle_terms_and_conditions_and_download.assert_called_once_with(
            path=path_bronze,
            variable="Temperatura",
            param='Temperatura máxima diaria',
            departamento="Atlantico",
            code="29035080",
            date_ini="01/01/2000",
            date_fin=(datetime.today() - timedelta(days=20)).strftime("%d/%m/%Y")
        )
        mock_filtering_data.assert_called_once_with(
            path_bronze,
            path_silver,
            file_path
        )

if __name__ == '__main__':
    unittest.main()