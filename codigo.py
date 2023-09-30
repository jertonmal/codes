import flet as ft
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")


def main(page):
    text = ft.Text("JChat")
    chat = ft.Column()
    user_name = ft.TextField(label="User Name:")

    def send_tunnel_msg(msg):
        tipo = msg["type"]
        if tipo == "msg":
            text_msg = msg["text"]
            user_msg = msg["user"]
            chat.controls.append(ft.Text(f"{user_msg}: {text_msg}"))
        else:
            user_msg = msg["user"]
            chat.controls.append(ft.Text(f"{user_msg} joined the chat ({current_time}).",
                                         size=12, italic=True, color=ft.colors.RED_600))
        page.update()

    page.pubsub.subscribe(send_tunnel_msg)

    def send_msg(e):
        page.pubsub.send_all({"text": msg_field.value,
                              "user": user_name.value,
                              "type": "msg"})
        msg_field.value = ""
        page.update()

    msg_field = ft.TextField(label="Type a message:", on_submit=send_msg)
    send_msg_button = ft.ElevatedButton("Enviar", on_click=send_msg)

    def enter_popup(e):
        page.pubsub.send_all({"user": user_name.value, "type": "enter"})
        page.add(chat)
        popup.open = False
        page.remove(start_button)
        page.remove(text)
        page.add(ft.Row([msg_field, send_msg_button]))
        page.update()

    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Welcome to JChat"),
        content=user_name,
        actions=[ft.ElevatedButton("Enter", on_click=enter_popup)],
    )

    def enter_chat(e):
        page.dialog = popup
        popup.open = True
        page.update()

    start_button = ft.ElevatedButton("Start chat", on_click=enter_chat)

    page.add(text)
    page.add(start_button)


ft.app(target=main, view=ft.WEB_BROWSER, port=1811)
