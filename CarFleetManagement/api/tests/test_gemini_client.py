import pytest
from unittest.mock import patch, MagicMock
from api.gemini_client import GeminiClient, get_client
import io

@pytest.fixture
def fake_api_key(monkeypatch):
    monkeypatch.setenv('GEMINI_API_KEY', 'fake-key')
    return 'fake-key'

@patch('api.gemini_client.os.getenv', return_value='fake-key')
@patch('api.gemini_client.genai')
def test_gemini_client_init_with_env_key(mock_genai, mock_getenv):
    client = GeminiClient()
    assert client.api_key == 'fake-key'
    mock_genai.configure.assert_called_with(api_key='fake-key')

@patch('api.gemini_client.os.getenv', return_value='fake-key')
@patch('api.gemini_client.genai')
def test_gemini_client_init_with_explicit_key(mock_genai, mock_getenv):
    client = GeminiClient(api_key='explicit-key')
    assert client.api_key == 'explicit-key'
    mock_genai.configure.assert_called_with(api_key='explicit-key')

@patch('api.gemini_client.os.getenv', return_value='fake-key')
@patch('api.gemini_client.Image')
def test_resize_image_downscales_large_image(mock_image, mock_getenv):
    # Setup
    img_mock = MagicMock()
    img_mock.width = 3000
    img_mock.height = 2000
    mock_image.open.return_value.__enter__.return_value = img_mock
    client = GeminiClient(api_key='test')
    # Act
    result = client._resize_image('dummy/path.png')
    # Assert
    img_mock.thumbnail.assert_called()
    assert isinstance(result, io.BytesIO)

@patch('api.gemini_client.os.getenv', return_value='fake-key')
@patch('api.gemini_client.Image')
def test_resize_image_no_resize_needed(mock_image, mock_getenv):
    img_mock = MagicMock()
    img_mock.width = 1000
    img_mock.height = 800
    mock_image.open.return_value.__enter__.return_value = img_mock
    client = GeminiClient(api_key='test')
    result = client._resize_image('dummy/path.png')
    img_mock.thumbnail.assert_not_called()
    assert isinstance(result, io.BytesIO)

@patch('api.gemini_client.os.getenv', return_value='fake-key')
@patch('api.gemini_client.genai')
def test_analyze_screenshot_api_call(mock_genai, mock_getenv):
    client = GeminiClient(api_key='test')
    # Mock _resize_image to avoid actual file IO
    client._resize_image = MagicMock(return_value=io.BytesIO(b'fakeimg'))
    # Mock os.path.exists to always return True
    with patch('api.gemini_client.os.path.exists', return_value=True):
        # Mock genai.GenerativeModel and its generate_content
        mock_model = MagicMock()
        mock_model.generate_content.return_value.text = "Gemini analysis result"
        mock_genai.GenerativeModel.return_value = mock_model
        result = client.analyze_screenshot('dummy/path.png')
    assert "choices" in result
    assert result["choices"][0]["message"]["content"] == "Gemini analysis result"

@patch('api.gemini_client.os.getenv', return_value='fake-key')
@patch('api.gemini_client.genai')
def test_get_client_returns_instance(mock_genai, mock_getenv):
    client = get_client()
    assert isinstance(client, GeminiClient)
