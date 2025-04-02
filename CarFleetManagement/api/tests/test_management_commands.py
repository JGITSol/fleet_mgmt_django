import os
import json
from unittest import mock
from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from django.conf import settings


class OpenRouterAnalyzeCommandTestCase(TestCase):
    """Test cases for the openrouter_analyze management command."""
    
    def setUp(self):
        """Set up test environment."""
        # Create test directories
        self.test_screenshots_dir = os.path.join(settings.BASE_DIR, 'test_screenshots')
        os.makedirs(self.test_screenshots_dir, exist_ok=True)
        
        # Create a test screenshot file
        self.test_screenshot = os.path.join(self.test_screenshots_dir, 'home_en_dark_20250331-201208.png')
        with open(self.test_screenshot, 'w') as f:
            f.write('test image content')
        
        # Create additional test screenshots for batch testing
        self.test_screenshots = [
            'home_en_light_20250331-201203.png',
            'about_fr_dark_20250331-201239.png',
            'features_es_light_20250331-201220.png'
        ]
        
        for screenshot in self.test_screenshots:
            with open(os.path.join(self.test_screenshots_dir, screenshot), 'w') as f:
                f.write('test image content')
        
        # Create a test analysis file
        self.test_analysis = {
            'home_en_dark_20250331-201208.png': {
                'choices': [
                    {
                        'message': {
                            'content': 'Analysis for home page in English with dark theme'
                        }
                    }
                ]
            },
            'home_en_light_20250331-201203.png': {
                'choices': [
                    {
                        'message': {
                            'content': 'Analysis for home page in English with light theme'
                        }
                    }
                ]
            }
        }
        
        self.analysis_file = os.path.join(self.test_screenshots_dir, 'test_analysis.json')
        with open(self.analysis_file, 'w') as f:
            json.dump(self.test_analysis, f)
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove test screenshot files
        if os.path.exists(self.test_screenshot):
            os.remove(self.test_screenshot)
        
        for screenshot in self.test_screenshots:
            file_path = os.path.join(self.test_screenshots_dir, screenshot)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Remove test analysis file
        if os.path.exists(self.analysis_file):
            os.remove(self.analysis_file)
        
        # Remove test output files
        test_output = os.path.join(self.test_screenshots_dir, 'test_output.json')
        if os.path.exists(test_output):
            os.remove(test_output)
        
        test_report = os.path.join(self.test_screenshots_dir, 'test_report.html')
        if os.path.exists(test_report):
            os.remove(test_report)
        
        # Remove test directory
        if os.path.exists(self.test_screenshots_dir):
            os.rmdir(self.test_screenshots_dir)
    
    def test_command_without_subcommand(self):
        """Test command without subcommand."""
        out = StringIO()
        call_command('openrouter_analyze', stdout=out)
        self.assertIn("No command specified", out.getvalue())
    
    @mock.patch('car_fleet_manager.management.commands.openrouter_analyze.get_client')
    def test_analyze_command(self, mock_get_client):
        """Test 'analyze' subcommand."""
        # Mock the OpenRouter client
        mock_client = mock.Mock()
        mock_client.analyze_screenshot.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Analysis result'
                    }
                }
            ]
        }
        mock_get_client.return_value = mock_client
        
        # Call the command
        out = StringIO()
        call_command(
            'openrouter_analyze',
            'analyze',
            self.test_screenshot,
            stdout=out
        )
        
        # Verify the output
        output = out.getvalue()
        self.assertIn(f"Analyzing screenshot: {self.test_screenshot}", output)
        self.assertIn("Analysis: Analysis result", output)
        
        # Verify the client was called correctly
        mock_client.analyze_screenshot.assert_called_once_with(self.test_screenshot, prompt=None)
    
    @mock.patch('car_fleet_manager.management.commands.openrouter_analyze.get_client')
    def test_analyze_command_with_output(self, mock_get_client):
        """Test 'analyze' subcommand with output file."""
        # Mock the OpenRouter client
        mock_client = mock.Mock()
        mock_client.analyze_screenshot.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Analysis result'
                    }
                }
            ]
        }
        mock_get_client.return_value = mock_client
        
        # Call the command
        test_output = os.path.join(self.test_screenshots_dir, 'test_output.json')
        out = StringIO()
        call_command(
            'openrouter_analyze',
            'analyze',
            self.test_screenshot,
            '--output', test_output,
            stdout=out
        )
        
        # Verify the output
        output = out.getvalue()
        self.assertIn(f"Analysis saved to {test_output}", output)
        
        # Verify the output file was created
        self.assertTrue(os.path.exists(test_output))
        
        # Verify the content of the output file
        with open(test_output, 'r') as f:
            content = json.load(f)
            self.assertIn('choices', content)
    
    @mock.patch('car_fleet_manager.management.commands.openrouter_analyze.get_client')
    def test_analyze_command_with_prompt(self, mock_get_client):
        """Test 'analyze' subcommand with custom prompt."""
        # Mock the OpenRouter client
        mock_client = mock.Mock()
        mock_client.analyze_screenshot.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Analysis result'
                    }
                }
            ]
        }
        mock_get_client.return_value = mock_client
        
        # Call the command
        out = StringIO()
        call_command(
            'openrouter_analyze',
            'analyze',
            self.test_screenshot,
            '--prompt', 'Custom prompt',
            stdout=out
        )
        
        # Verify the client was called with the custom prompt
        mock_client.analyze_screenshot.assert_called_once_with(self.test_screenshot, prompt='Custom prompt')
    
    @mock.patch('car_fleet_manager.management.commands.openrouter_analyze.get_client')
    def test_batch_command(self, mock_get_client):
        """Test 'batch' subcommand."""
        # Mock the OpenRouter client
        mock_client = mock.Mock()
        mock_client.analyze_screenshot.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Analysis result'
                    }
                }
            ]
        }
        mock_get_client.return_value = mock_client
        
        # Call the command
        test_output = os.path.join(self.test_screenshots_dir, 'test_output.json')
        out = StringIO()
        call_command(
            'openrouter_analyze',
            'batch',
            '--dir', self.test_screenshots_dir,
            '--output', test_output,
            stdout=out
        )
        
        # Verify the output
        output = out.getvalue()
        self.assertIn(f"Found {len(self.test_screenshots) + 1} screenshots to analyze", output)
        self.assertIn(f"Analysis complete. Results saved to {test_output}", output)
        
        # Verify the output file was created
        self.assertTrue(os.path.exists(test_output))
        
        # Verify the content of the output file
        with open(test_output, 'r') as f:
            content = json.load(f)
            self.assertEqual(len(content), len(self.test_screenshots) + 1)
    
    @mock.patch('car_fleet_manager.management.commands.openrouter_analyze.get_client')
    def test_batch_command_with_filters(self, mock_get_client):
        """Test 'batch' subcommand with filters."""
        # Mock the OpenRouter client
        mock_client = mock.Mock()
        mock_client.analyze_screenshot.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Analysis result'
                    }
                }
            ]
        }
        mock_get_client.return_value = mock_client
        
        # Call the command with language filter
        test_output = os.path.join(self.test_screenshots_dir, 'test_output.json')
        out = StringIO()
        call_command(
            'openrouter_analyze',
            'batch',
            '--dir', self.test_screenshots_dir,
            '--language', 'en',
            '--output', test_output,
            stdout=out
        )
        
        # Verify the output
        output = out.getvalue()
        self.assertIn("Found 2 screenshots to analyze", output)  # Only the English screenshots
        
        # Verify the content of the output file
        with open(test_output, 'r') as f:
            content = json.load(f)
            self.assertEqual(len(content), 2)
            self.assertIn('home_en_dark_20250331-201208.png', content)
            self.assertIn('home_en_light_20250331-201203.png', content)
    
    @mock.patch('car_fleet_manager.management.commands.openrouter_analyze.generate_report')
    def test_report_command(self, mock_generate_report):
        """Test 'report' subcommand."""
        # Mock the generate_report function
        test_report = os.path.join(self.test_screenshots_dir, 'test_report.html')
        mock_generate_report.return_value = test_report
        
        # Call the command
        out = StringIO()
        call_command(
            'openrouter_analyze',
            'report',
            self.analysis_file,
            stdout=out
        )
        
        # Verify the output
        output = out.getvalue()
        self.assertIn(f"Generating report from {self.analysis_file}", output)
        self.assertIn(f"Report generated: {test_report}", output)
        
        # Verify generate_report was called correctly
        mock_generate_report.assert_called_once_with(self.analysis_file, None)
    
    @mock.patch('car_fleet_manager.management.commands.openrouter_analyze.generate_report')
    def test_report_command_with_output(self, mock_generate_report):
        """Test 'report' subcommand with output file."""
        # Mock the generate_report function
        test_report = os.path.join(self.test_screenshots_dir, 'test_report.html')
        mock_generate_report.return_value = test_report
        
        # Call the command
        out = StringIO()
        call_command(
            'openrouter_analyze',
            'report',
            self.analysis_file,
            '--output', test_report,
            stdout=out
        )
        
        # Verify generate_report was called with the output file
        mock_generate_report.assert_called_once_with(self.analysis_file, test_report)