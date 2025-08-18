# Car Fleet Manager Frontend (Reflex)

This is a Reflex (reflex.dev) frontend for the Car Fleet Manager app. It is designed to be fully accessible, responsive, and uses modern CSS best practices.

## Features
- Responsive, mobile-first layout
- Accessible components (ARIA, keyboard navigation, color contrast)
- Modern CSS (Tailwind/Chakra via Reflex)
- Pages for Vehicles, Drivers, Maintenance, Dashboard

## Getting Started
1. Install dependencies:
   ```bash
   pip install reflex
   ```
2. Run the app:
   ```bash
   reflex run
   ```

## Project Structure
- `app.py` - Main Reflex app entry point
- `pages/` - All main pages (dashboard, vehicles, drivers, maintenance)
- `components/` - Reusable UI components

## Requirements
- Python 3.8+
- reflex >=0.4.0

---

For backend integration, update API endpoints in the data fetching utilities.
