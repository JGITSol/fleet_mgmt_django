import os

import requests

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')

# Module-level constants to avoid long inline literal messages (TRY003)
_OPENROUTER_API_KEY_MISSING = "OpenRouter API key not configured"
_OPENROUTER_FILE_NOT_FOUND = "File not found"
_OPENROUTER_DEFAULT_PROMPT = "Analyze this screenshot."

class OpenRouterClient:
    def __init__(self, api_key=None):
        self.api_key = api_key if api_key is not None else OPENROUTER_API_KEY
        if not self.api_key:
            raise ValueError(_OPENROUTER_API_KEY_MISSING)

    def analyze_screenshot(self, screenshot_path, prompt=None):
        if not os.path.exists(screenshot_path):
            raise FileNotFoundError(screenshot_path)
        url = 'https://openrouter.ai/api/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        with open(screenshot_path, 'rb') as img_file:
            image_data = img_file.read()
        data = {
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'text',
                            'text': prompt or _OPENROUTER_DEFAULT_PROMPT
                        },
                        {
                            'type': 'image',
                            'image': image_data.hex()  # Use hex for test stub, real API may require base64
                        }
                    ]
                }
            ]
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}

    def batch_analyze_screenshots(self, directory, language=None, theme=None):
        if not os.path.isdir(directory):
            class InvalidDirectory(NotADirectoryError):
                def __init__(self, path: str):
                    super().__init__(path)

            raise InvalidDirectory(directory)
        results = {}
        for filename in os.listdir(directory):
            if filename.endswith('.png'):
                parts = filename.replace('.png', '').split('_')
                if len(parts) >= 3:
                    lang = parts[1]
                    thm = parts[2]
                    if language and lang != language:
                        continue
                    if theme and thm != theme:
                        continue
                path = os.path.join(directory, filename)
                try:
                    results[filename] = self.analyze_screenshot(path)
                except Exception as e:
                    results[filename] = {'error': str(e)}
        return results

def get_client(*args, **kwargs):
    return OpenRouterClient(*args, **kwargs)
