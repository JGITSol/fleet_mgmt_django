"""
Tests for API renderers.
"""

from unittest.mock import patch

from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from CarFleetManagement.api.renderers import CustomBrowsableAPIRenderer


class CustomBrowsableAPIRendererTestCase(TestCase):
    """Test cases for CustomBrowsableAPIRenderer."""

    def setUp(self):
        """Set up test data."""
        self.renderer = CustomBrowsableAPIRenderer()
        self.factory = APIRequestFactory()

    def test_get_context_removes_theme_data(self):
        """Test that get_context removes theme-related data."""
        # Create a mock context with theme data
        with patch.object(self.renderer.__class__.__bases__[0], "get_context") as mock_super:
            mock_super.return_value = {"theme": "light", "style": "default", "other_data": "value"}

            request = self.factory.get("/")
            renderer_context = {"request": Request(request)}

            context = self.renderer.get_context(
                data={"test": "data"}, accepted_media_type="text/html", renderer_context=renderer_context
            )

            # Check that theme data is removed
            self.assertNotIn("theme", context)
            self.assertNotIn("style", context)

            # Check that custom theme data is added
            self.assertEqual(context["custom_theme"], "dark")
            self.assertTrue(context["disable_theme_toggle"])

            # Check that other data is preserved
            self.assertEqual(context["other_data"], "value")

    def test_get_template_names(self):
        """Test that get_template_names returns correct template."""
        template_names = self.renderer.get_template_names()
        self.assertEqual(template_names, ["rest_framework/api.html"])

    def test_render_injects_custom_styles(self):
        """Test that render method injects custom styles and scripts."""
        # Mock the parent render method
        mock_content = """
        <html>
        <head><title>Test</title></head>
        <body>
            <div>Test content</div>
        </body>
        </html>
        """

        with patch.object(self.renderer.__class__.__bases__[0], "render") as mock_super:
            mock_super.return_value = mock_content.encode("utf-8")

            result = self.renderer.render(data={"test": "data"}, accepted_media_type="text/html", renderer_context={})

            # Convert result to string for checking
            result_str = result.decode("utf-8") if isinstance(result, bytes) else result

            # Check that custom styles are injected
            self.assertIn("<style>", result_str)
            self.assertIn("background-color: #2b3035 !important", result_str)
            self.assertIn("color: #f8f9fa !important", result_str)

            # Check that custom scripts are injected
            self.assertIn("<script>", result_str)
            self.assertIn("toggleTheme", result_str)
            self.assertIn("theme-toggle", result_str)

    def test_render_handles_string_content(self):
        """Test that render method handles string content correctly."""
        mock_content = """
        <html>
        <head><title>Test</title></head>
        <body>
            <div>Test content</div>
        </body>
        </html>
        """

        with patch.object(self.renderer.__class__.__bases__[0], "render") as mock_super:
            mock_super.return_value = mock_content  # String instead of bytes

            result = self.renderer.render(data={"test": "data"}, accepted_media_type="text/html", renderer_context={})

            # Should return bytes
            self.assertIsInstance(result, bytes)

            # Convert to string for checking
            result_str = result.decode("utf-8")

            # Check that custom styles are injected
            self.assertIn("<style>", result_str)
            self.assertIn("background-color: #2b3035 !important", result_str)

    def test_render_handles_content_without_body_tag(self):
        """Test that render method handles content without body tag."""
        mock_content = "<div>Simple content without body tag</div>"

        with patch.object(self.renderer.__class__.__bases__[0], "render") as mock_super:
            mock_super.return_value = mock_content.encode("utf-8")

            result = self.renderer.render(data={"test": "data"}, accepted_media_type="text/html", renderer_context={})

            # Convert result to string for checking
            result_str = result.decode("utf-8") if isinstance(result, bytes) else result

            # Check that custom styles are appended
            self.assertIn("<style>", result_str)
            self.assertIn("background-color: #2b3035 !important", result_str)
            self.assertTrue(result_str.endswith("</script>"))

    def test_render_preserves_original_content(self):
        """Test that render method preserves original content."""
        original_content = """
        <html>
        <head><title>Original Title</title></head>
        <body>
            <h1>Original Header</h1>
            <p>Original paragraph</p>
        </body>
        </html>
        """

        with patch.object(self.renderer.__class__.__bases__[0], "render") as mock_super:
            mock_super.return_value = original_content.encode("utf-8")

            result = self.renderer.render(data={"test": "data"}, accepted_media_type="text/html", renderer_context={})

            # Convert result to string for checking
            result_str = result.decode("utf-8") if isinstance(result, bytes) else result

            # Check that original content is preserved
            self.assertIn("Original Title", result_str)
            self.assertIn("Original Header", result_str)
            self.assertIn("Original paragraph", result_str)

            # Check that custom styles are also present
            self.assertIn("<style>", result_str)
            self.assertIn("<script>", result_str)

    def test_template_attribute(self):
        """Test that template attribute is set correctly."""
        self.assertEqual(self.renderer.template, "rest_framework/api.html")

    def test_custom_css_classes_included(self):
        """Test that specific CSS classes are included in the injected styles."""
        mock_content = "<html><body>Test</body></html>"

        with patch.object(self.renderer.__class__.__bases__[0], "render") as mock_super:
            mock_super.return_value = mock_content.encode("utf-8")

            result = self.renderer.render(data={"test": "data"}, accepted_media_type="text/html", renderer_context={})

            result_str = result.decode("utf-8")

            # Check for specific CSS classes that should be styled
            expected_classes = [
                ".container-fluid",
                ".content-main",
                ".theme-toggle",
                ".form-control",
                ".btn-default",
                ".navbar",
                ".nav-tabs",
                ".breadcrumb",
                ".request-info",
                ".response-info",
            ]

            for css_class in expected_classes:
                self.assertIn(css_class, result_str)

    def test_javascript_functions_included(self):
        """Test that specific JavaScript functions are included."""
        mock_content = "<html><body>Test</body></html>"

        with patch.object(self.renderer.__class__.__bases__[0], "render") as mock_super:
            mock_super.return_value = mock_content.encode("utf-8")

            result = self.renderer.render(data={"test": "data"}, accepted_media_type="text/html", renderer_context={})

            result_str = result.decode("utf-8")

            # Check for specific JavaScript functionality
            expected_js_features = [
                "DOMContentLoaded",
                "toggleTheme",
                "preventDefault",
                "MutationObserver",
                "addEventListener",
            ]

            for js_feature in expected_js_features:
                self.assertIn(js_feature, result_str)
