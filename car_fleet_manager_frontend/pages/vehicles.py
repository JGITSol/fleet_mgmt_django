import reflex as rx
from api_utils import api_client
from components.footer import footer
from components.header import header


class VehiclesState(rx.State):
    vehicles: list = []
    loading: bool = True
    error: str = ""
    show_add: bool = False
    form: dict = {}
    editing: dict = None

    def fetch_vehicles(self):
        self.loading = True
        try:
            self.vehicles = api_client.get_vehicles()
            self.error = ""
        except Exception as e:
            self.error = str(e)
        self.loading = False

    def handle_add(self):
        try:
            api_client.create_vehicle(self.form)
            self.fetch_vehicles()
            self.show_add = False
            self.form = {}
        except Exception as e:
            self.error = str(e)

    def handle_edit(self, vehicle):
        self.editing = vehicle
        self.form = vehicle.copy()
        self.show_add = True

def page():
    return rx.box(
        header(),
        rx.button("Load Vehicles", on_click=VehiclesState.fetch_vehicles),
        # ... render your vehicles, loading, error, etc. using VehiclesState
        footer(),
    )

    def handle_update():
        try:
            api_client.update_vehicle(state["editing"]["id"], state["form"])
            fetch_vehicles()
            state["show_add"] = False
            state["editing"] = None
            state["form"] = {}
        except Exception as e:
            state["error"] = str(e)

    def handle_delete(vehicle_id):
        try:
            api_client.delete_vehicle(vehicle_id)
            fetch_vehicles()
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
            rx.heading("Vehicles", size="xl", mb=4),
            rx.text("Manage and view all vehicles in your fleet.", mb=4),
            rx.cond(state["loading"], rx.spinner("Loading vehicles...", color="blue.600", mb=4)),
            rx.cond(state["error"], rx.text(state["error"], color="red.600", mb=4)),
            rx.button("Add Vehicle", on_click=lambda: state.update({"show_add": True, "editing": None, "form": {}}), color_scheme="blue", mb=4, aria_label="Add vehicle"),
            rx.cond(
                state["show_add"],
                rx.form(
                    form_field("Brand", "brand"),
                    form_field("Model", "model"),
                    form_field("Year", "year", type_="number"),
                    form_field("License Plate", "license_plate"),
                    form_field("VIN", "vin"),
                    form_field("Color", "color"),
                    form_field("Fuel Type", "fuel_type"),
                    form_field("Transmission", "transmission"),
                    form_field("Vehicle Type", "vehicle_type"),
                    form_field("Mileage", "mileage", type_="number"),
                    form_field("Last Service Date", "last_service_date", type_="date"),
                    form_field("Next Service Date", "next_service_date", type_="date"),
                    form_field("Insurance Expiry", "insurance_expiry", type_="date"),
                    form_field("Status", "status"),
                    rx.hstack(
                        rx.button(
                            "Save" if not state["editing"] else "Update",
                            type="submit",
                            color_scheme="green",
                            on_click=handle_add if not state["editing"] else handle_update,
                            aria_label="Save vehicle"
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
                    aria_label="Vehicle form"
                )
            ),
            rx.cond(
                not state["loading"] and not state["vehicles"],
                rx.text("No vehicles found.", color="gray.600", mb=4)
            ),
            rx.cond(
                state["vehicles"],
                rx.table(
                    rx.thead(
                        rx.tr(
                            rx.th("Brand"), rx.th("Model"), rx.th("Year"), rx.th("License Plate"), rx.th("VIN"), rx.th("Status"), rx.th("Actions"),
                        )
                    ),
                    rx.tbody(
                        *[
                            rx.tr(
                                rx.td(v.get("brand", "")),
                                rx.td(v.get("model", "")),
                                rx.td(v.get("year", "")),
                                rx.td(v.get("license_plate", "")),
                                rx.td(v.get("vin", "")),
                                rx.td(v.get("status", "")),
                                rx.td(
                                    rx.button("Edit", on_click=lambda v=v: handle_edit(v), size="sm", color_scheme="blue", aria_label=f"Edit {v.get('brand','')} {v.get('model','')}"),
                                    rx.button("Delete", on_click=lambda v_id=v["id"]: handle_delete(v_id), size="sm", color_scheme="red", ml=2, aria_label=f"Delete {v.get('brand','')} {v.get('model','')}"),
                                    spacing=2
                                ),
                                key=v["id"]
                            )
                            for v in state["vehicles"]
                        ]
                    ),
                    width="100%",
                    variant="simple",
                    aria_label="Vehicles table"
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
