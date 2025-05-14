import os
import json
from django.core.management.base import BaseCommand, CommandError
from api.openrouter_client import OpenRouterClient
from api.report_generator import generate_report
from django.conf import settings

class Command(BaseCommand):
    help = 'Analyze screenshots using OpenRouter API and generate reports.'

    def add_arguments(self, parser):
        parser.add_argument('subcommand', nargs='?', type=str, help='Subcommand: analyze, batch, report')
        parser.add_argument('screenshot', nargs='?', type=str, help='Path to screenshot for analysis')
        parser.add_argument('--output', type=str, help='Output file for analysis or report')
        parser.add_argument('--prompt', type=str, help='Custom prompt for analysis')
        parser.add_argument('--input', type=str, help='Input file for batch analysis')
        parser.add_argument('--filters', type=str, nargs='*', help='Filters for batch analysis (not implemented)')
        parser.add_argument('--dir', type=str, help='Directory for batch analysis')
        parser.add_argument('--language', type=str, help='Language filter for batch analysis')
        parser.add_argument('--theme', type=str, help='Theme filter for batch analysis')

    def handle(self, *args, **options):
        subcommand = options.get('subcommand')
        screenshot = options.get('screenshot')
        output = options.get('output')
        prompt = options.get('prompt')
        input_file = options.get('input')
        filters = options.get('filters')
        batch_dir = options.get('dir')
        language = options.get('language')
        theme = options.get('theme')

        if not subcommand:
            self.stdout.write(self.style.ERROR('No command specified. Use: analyze, batch, or report.'))
            return

        if subcommand == 'analyze':
            self.analyze_screenshot(screenshot, output, prompt)
        elif subcommand == 'batch':
            self.batch_analyze(batch_dir, output, language, theme, prompt)
        elif subcommand == 'report':
            analysis_file = screenshot or input_file
            self.stdout.write(f"Generating report from {analysis_file}")
            self.generate_report(analysis_file, output)
        else:
            self.stdout.write(self.style.ERROR(f'Unknown subcommand: {subcommand}'))

    def analyze_screenshot(self, screenshot_path, output_file=None, prompt=None):
        if not screenshot_path or not os.path.exists(screenshot_path):
            self.stdout.write(self.style.ERROR(f'Screenshot not found: {screenshot_path}'))
            return
        self.stdout.write(f'Analyzing screenshot: {screenshot_path}')
        client = get_client()
        result = client.analyze_screenshot(screenshot_path, prompt=prompt)
        content = ''
        if 'choices' in result and result['choices']:
            content = result['choices'][0]['message']['content']
        elif 'error' in result:
            content = f"Error: {result['error']}"
        self.stdout.write(f'Analysis: {content}')
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(result, f)
            self.stdout.write(self.style.SUCCESS(f'Analysis saved to {output_file}'))

    def batch_analyze(self, batch_dir, output_file=None, language=None, theme=None, prompt=None):
        from api.openrouter_client import OpenRouterClient
        if not batch_dir or not os.path.isdir(batch_dir):
            self.stdout.write(self.style.ERROR(f'Directory not found: {batch_dir}'))
            raise CommandError(f'Directory not found: {batch_dir}')
        client = get_client()
        results = {}
        for filename in os.listdir(batch_dir):
            if filename.endswith('.png'):
                parts = filename.replace('.png', '').split('_')
                if len(parts) >= 3:
                    lang = parts[1]
                    thm = parts[2]
                    if language and lang != language:
                        continue
                    if theme and thm != theme:
                        continue
                screenshot_path = os.path.join(batch_dir, filename)
                try:
                    result = client.analyze_screenshot(screenshot_path, prompt=prompt)
                    results[filename] = result
                    self.stdout.write(self.style.SUCCESS(f'Analyzed: {screenshot_path}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Failed to analyze {screenshot_path}: {e}'))
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(results, f)
            self.stdout.write(self.style.SUCCESS(f'Batch analysis saved to {output_file}'))

    def generate_report(self, analysis_file, output_file=None):
        if not analysis_file or not os.path.exists(analysis_file):
            self.stdout.write(self.style.ERROR(f'Analysis file not found: {analysis_file}'))
            return
        report_path = generate_report(analysis_file, output_file)
        self.stdout.write(self.style.SUCCESS(f'Report generated at: {report_path}'))

def get_client():
    api_key = getattr(settings, 'OPENROUTER_API_KEY', None)
    return OpenRouterClient(api_key=api_key)
