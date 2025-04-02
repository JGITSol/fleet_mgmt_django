# OpenRouter API Integration for Car Fleet Manager

This module provides integration with the OpenRouter API for analyzing UI screenshots and generating reports. It helps identify UI issues across different languages and themes, making it easier to maintain a consistent user experience.

## Features

- Analyze individual screenshots using OpenRouter's AI capabilities
- Batch analyze multiple screenshots from the debug_screenshots directory
- Generate HTML reports from analysis results
- Filter screenshots by language, theme, or page name
- Command-line interface for easy use
- REST API endpoints for integration with other systems

## Prerequisites

- OpenRouter API key (stored in `.env` file)
- Python 3.8+
- Django 5.1+
- Requests library

## Configuration

The OpenRouter API key is read from the `.env` file in the project root. Make sure this file contains your API key:

```
OPENROUTER_API_KEY=your-api-key-here
```

**Note:** The `.env` file is included in `.gitignore` to prevent exposing your API key in version control.

## Command-Line Usage

### Analyze a Single Screenshot

```bash
python manage.py openrouter_analyze analyze path/to/screenshot.png --output analysis.json
```

### Batch Analyze Multiple Screenshots

```bash
python manage.py openrouter_analyze batch --dir debug_screenshots --language en --theme dark --output batch_analysis.json
```

### Generate a Report from Analysis Results

```bash
python manage.py openrouter_analyze report batch_analysis.json --output ui_report.html
```

## API Endpoints

### Analyze a Single Screenshot

```
POST /api/screenshots/analyze/
```

Parameters:
- `screenshot`: The image file to analyze
- `prompt` (optional): Custom prompt for analysis

### Batch Analyze Screenshots

```
POST /api/screenshots/batch-analyze/
```

Parameters:
- `language` (optional): Filter screenshots by language
- `theme` (optional): Filter screenshots by theme (light/dark)
- `page` (optional): Filter screenshots by page name

### Generate a Report

```
POST /api/screenshots/generate-report/
```

Parameters:
- `analysis_data`: JSON object containing analysis results

## Example Workflow

1. Capture screenshots using the debug_screenshots command:
   ```bash
   python manage.py debug_screenshots --start-server
   ```

2. Analyze the screenshots using OpenRouter API:
   ```bash
   python manage.py openrouter_analyze batch --output analysis.json
   ```

3. Generate an HTML report from the analysis:
   ```bash
   python manage.py openrouter_analyze report analysis.json
   ```

4. Open the generated HTML report to review the findings

## Implementation Details

- `openrouter_client.py`: Client for interacting with the OpenRouter API
- `report_generator.py`: Generates HTML reports from analysis results
- `views.py`: API endpoints for screenshot analysis
- `management/commands/openrouter_analyze.py`: Command-line interface

## Security Considerations

- The OpenRouter API key is stored in the `.env` file, which is excluded from version control
- Temporary files are cleaned up after use
- Input validation is performed on all user inputs