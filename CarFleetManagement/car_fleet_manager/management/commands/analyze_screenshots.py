"""Management command to analyze debug screenshots using OpenRouter API.

This command uses the OpenRouter API to analyze screenshots captured by the
debug_screenshots command, identifying UI issues across different languages and themes.
"""

import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from api.openrouter_client import get_client

class Command(BaseCommand):
    help = 'Analyze debug screenshots using OpenRouter API to identify UI issues'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--screenshots-dir', 
            default=os.path.join(settings.BASE_DIR, 'debug_screenshots'),
            help='Directory containing screenshots to analyze'
        )
        parser.add_argument(
            '--language',
            choices=[lang_code for lang_code, _ in settings.LANGUAGES],
            help='Filter screenshots by language'
        )
        parser.add_argument(
            '--theme',
            choices=['light', 'dark'],
            help='Filter screenshots by theme'
        )
        parser.add_argument(
            '--output',
            default='screenshot_analysis.json',
            help='Output file for analysis results'
        )
        parser.add_argument(
            '--page',
            help='Filter screenshots by page name'
        )
        
    def handle(self, *args, **options):
        screenshots_dir = options['screenshots_dir']
        language = options['language']
        theme = options['theme']
        output_file = options['output']
        page = options['page']
        
        # Validate screenshots directory
        if not os.path.isdir(screenshots_dir):
            self.stdout.write(
                self.style.ERROR(f"Screenshots directory not found: {screenshots_dir}")
            )
            return
        
        # Get all PNG files in the directory
        screenshots = [f for f in os.listdir(screenshots_dir) if f.endswith('.png')]
        
        # Apply filters if specified
        if language:
            screenshots = [s for s in screenshots if f"_{language}_" in s]
        if theme:
            screenshots = [s for s in screenshots if f"_{theme}_" in s]
        if page:
            screenshots = [s for s in screenshots if s.startswith(f"{page}_")]
        
        if not screenshots:
            self.stdout.write(
                self.style.WARNING("No screenshots found matching the specified criteria")
            )
            return
        
        self.stdout.write(f"Found {len(screenshots)} screenshots to analyze")
        
        try:
            # Get OpenRouter client
            client = get_client()
            
            # Process each screenshot
            results = {}
            for i, screenshot in enumerate(screenshots, 1):
                self.stdout.write(f"Analyzing screenshot {i}/{len(screenshots)}: {screenshot}")
                screenshot_path = os.path.join(screenshots_dir, screenshot)
                
                # Extract metadata from filename (format: page_lang_theme_timestamp.png)
                parts = screenshot.replace('.png', '').split('_')
                if len(parts) >= 3:
                    page_name = parts[0]
                    lang = parts[1]
                    theme_name = parts[2]
                    
                    # Create a custom prompt based on metadata
                    prompt = f"""Analyze this UI screenshot of the {page_name} page in {lang} language with {theme_name} theme.
                    Identify any issues with:
                    1. Text rendering and translations
                    2. Layout and alignment
                    3. Theme consistency (colors, contrast)
                    4. Responsive design issues
                    5. UI element spacing and positioning
                    
                    Provide a concise summary of findings and recommendations for improvement."""
                else:
                    prompt = None  # Use default prompt
                
                # Analyze the screenshot
                analysis = client.analyze_screenshot(screenshot_path, prompt=prompt)
                results[screenshot] = analysis
                
                # Display a preview of the analysis
                if 'choices' in analysis and analysis['choices']:
                    content = analysis['choices'][0]['message']['content']
                    preview = content[:150] + '...' if len(content) > 150 else content
                    self.stdout.write(self.style.SUCCESS(f"Analysis: {preview}"))
                elif 'error' in analysis:
                    self.stdout.write(self.style.ERROR(f"Error: {analysis['error']}"))
            
            # Save results to file
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            
            self.stdout.write(
                self.style.SUCCESS(f"Analysis complete. Results saved to {output_file}")
            )
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during analysis: {str(e)}"))