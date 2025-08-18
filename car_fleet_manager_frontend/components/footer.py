import reflex as rx

def footer():
    return rx.box(
        rx.container(
            rx.text("© 2025 Car Fleet Manager. All rights reserved.", color="gray.600", font_size="sm"),
            py=4,
            width=["100%", "80%", "60%"],
            align="center"
        ),
        bg="white",
        shadow="sm",
        as_="footer",
        role="contentinfo",
    )
