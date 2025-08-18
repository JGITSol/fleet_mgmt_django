import reflex as rx
from components.header import header
from components.footer import footer
from api_utils import api_client

class DriversState(rx.State):
    drivers: list = []
    loading: bool = True
    error: str = ""
    show_add: bool = False
    form: dict = {}
    editing: dict = None

    def fetch_drivers(self):
        self.loading = True
        try:
            self.drivers = api_client.get_drivers()
            self.error = ""
        except Exception as e:
            self.error = str(e)
        self.loading = False

    def handle_add(self):
        try:
            api_client.create_driver(self.form)
            self.fetch_drivers()
            self.show_add = False
            self.form = {}
        except Exception as e:
            self.error = str(e)

    def handle_edit(self, driver):
        self.editing = driver
        self.form = driver.copy()
        self.show_add = True

def page():
    return rx.box(
        header(),
        rx.button("Load Drivers", on_click=DriversState.fetch_drivers),
        # ... render your drivers, loading, error, etc. using DriversState
        footer(),
    )

    def handle_update():
        try:
            api_client.update_driver(state["editing"]["id"], state["form"])
            fetch_drivers()
            state["show_add"] = False
            state["editing"] = None
            state["form"] = {}
        except Exception as e:
            state["error"] = str(e)

    def handle_delete(driver_id):
        try:
            api_client.delete_driver(driver_id)
            fetch_drivers()
        except Exception as e:
            state["error"] = str(e)

    def form_field(label, key, type_="text"):
        return rx.form_control(
            rx.form_label(label, html_for=key),
            rx.input(
                id=key,
                value=state["form"].get(key, ""),
                on_change=lambda v: state["form"].update({key: v}),
                type=type_,
                aria_label=label,
                required=True
            ),
            mb=2
        )

    return rx.box(
        header(),
        rx.container(
            rx.heading("Drivers", size="xl", mb=4),
            rx.text("Manage and view all drivers in your fleet.", mb=4),
            rx.cond(state["loading"], rx.spinner("Loading drivers...", color="blue.600", mb=4)),
            rx.cond(state["error"], rx.text(state["error"], color="red.600", mb=4)),
            rx.button("Add Driver", on_click=lambda: state.update({"show_add": True, "editing": None, "form": {}}), color_scheme="blue", mb=4, aria_label="Add driver"),
            rx.cond(
                state["show_add"],
                rx.form(
                    form_field("First Name", "first_name"),
                    form_field("Last Name", "last_name"),
                    form_field("License Number", "license_number"),
                    form_field("Phone", "phone"),
                    form_field("Email", "email", type_="email"),
                    rx.hstack(
                        rx.button(
                            "Save" if not state["editing"] else "Update",
                            type="submit",
                            color_scheme="green",
                            on_click=handle_add if not state["editing"] else handle_update,
                            aria_label="Save driver"
                        ),
                        rx.button("Cancel", on_click=lambda: state.update({"show_add": False, "editing": None, "form": {}}), aria_label="Cancel add/edit", color_scheme="gray"),
                        spacing=4
                    ),
                    bg="gray.100",
                    p=6,
                    rounded="md",
                    shadow="md",
                    mb=6,
                    width="100%",
                    aria_label="Driver form"
                )
            ),
            rx.cond(
                not state["loading"] and not state["drivers"],
                rx.text("No drivers found.", color="gray.600", mb=4)
            ),
            rx.cond(
                state["drivers"],
                rx.table(
                    rx.thead(
                        rx.tr(
                            rx.th("First Name"), rx.th("Last Name"), rx.th("License #"), rx.th("Phone"), rx.th("Email"), rx.th("Actions"),
                        )
                    ),
                    rx.tbody(
                        *[
                            rx.tr(
                                rx.td(d.get("first_name", "")),
                                rx.td(d.get("last_name", "")),
                                rx.td(d.get("license_number", "")),
                                rx.td(d.get("phone", "")),
                                rx.td(d.get("email", "")),
                                rx.td(
                                    rx.button("Edit", on_click=lambda d=d: handle_edit(d), size="sm", color_scheme="blue", aria_label=f"Edit {d.get('first_name','')} {d.get('last_name','')}"),
                                    rx.button("Delete", on_click=lambda d_id=d["id"]: handle_delete(d_id), size="sm", color_scheme="red", ml=2, aria_label=f"Delete {d.get('first_name','')} {d.get('last_name','')}"),
                                    spacing=2
                                ),
                                key=d["id"]
                            )
                            for d in state["drivers"]
                        ]
                    ),
                    width="100%",
                    variant="simple",
                    aria_label="Drivers table"
                )
            ),
            width=["100%", "80%", "60%"],
            py=8,
        ),
        footer(),
        as_="main",
        min_height="100vh",
        bg="gray.50"
    )
