import reflex as rx
from components.header import header
from components.footer import footer

def page():
    return rx.box(
        header(),
        rx.container(
            rx.heading("Fleet Dashboard", size="4", mb=4),
            rx.text("Welcome to the Car Fleet Manager dashboard. Use the navigation to manage vehicles, drivers, and maintenance.", mb=8),
            rx.grid(
                # Total Vehicles Stat Card
                rx.box(
                    rx.icon("car", color="blue", box_size=6, mb=2),
                    rx.text("Total Vehicles", font_weight="bold"),
                    rx.text("123", font_size="2xl", color="blue.700"),
                    p=4,
                    border_radius="md",
                    bg="white",
                    box_shadow="md",
                    align="center"
                ),
                # Active Drivers Stat Card
                rx.box(
                    rx.icon("user", color="green", box_size=6, mb=2),
                    rx.text("Active Drivers", font_weight="bold"),
                    rx.text("45", font_size="2xl", color="green.700"),
                    p=4,
                    border_radius="md",
                    bg="white",
                    box_shadow="md",
                    align="center"
                ),
                # Upcoming Maintenance Stat Card
                rx.box(
                    rx.icon("tool", color="orange", box_size=6, mb=2),
                    rx.text("Upcoming Maintenance", font_weight="bold"),
                    rx.text("7", font_size="2xl", color="orange.700"),
                    p=4,
                    border_radius="md",
                    bg="white",
                    box_shadow="md",
                    align="center"
                ),
                columns="3",
                gap=6,
                width="100%",
                mb=8,
            ),
            align="center",
            width=["100%", "80%", "60%"],
            py=8,
        ),
        footer(),
        as_="main",
        min_height="100vh",
        bg="gray.50"
    )
