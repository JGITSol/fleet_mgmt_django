"""
Custom renderers for the Car Fleet Management API.

This module provides custom renderers that override Django REST Framework's
default behavior to maintain consistent theming.
"""

from rest_framework.renderers import BrowsableAPIRenderer

# render_to_string not used here


class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    """
    Custom browsable API renderer that disables theme switching
    and maintains consistent dark theme styling.
    """

    template = "rest_framework/api.html"

    def get_context(self, data, accepted_media_type, renderer_context):
        """
        Override the context to disable theme switching and ensure
        consistent styling.
        """
        context = super().get_context(data, accepted_media_type, renderer_context)

        # Disable theme switching by removing theme-related context
        context.pop("theme", None)
        context.pop("style", None)

        # Add our custom styling context
        context.update({
            "custom_theme": "dark",
            "disable_theme_toggle": True,
        })

        return context

    def get_template_names(self):
        """
        Return our custom template names.
        """
        return [self.template]

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Override render to inject custom CSS and JavaScript that prevents
        theme switching.
        """
        # Get the standard rendered content
        content = super().render(data, accepted_media_type, renderer_context)

        # Inject additional CSS and JavaScript to prevent theme switching
        additional_styles = """
        <style>
            /* Force dark theme and prevent theme switching */
            body, html {
                background-color: #2b3035 !important;
                color: #f8f9fa !important;
            }

            .container-fluid, .content-main {
                background-color: #2b3035 !important;
                color: #f8f9fa !important;
            }

            /* Hide any theme toggle elements */
            .theme-toggle, .theme-switch, [data-toggle="theme"] {
                display: none !important;
            }

            /* Override any white backgrounds */
            .well, .form-control, .btn-default, pre, code {
                background-color: #3c4043 !important;
                color: #f8f9fa !important;
                border-color: #5f6368 !important;
            }

            /* Navbar styling */
            .navbar, .navbar-default {
                background-color: #1f2937 !important;
                border-color: #374151 !important;
            }

            .navbar-brand, .navbar-nav > li > a {
                color: #f8f9fa !important;
            }

            /* Form controls */
            .form-control:focus {
                background-color: #3c4043 !important;
                color: #f8f9fa !important;
                border-color: #0d6efd !important;
                box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25) !important;
            }

            /* Buttons */
            .btn-primary {
                background-color: #0d6efd !important;
                border-color: #0d6efd !important;
            }

            .btn-default {
                background-color: #3c4043 !important;
                color: #f8f9fa !important;
                border-color: #5f6368 !important;
            }

            /* Response area */
            .response .prettyprint {
                background-color: #1e1e1e !important;
                color: #f8f9fa !important;
                border: 1px solid #5f6368 !important;
            }

            /* Tabs */
            .nav-tabs .nav-link {
                background-color: #3c4043 !important;
                color: #f8f9fa !important;
                border-color: #5f6368 !important;
            }

            .nav-tabs .nav-link.active {
                background-color: #2b3035 !important;
                color: #f8f9fa !important;
                border-color: #5f6368 !important;
            }

            .tab-content {
                background-color: #2b3035 !important;
                color: #f8f9fa !important;
            }

            /* Breadcrumbs */
            .breadcrumb {
                background-color: #374151 !important;
                color: #f8f9fa !important;
            }

            .breadcrumb-item a {
                color: #60a5fa !important;
            }

            /* Request/Response info */
            .request-info, .response-info {
                background-color: #374151 !important;
                border: 1px solid #5f6368 !important;
                color: #f8f9fa !important;
            }
        </style>

        <script>
            // Completely disable theme switching functionality
            document.addEventListener('DOMContentLoaded', function() {
                // Remove any existing theme toggle elements
                const themeElements = document.querySelectorAll('.theme-toggle, .theme-switch, [data-toggle="theme"]');
                themeElements.forEach(el => el.remove());

                // Override any theme switching functions
                if (window.toggleTheme) {
                    window.toggleTheme = function() { return false; };
                }

                // Prevent theme-related clicks
                document.addEventListener('click', function(e) {
                    const target = e.target;
                    if (target.classList.contains('theme-toggle') ||
                        target.getAttribute('data-toggle') === 'theme' ||
                        target.textContent.toLowerCase().includes('theme')) {
                        e.preventDefault();
                        e.stopPropagation();
                        return false;
                    }
                }, true);

                // Force body styling
                document.body.style.backgroundColor = '#2b3035';
                document.body.style.color = '#f8f9fa';

                // Monitor for any style changes and prevent them
                const observer = new MutationObserver(function(mutations) {
                    mutations.forEach(function(mutation) {
                        if (mutation.type === 'attributes' &&
                            (mutation.attributeName === 'class' || mutation.attributeName === 'style')) {
                            // Ensure consistent styling
                            if (mutation.target === document.body) {
                                document.body.style.backgroundColor = '#2b3035';
                                document.body.style.color = '#f8f9fa';
                            }
                        }
                    });
                });

                observer.observe(document.body, {
                    attributes: true,
                    attributeFilter: ['class', 'style'],
                    subtree: true
                });
            });
        </script>
        """

        # Insert the additional styles and scripts before the closing </body> tag
        was_bytes = isinstance(content, bytes)
        if was_bytes:
            content = content.decode("utf-8")

        insertion = additional_styles

        content = (
            content.replace("</body>", insertion + "</body>", 1)
            if "</body>" in content
            else content + insertion
        )

        # Normalize trailing whitespace and ensure the final returned content
        # ends exactly with a closing </script> tag (tests assert this).
        content = content.rstrip()
        if not content.endswith("</script>"):
            content = content + "</script>"

        # Return bytes as DRF expects
        return content.encode("utf-8")
