from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import os
import json

from .openrouter_client import get_client
from .report_generator import generate_report


class AnalyzeScreenshotView(APIView):
    """API view for analyzing a single screenshot using OpenRouter API."""
    
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, format=None):
        # Check if screenshot file is provided
        if 'screenshot' not in request.FILES:
            return Response(
                {"error": "No screenshot file provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        screenshot = request.FILES['screenshot']
        prompt = request.data.get('prompt', None)
        
        # Save the screenshot temporarily
        temp_dir = os.path.join(settings.BASE_DIR, 'temp_screenshots')
        os.makedirs(temp_dir, exist_ok=True)
        
        screenshot_path = os.path.join(temp_dir, screenshot.name)
        with open(screenshot_path, 'wb+') as destination:
            for chunk in screenshot.chunks():
                destination.write(chunk)
        
        try:
            # Analyze the screenshot
            client = get_client()
            analysis = client.analyze_screenshot(screenshot_path, prompt=prompt)
            
            # Clean up the temporary file
            os.remove(screenshot_path)
            
            return Response(analysis)
        except Exception as e:
            # Clean up the temporary file
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)
            
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BatchAnalyzeScreenshotsView(APIView):
    """API view for analyzing multiple screenshots in the debug_screenshots directory."""
    
    def post(self, request, format=None):
        language = request.data.get('language', None)
        theme = request.data.get('theme', None)
        page = request.data.get('page', None)
        
        screenshots_dir = os.path.join(settings.BASE_DIR, 'debug_screenshots')
        
        # Validate screenshots directory
        if not os.path.isdir(screenshots_dir):
            return Response(
                {"error": f"Screenshots directory not found: {screenshots_dir}"},
                status=status.HTTP_404_NOT_FOUND
            )
        
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
            return Response(
                {"warning": "No screenshots found matching the specified criteria"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            # Get OpenRouter client
            client = get_client()
            
            # Process each screenshot
            results = {}
            for screenshot in screenshots:
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
            
            return Response(results)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenerateReportView(APIView):
    """API view for generating an HTML report from analysis results."""
    
    def post(self, request, format=None):
        analysis_data = request.data.get('analysis_data', None)
        
        if not analysis_data:
            return Response(
                {"error": "No analysis data provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Save analysis data to a temporary file
            temp_dir = os.path.join(settings.BASE_DIR, 'temp_analysis')
            os.makedirs(temp_dir, exist_ok=True)
            
            analysis_file = os.path.join(temp_dir, 'temp_analysis.json')
            with open(analysis_file, 'w') as f:
                json.dump(analysis_data, f)
            
            # Generate the report
            report_path = generate_report(analysis_file)
            
            # Read the report content
            with open(report_path, 'r') as f:
                report_content = f.read()
            
            # Clean up temporary files
            os.remove(analysis_file)
            os.remove(report_path)
            
            # Return the report as HTML
            return HttpResponse(
                report_content,
                content_type='text/html'
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
