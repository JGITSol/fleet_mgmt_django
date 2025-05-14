class GeminiClient:
    def __init__(self, *args, **kwargs):
        pass

    def some_method(self):
        return "stub"

genai = object()  # Dummy attribute for tests
def get_client(*args, **kwargs):
    return GeminiClient(*args, **kwargs)

class Image:
    pass
