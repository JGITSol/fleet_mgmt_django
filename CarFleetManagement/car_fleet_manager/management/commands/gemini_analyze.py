"""Management command to analyze screenshots using Google Gemini API.

This command provides a convenient CLI for using the Google Gemini API
to analyze screenshots and generate reports.
"""

import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from api.gemini_client import get_client
from api.report_generator import generate_report

class Command(BaseCommand):
    help = 'Analyze screenshots using Google Gemini API and generate reports'
    
    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='command', help='Commands')
        
        # Analyze a single screenshot
        analyze_parser = subparsers.add_parser('analyze', help='Analyze a single screenshot')
        analyze_parser.add_argument('screenshot_path', help='Path to the screenshot file')
        analyze_parser.add_argument('--prompt', help='Custom prompt for analysis')
        analyze_parser.add_argument('--output', help='Output file for analysis results')
        
        # Batch analyze multiple screenshots
        batch_parser = subparsers.add_parser('batch', help='Analyze multiple screenshots')
        batch_parser.add_argument(
            '--dir', 
            default=os.path.join(settings.BASE_DIR, 'debug_screenshots'),
            help='Directory containing screenshots'
        )
        batch_parser.add_argument('--language', help='Filter screenshots by language')
        batch_parser.add_argument('--theme', choices=['light', 'dark'], help='Filter screenshots by theme')
        batch_parser.add_argument('--page', help='Filter screenshots by page name')
        batch_parser.add_argument(
            '--output', 
            default='gemini_screenshot_analysis.json',
            help='Output file for analysis results'
        )
        
        # Generate a report from analysis results
        report_parser = subparsers.add_parser('report', help='Generate a report from analysis results')
        report_parser.add_argument('analysis_file', help='JSON file containing analysis results')
        report_parser.add_argument('--output', help='Output file for the HTML report')
        
    def handle(self, *args, **options):
        command = options['command']
        
        if not command:
            self.stdout.write(self.style.ERROR("No command specified. Use 'analyze', 'batch', or 'report'."))
            return
        
        try:
            if command == 'analyze':
                self._handle_analyze(options)
            elif command == 'batch':
                self._handle_batch(options)
            elif command == 'report':
                self._handle_report(options)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
    
    def _handle_analyze(self, options):
        """Handle the 'analyze' command."""
        screenshot_path = options['screenshot_path']
        prompt = options['prompt']
        output_file = options['output']
        
        if not os.path.exists(screenshot_path):
            self.stdout.write(self.style.ERROR(f"Screenshot not found: {screenshot_path}"))
            return
        
        self.stdout.write(f"Analyzing screenshot with Gemini: {screenshot_path}")
        
        # Get Gemini client and analyze the screenshot
        client = get_client()
        analysis = client.analyze_screenshot(screenshot_path, prompt=prompt)
        
        # Display a preview of the analysis
        if 'choices' in analysis and analysis['choices']:
            content = analysis['choices'][0]['message']['content']
            preview = content[:150] + '...' if len(content) > 150 else content
            self.stdout.write(self.style.SUCCESS(f"Analysis: {preview}"))
        elif 'error' in analysis:
            self.stdout.write(self.style.ERROR(f"Error: {analysis['error']}"))
        
        # Save results to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(analysis, f, indent=2)
            self.stdout.write(self.style.SUCCESS(f"Analysis saved to {output_file}"))
    
    def _handle_batch(self, options):
        """Handle the 'batch' command."""
        screenshots_dir = options['dir']
        language = options['language']
        theme = options['theme']
        page = options['page']
        output_file = options['output']
        
        if not os.path.isdir(screenshots_dir):
            self.stdout.write(self.style.ERROR(f"Screenshots directory not found: {screenshots_dir}"))
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
            self.stdout.write(self.style.WARNING("No screenshots found matching the specified criteria"))
            return
        
        self.stdout.write(f"Found {len(screenshots)} screenshots to analyze with Gemini")
        
        # Get Gemini client
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
        
        self.stdout.write(self.style.SUCCESS(f"Analysis complete. Results saved to {output_file}"))
    
    def _handle_report(self, options):
        """Handle the 'report' command."""
        analysis_file = options['analysis_file']
        output_file = options['output']
        
        if not os.path.exists(analysis_file):
            self.stdout.write(self.style.ERROR(f"Analysis file not found: {analysis_file}"))
            return
        
        self.stdout.write(f"Generating report from {analysis_file}")
        
        # Generate the report
        report_path = generate_report(analysis_file, output_file)
        
        self.stdout.write(self.style.SUCCESS(f"Report generated: {report_path}"))