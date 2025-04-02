"""Report generator for OpenRouter API screenshot analysis.

This module provides functionality to generate HTML reports from
the screenshot analysis results produced by the OpenRouter API.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

class ScreenshotAnalysisReport:
    """Generator for screenshot analysis reports."""
    
    def __init__(self, analysis_file):
        """Initialize the report generator.
        
        Args:
            analysis_file (str): Path to the JSON file containing analysis results
        """
        self.analysis_file = analysis_file
        self.analysis_data = self._load_analysis_data()
        
    def _load_analysis_data(self):
        """Load analysis data from the JSON file.
        
        Returns:
            dict: The analysis data
        """
        if not os.path.exists(self.analysis_file):
            raise FileNotFoundError(f"Analysis file not found: {self.analysis_file}")
        
        with open(self.analysis_file, 'r') as f:
            return json.load(f)
    
    def generate_html_report(self, output_file=None):
        """Generate an HTML report from the analysis data.
        
        Args:
            output_file (str, optional): Path to save the HTML report.
                If not provided, a default path will be used.
                
        Returns:
            str: Path to the generated HTML report
        """
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            output_file = os.path.join(settings.BASE_DIR, f'screenshot_analysis_report_{timestamp}.html')
        
        # Organize data by page, language, and theme
        organized_data = {}
        for screenshot, analysis in self.analysis_data.items():
            # Extract metadata from filename (format: page_lang_theme_timestamp.png)
            parts = screenshot.replace('.png', '').split('_')
            if len(parts) >= 3:
                page_name = parts[0]
                lang = parts[1]
                theme = parts[2]
                
                # Initialize nested dictionaries if they don't exist
                if page_name not in organized_data:
                    organized_data[page_name] = {}
                if lang not in organized_data[page_name]:
                    organized_data[page_name][lang] = {}
                
                # Extract the analysis content
                content = ""
                if 'choices' in analysis and analysis['choices']:
                    content = analysis['choices'][0]['message']['content']
                elif 'error' in analysis:
                    content = f"Error: {analysis['error']}"
                
                # Store the analysis
                organized_data[page_name][lang][theme] = {
                    'screenshot': screenshot,
                    'analysis': content
                }
        
        # Prepare context for the template
        context = {
            'title': 'Screenshot Analysis Report',
            'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'data': organized_data,
            'screenshot_dir': os.path.join(settings.BASE_DIR, 'debug_screenshots')
        }
        
        # Generate HTML content
        # In a real implementation, you would use Django's template system
        # Here we're creating a simple HTML structure
        html_content = self._generate_html_template(context)
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        return output_file
    
    def _generate_html_template(self, context):
        """Generate HTML content for the report.
        
        Args:
            context (dict): Context data for the template
            
        Returns:
            str: HTML content
        """
        # In a real implementation, you would use Django's template system
        # For simplicity, we're generating HTML directly here
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{context['title']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2, h3, h4 {{ color: #333; }}
                .page-section {{ margin-bottom: 30px; border: 1px solid #ddd; padding: 15px; border-radius: 5px; }}
                .language-section {{ margin-bottom: 20px; }}
                .theme-comparison {{ display: flex; flex-wrap: wrap; gap: 20px; }}
                .theme-card {{ flex: 1; min-width: 300px; border: 1px solid #eee; padding: 10px; border-radius: 5px; }}
                .screenshot {{ max-width: 100%; height: auto; border: 1px solid #ccc; margin-bottom: 10px; }}
                .analysis {{ white-space: pre-line; background: #f9f9f9; padding: 10px; border-radius: 3px; }}
                .meta {{ color: #666; font-size: 0.9em; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <h1>{context['title']}</h1>
            <div class="meta">Generated at: {context['generated_at']}</div>
        """
        
        # Add content for each page
        for page_name, languages in context['data'].items():
            html += f"""
            <div class="page-section">
                <h2>Page: {page_name}</h2>
            """
            
            # Add content for each language
            for lang, themes in languages.items():
                html += f"""
                <div class="language-section">
                    <h3>Language: {lang}</h3>
                    <div class="theme-comparison">
                """
                
                # Add content for each theme
                for theme, data in themes.items():
                    screenshot_path = os.path.join(context['screenshot_dir'], data['screenshot'])
                    html += f"""
                    <div class="theme-card">
                        <h4>Theme: {theme}</h4>
                        <img class="screenshot" src="file:///{screenshot_path}" alt="{data['screenshot']}">
                        <div class="analysis">{data['analysis']}</div>
                    </div>
                    """
                
                html += "</div></div>"
            
            html += "</div>"
        
        html += "</body></html>"
        return html


def generate_report(analysis_file, output_file=None):
    """Generate a report from analysis results.
    
    Args:
        analysis_file (str): Path to the JSON file containing analysis results
        output_file (str, optional): Path to save the HTML report
        
    Returns:
        str: Path to the generated HTML report
    """
    report_generator = ScreenshotAnalysisReport(analysis_file)
    return report_generator.generate_html_report(output_file)