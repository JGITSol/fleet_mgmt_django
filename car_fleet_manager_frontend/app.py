import reflex as rx
from pages import dashboard, drivers, login, maintenance, vehicles

app = rx.App()

# Add pages
app.add_page(dashboard.page, route="/")
app.add_page(vehicles.page, route="/vehicles")
app.add_page(drivers.page, route="/drivers")
app.add_page(maintenance.page, route="/maintenance")
app.add_page(login.page, route="/login")

# Optionally, set up route guard if supported in your Reflex version (pseudo-code):
# app.route_guard = ...
# If your Reflex version supports route guards, you can add it here. Otherwise, handle authentication in the page components.
