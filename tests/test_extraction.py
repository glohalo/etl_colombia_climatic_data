import pytest
import os
import time
from unittest.mock import MagicMock, patch
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from extraction import scroll_down, wait_for_download, handle_finder_dialog, download_hydrometeorological_data

def test_scroll_down():
    driver = MagicMock()
    TimeWait = 10
    element = MagicMock()
    WebDriverWait(driver, TimeWait).until.return_value = element

    scroll_down(driver, TimeWait)

    driver.execute_script.assert_called_with("arguments[0].scrollIntoView(true);", element)

def test_wait_for_download(tmp_path):
    path = tmp_path
    TimeWait = 10

    # Create a dummy file to simulate download completion
    dummy_file = path / "dummy_file.txt"
    dummy_file.touch()

    wait_for_download(path, TimeWait)

    assert dummy_file.exists()

def test_handle_finder_dialog():
    path = "/Users/gloriacarrascal/master/research_data/dm_project/data/bronze/"
    file_name = "report.zip"

    with patch('subprocess.run') as mock_run:
        handle_finder_dialog(path, file_name)
        mock_run.assert_called_once()

@patch('extraction.handle_finder_dialog')
@patch('extraction.wait_for_download')
@patch('selenium.webdriver.Safari')
def test_download_hydrometeorological_data(mock_safari, mock_wait_for_download, mock_handle_finder_dialog, tmp_path):
    driver = mock_safari.return_value
    path = tmp_path
    variable = "Precipitación"
    param = "Día pluviométrico (convencional)"
    departamento = "Antioquia"
    code = "27015070"
    date_ini = "01/01/2000"
    date_fin = "31/12/2020"

    download_hydrometeorological_data(driver, path, variable, param, departamento, code, date_ini, date_fin)

    mock_safari.assert_called_once()
    mock_wait_for_download.assert_called_once_with(path, 40)
    mock_handle_finder_dialog.assert_called_once_with(path, "report.zip")

if __name__ == "__main__":
    pytest.main()

