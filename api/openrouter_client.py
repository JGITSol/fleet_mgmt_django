import os
import requests

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')

class OpenRouterClient:
    def __init__(self, api_key=None):
        self.api_key = api_key if api_key is not None else OPENROUTER_API_KEY
        if not self.api_key:
            raise ValueError('API key is required')

    def analyze_screenshot(self, screenshot_path, prompt=None):
        if not os.path.exists(screenshot_path):
            raise FileNotFoundError(f"File not found: {screenshot_path}")
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
                            'text': prompt or 'Analyze this screenshot.'
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
            raise NotADirectoryError(f"Not a directory: {directory}")
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
