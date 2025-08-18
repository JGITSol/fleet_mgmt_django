import reflex as rx

def header():
    return rx.box(
        rx.container(
            rx.hstack(
                rx.heading("Car Fleet Manager", size="4", color="blue.700", as_="a", href="/", mr=8),
                rx.spacer(),
                rx.link("Dashboard", href="/", px=4, py=2, rounded="md", _hover={"bg": "blue.100"}),
                rx.link("Vehicles", href="/vehicles", px=4, py=2, rounded="md", _hover={"bg": "blue.100"}),
                rx.link("Drivers", href="/drivers", px=4, py=2, rounded="md", _hover={"bg": "blue.100"}),
                rx.link("Maintenance", href="/maintenance", px=4, py=2, rounded="md", _hover={"bg": "blue.100"}),
                spacing="2",
            ),
            py=4,
            width=["100%", "80%", "60%"],
        ),
        bg="white",
        shadow="sm",
        as_="header",
        role="navigation",
        aria_label="Main navigation",
    )
