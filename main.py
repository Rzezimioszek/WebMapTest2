import flet as ft


def main(page: ft.Page):

    label = ft.Text("Aqq")
    page.add(label)

    def submit_on_clik(e):
        label.visible = not label.visible
        page.update()

    submit = ft.ElevatedButton("Wprowadź", on_click= lambda e: submit_on_clik(e))

    page.add(submit)

    page.update()

if __name__ == "__main__":
    site = ft.app(main, view=ft.AppView.WEB_BROWSER)