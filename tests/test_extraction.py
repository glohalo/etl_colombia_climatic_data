import os
from datetime import timedelta, datetime
from unittest.mock import MagicMock, patch
from src.data_extraction import (scroll_down,wait_for_download,handle_finder_dialog,
    handle_terms_and_conditions_and_download,
)

def test_scroll_down():
    driver = MagicMock()
    TimeWait = 10

    scroll_down(driver, TimeWait)

    driver.execute_script.assert_called()

def test_wait_for_download(tmp_path):
    path = tmp_path
    TimeWait = 10

    # Create a dummy file to simulate download completion
    dummy_file = path / "report.zip"
    dummy_file.touch()
    wait_for_download(path, TimeWait)
    assert dummy_file.exists()

@patch('subprocess.run')
def test_handle_finder_dialog(mock_subprocess_run):
    base_dir = os.path.abspath(os.path.join(os.getcwd(), '.', '..'))
    path = os.path.join(base_dir, 'data', 'bronze')
    file_name = "/report.zip"
    handle_finder_dialog(path, file_name)
    mock_subprocess_run.assert_called_once()

@patch('src.data_extraction.handle_terms_and_conditions')
@patch('src.data_extraction.handle_accept_button')
@patch('src.data_extraction.variable_deparment_and_date_set_up')
@patch('src.data_extraction.webdriver.Safari')
def test_handle_terms_and_conditions_and_download(mock_safari, mock_variable_deparment_and_date_set_up, mock_handle_accept_button, mock_handle_terms_and_conditions, tmp_path):
    # Setup
    driver = MagicMock()
    mock_safari.return_value = driver
    path = tmp_path
    variable = "Temperatura"
    param = "Temperatura máxima diaria"
    departamento = "Atlantico"
    code = "29035080"
    date_ini = "01/01/2000"
    date_fin = (datetime.today() - timedelta(days=20)).strftime("%d/%m/%Y")

    # Mock the handle_terms_and_conditions and handle_accept_button methods to return True
    mock_handle_terms_and_conditions.return_value = True
    mock_handle_accept_button.return_value = True

    # Call the function
    handle_terms_and_conditions_and_download(path, variable, param, departamento, code, date_ini, date_fin)

    # Assertions
    mock_safari.assert_called_once()  # Ensure Safari was instantiated
    driver.get.assert_called_once_with("http://dhime.ideam.gov.co/atencionciudadano/")
    mock_handle_terms_and_conditions.assert_called_once_with(driver, 60)
    mock_handle_accept_button.assert_called_once_with(driver, 60)
    mock_variable_deparment_and_date_set_up.assert_called_once_with(driver, path, variable, param, departamento, code, date_ini, date_fin, retries=1)
    driver.quit.assert_called_once()