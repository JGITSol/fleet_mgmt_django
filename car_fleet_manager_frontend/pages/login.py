import reflex as rx
from api_utils import api_client


class LoginState(rx.State):
    username: str = ""
    password: str = ""
    error: str = ""

    def handle_login(self):
        try:
            data = api_client.login(self.username, self.password)
            rx.navigate("/")
        except Exception as e:
            self.error = str(e)

def page():
    return rx.box(
        rx.heading("Login", size="4", mb=4),
        rx.form(
            rx.input(
                value=LoginState.username,
                on_change=lambda v: LoginState.set_username(v),
                placeholder="Username",
                required=True,
                mb=2,
                aria_label="Username"
            ),
            rx.input(
                value=LoginState.password,
                on_change=lambda v: LoginState.set_password(v),
                placeholder="Password",
                type="password",
                required=True,
                mb=4,
                aria_label="Password"
            ),
            rx.button("Login", type="submit", on_click=LoginState.handle_login, color_scheme="blue", width="100%", mb=2),
            rx.cond(LoginState.error, rx.text(LoginState.error, color="red.600", mb=2)),
            on_submit=LoginState.handle_login,
            width="100%",
            aria_label="Login form"
        ),
        width=["100%", "90%", "400px"],
        mx="auto",
        mt=16,
        p=8,
        bg="white",
        rounded="md",
        shadow="md",
        as_="main"
    )
