import json
import os
from io import StringIO
from unittest import mock

from django.conf import settings
from django.core.management import call_command
from dotenv import load_dotenv
from rest_framework.test import APITestCase

# Load environment variables for API key
load_dotenv(dotenv_path=os.path.join(settings.BASE_DIR, '.env'), override=False)

class OpenRouterAnalyzeCommandTestCase(APITestCase):
    def setUp(self):
        # Create test screenshots directory
        self.test_dir = os.path.join(settings.BASE_DIR, 'test_screenshots')
        os.makedirs(self.test_dir, exist_ok=True)
        # Single screenshot
        self.test_screenshot = os.path.join(self.test_dir, 'home_en_dark_20250331-201208.png')
        with open(self.test_screenshot, 'w') as f:
            f.write('image data')
        # Batch screenshots
        self.batch_files = [
            'home_en_light_20250331-201203.png',
            'about_fr_dark_20250331-201239.png'
        ]
        for fname in self.batch_files:
            with open(os.path.join(self.test_dir, fname), 'w') as f:
                f.write('image data')
        # Pre-built analysis file
        self.analysis_file = os.path.join(self.test_dir, 'analysis.json')
        sample = {
            'home_en_dark_20250331-201208.png': {'choices': [{'message': {'content': 'Sample'}}]}
        }
        with open(self.analysis_file, 'w') as f:
            json.dump(sample, f)

    def tearDown(self):
        # Cleanup files and directory
        for f in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, f))
        os.rmdir(self.test_dir)

    @mock.patch('CarFleetManagement.api.management.commands.openrouter_analyze.get_client')
    def test_command_without_subcommand(self, mock_get_client):
        out = StringIO()
        call_command('openrouter_analyze', stdout=out)
        self.assertIn('No command specified', out.getvalue())
        mock_get_client.assert_not_called()

    @mock.patch('CarFleetManagement.api.management.commands.openrouter_analyze.get_client')
    def test_analyze_command(self, mock_get_client):
        client = mock_get_client.return_value
        client.analyze_screenshot.return_value = {'choices': [{'message': {'content': 'OK'}}]}
        out = StringIO()
        call_command('openrouter_analyze', 'analyze', self.test_screenshot, stdout=out)
        out_str = out.getvalue()
        self.assertIn(f'Analyzing screenshot: {self.test_screenshot}', out_str)
        self.assertIn('Analysis: OK', out_str)
        client.analyze_screenshot.assert_called_once_with(self.test_screenshot, prompt=None)

    @mock.patch('CarFleetManagement.api.management.commands.openrouter_analyze.get_client')
    def test_analyze_with_output(self, mock_get_client):
        client = mock_get_client.return_value
        client.analyze_screenshot.return_value = {'choices': [{'message': {'content': 'OK'}}]}
        out_path = os.path.join(self.test_dir, 'out.json')
        out = StringIO()
        call_command('openrouter_analyze', 'analyze', self.test_screenshot, '--output', out_path, stdout=out)
        self.assertTrue(os.path.exists(out_path))
        with open(out_path) as f:
            data = json.load(f)
        self.assertIn('choices', data)

    @mock.patch('CarFleetManagement.api.management.commands.openrouter_analyze.get_client')
    def test_analyze_with_prompt(self, mock_get_client):
        client = mock_get_client.return_value
        client.analyze_screenshot.return_value = {'choices': [{'message': {'content': 'Custom'}}]}
        out = StringIO()
        call_command('openrouter_analyze', 'analyze', self.test_screenshot, '--prompt', 'P', stdout=out)
        self.assertIn('Analysis: Custom', out.getvalue())
        client.analyze_screenshot.assert_called_once_with(self.test_screenshot, prompt='P')

    @mock.patch('CarFleetManagement.api.management.commands.openrouter_analyze.get_client')
    def test_analyze_error(self, mock_get_client):
        client = mock_get_client.return_value
        client.analyze_screenshot.return_value = {'error': 'Fail'}
        out = StringIO()
        call_command('openrouter_analyze', 'analyze', self.test_screenshot, stdout=out)
        self.assertIn('Analysis: Error: Fail', out.getvalue())

    @mock.patch('CarFleetManagement.api.management.commands.openrouter_analyze.get_client')
    def test_batch(self, mock_get_client):
        client = mock_get_client.return_value
        client.analyze_screenshot.return_value = {'choices': [{'message': {'content': 'B'}}]}
        # create input file
        inp = os.path.join(self.test_dir, 'in.txt')
        with open(inp, 'w') as f:
            f.write(self.test_screenshot + '\n')
            for fn in self.batch_files:
                f.write(os.path.join(self.test_dir, fn) + '\n')
        out_path = os.path.join(self.test_dir, 'batch.json')
        out = StringIO()
        call_command('openrouter_analyze', 'batch', '--input', inp, '--output', out_path, stdout=out)
        self.assertTrue(os.path.exists(out_path))
        with open(out_path) as f:
            d = json.load(f)
        self.assertEqual(len(d), 1 + len(self.batch_files))

    @mock.patch('CarFleetManagement.api.management.commands.openrouter_analyze.get_client')
    def test_batch_filters(self, mock_get_client):
        # filters not implemented
        client = mock_get_client.return_value
        client.analyze_screenshot.return_value = {'choices': [{'message': {'content': 'F'}}]}
        inp = os.path.join(self.test_dir, 'in2.txt')
        with open(inp, 'w') as f:
            f.write(self.test_screenshot + '\n')
        out_path = os.path.join(self.test_dir, 'batchf.json')
        out = StringIO()
        call_command('openrouter_analyze', 'batch', '--input', inp, '--filters', 'en', '--output', out_path, stdout=out)
        with open(out_path) as f:
            d = json.load(f)
        self.assertEqual(len(d), 1)

    @mock.patch('CarFleetManagement.api.management.commands.openrouter_analyze.generate_report')
    def test_report(self, mock_gen):
        mock_gen.return_value = 'r.html'
        out = StringIO()
        call_command('openrouter_analyze', 'report', self.analysis_file, '--output', 'r.html', stdout=out)
        self.assertIn('Report generated at: r.html', out.getvalue())
        mock_gen.assert_called_once_with(self.analysis_file, 'r.html')
