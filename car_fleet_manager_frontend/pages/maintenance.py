import reflex as rx
from api_utils import api_client
from components.footer import footer
from components.header import header


class MaintenanceState(rx.State):
    maintenance: list = []
    loading: bool = True
    error: str = ""
    show_add: bool = False
    form: dict = {}
    editing: dict = None

    def fetch_maintenance(self):
        self.loading = True
        try:
            self.maintenance = api_client.get_maintenance()
            self.error = ""
        except Exception as e:
            self.error = str(e)
        self.loading = False

    def handle_add(self):
        try:
            api_client.create_maintenance(self.form)
            self.fetch_maintenance()
            self.show_add = False
            self.form = {}
        except Exception as e:
            self.error = str(e)

    def handle_edit(self, item):
        self.editing = item
        self.form = item.copy()
        self.show_add = True

def page():
    return rx.box(
        header(),
        rx.button("Load Maintenance", on_click=MaintenanceState.fetch_maintenance),
        # ... render your maintenance, loading, error, etc. using MaintenanceState
        footer(),
    )

    def handle_update():
        try:
            api_client.update_maintenance(state["editing"]["id"], state["form"])
            fetch_maintenance()
            state["show_add"] = False
            state["editing"] = None
            state["form"] = {}
        except Exception as e:
            state["error"] = str(e)

    def handle_delete(item_id):
        try:
            api_client.delete_maintenance(item_id)
            fetch_maintenance()
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
            rx.heading("Maintenance", size="xl", mb=4),
            rx.text("Track and schedule vehicle maintenance.", mb=4),
            rx.cond(state["loading"], rx.spinner("Loading maintenance...", color="blue.600", mb=4)),
            rx.cond(state["error"], rx.text(state["error"], color="red.600", mb=4)),
            rx.button("Add Maintenance", on_click=lambda: state.update({"show_add": True, "editing": None, "form": {}}), color_scheme="blue", mb=4, aria_label="Add maintenance"),
            rx.cond(
                state["show_add"],
                rx.form(
                    form_field("Vehicle ID", "vehicle"),
                    form_field("Description", "description"),
                    form_field("Date", "date", type_="date"),
                    form_field("Cost", "cost", type_="number"),
                    form_field("Status", "status"),
                    rx.hstack(
                        rx.button(
                            "Save" if not state["editing"] else "Update",
                            type="submit",
                            color_scheme="green",
                            on_click=handle_add if not state["editing"] else handle_update,
                            aria_label="Save maintenance"
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
                    aria_label="Maintenance form"
                )
            ),
            rx.cond(
                not state["loading"] and not state["maintenance"],
                rx.text("No maintenance records found.", color="gray.600", mb=4)
            ),
            rx.cond(
                state["maintenance"],
                rx.table(
                    rx.thead(
                        rx.tr(
                            rx.th("Vehicle ID"), rx.th("Description"), rx.th("Date"), rx.th("Cost"), rx.th("Status"), rx.th("Actions"),
                        )
                    ),
                    rx.tbody(
                        *[
                            rx.tr(
                                rx.td(m.get("vehicle", "")),
                                rx.td(m.get("description", "")),
                                rx.td(m.get("date", "")),
                                rx.td(m.get("cost", "")),
                                rx.td(m.get("status", "")),
                                rx.td(
                                    rx.button("Edit", on_click=lambda m=m: handle_edit(m), size="sm", color_scheme="blue", aria_label=f"Edit {m.get('description','')}"),
                                    rx.button("Delete", on_click=lambda m_id=m["id"]: handle_delete(m_id), size="sm", color_scheme="red", ml=2, aria_label=f"Delete {m.get('description','')}"),
                                    spacing=2
                                ),
                                key=m["id"]
                            )
                            for m in state["maintenance"]
                        ]
                    ),
                    width="100%",
                    variant="simple",
                    aria_label="Maintenance table"
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
