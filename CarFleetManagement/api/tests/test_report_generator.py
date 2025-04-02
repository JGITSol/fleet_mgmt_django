import os
import json
from unittest import mock
from django.test import TestCase
from django.conf import settings
from pathlib import Path

from api.report_generator import ScreenshotAnalysisReport, generate_report


class ScreenshotAnalysisReportTestCase(TestCase):
    """Test cases for the ScreenshotAnalysisReport class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a test directory
        self.test_dir = os.path.join(settings.BASE_DIR, 'test_analysis')
        os.makedirs(self.test_dir, exist_ok=True)
        
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
            },
            'about_fr_dark_20250331-201239.png': {
                'choices': [
                    {
                        'message': {
                            'content': 'Analysis for about page in French with dark theme'
                        }
                    }
                ]
            },
            'features_es_light_20250331-201220.png': {
                'error': 'API error'
            }
        }
        
        self.analysis_file = os.path.join(self.test_dir, 'test_analysis.json')
        with open(self.analysis_file, 'w') as f:
            json.dump(self.test_analysis, f)
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove test analysis file
        if os.path.exists(self.analysis_file):
            os.remove(self.analysis_file)
        
        # Remove test directory
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
    
    def test_init_file_not_found(self):
        """Test initialization with non-existent file."""
        with self.assertRaises(FileNotFoundError):
            ScreenshotAnalysisReport('nonexistent_file.json')
    
    def test_init_with_valid_file(self):
        """Test initialization with valid analysis file."""
        report = ScreenshotAnalysisReport(self.analysis_file)
        self.assertEqual(report.analysis_data, self.test_analysis)
    
    def test_generate_html_report_default_output(self):
        """Test generate_html_report with default output path."""
        report = ScreenshotAnalysisReport(self.analysis_file)
        
        with mock.patch('builtins.open', mock.mock_open()) as mock_file:
            output_path = report.generate_html_report()
            
            # Verify the file was written
            mock_file.assert_called()
            
            # Verify the output path is in the expected format
            self.assertIn('screenshot_analysis_report_', output_path)
            self.assertTrue(output_path.endswith('.html'))
    
    def test_generate_html_report_custom_output(self):
        """Test generate_html_report with custom output path."""
        report = ScreenshotAnalysisReport(self.analysis_file)
        custom_output = os.path.join(self.test_dir, 'custom_report.html')
        
        with mock.patch('builtins.open', mock.mock_open()) as mock_file:
            output_path = report.generate_html_report(custom_output)
            
            # Verify the file was written
            mock_file.assert_called()
            
            # Verify the output path is the custom one
            self.assertEqual(output_path, custom_output)
    
    def test_generate_html_report_content(self):
        """Test the content of the generated HTML report."""
        report = ScreenshotAnalysisReport(self.analysis_file)
        
        # Use a StringIO to capture the written content
        from io import StringIO
        string_io = StringIO()
        
        with mock.patch('builtins.open', mock.mock_open()) as mock_file:
            # Make write() write to our StringIO
            mock_file.return_value.write.side_effect = lambda data: string_io.write(data)
            
            report.generate_html_report()
            
            # Get the written content
            content = string_io.getvalue()
            
            # Verify the content includes expected elements
            self.assertIn('<title>Screenshot Analysis Report</title>', content)
            self.assertIn('<h2>Page: home</h2>', content)
            self.assertIn('<h2>Page: about</h2>', content)
            self.assertIn('<h2>Page: features</h2>', content)
            self.assertIn('<h3>Language: en</h3>', content)
            self.assertIn('<h3>Language: fr</h3>', content)
            self.assertIn('<h3>Language: es</h3>', content)
            self.assertIn('<h4>Theme: dark</h4>', content)
            self.assertIn('<h4>Theme: light</h4>', content)
            self.assertIn('Analysis for home page in English with dark theme', content)
            self.assertIn('Analysis for home page in English with light theme', content)
            self.assertIn('Analysis for about page in French with dark theme', content)
            self.assertIn('Error: API error', content)
    
    def test_generate_report_function(self):
        """Test the generate_report function."""
        with mock.patch('api.report_generator.ScreenshotAnalysisReport') as mock_report:
            # Mock the generate_html_report method
            mock_instance = mock_report.return_value
            mock_instance.generate_html_report.return_value = 'test_output.html'
            
            # Call the function
            output = generate_report(self.analysis_file, 'custom_output.html')
            
            # Verify the ScreenshotAnalysisReport was created with the correct file
            mock_report.assert_called_once_with(self.analysis_file)
            
            # Verify generate_html_report was called with the correct output file
            mock_instance.generate_html_report.assert_called_once_with('custom_output.html')
            
            # Verify the output is correct
            self.assertEqual(output, 'test_output.html')