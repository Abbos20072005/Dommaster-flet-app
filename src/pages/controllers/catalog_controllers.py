import flet as ft
import httpx

def catalog_categories_data():
    urls = f"https://api.dommaster.uz/api/v1/categories/"
    headers = {
        "Content-Type": "application/json",
        # "Authorization": f"Bearer {access_token}",
        # "Accept-Language": language
    }
    responses = httpx.get(url=urls, headers=headers)
    categories_data = ft.GridView(
        expand=True,
        max_extent=150
    )

    if responses.status_code == 200:
        categories = responses.json().get("result")
        for category in categories:
            categories_data.controls.append(
                ft.Button(
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=20)
                    ),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                value=category.get("name"),
                                size=10,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Image(
                                src=category.get("image"),
                                width=60,
                                height=60
                            )
                        ]
                    )
                )
            )
        return categories_data
    

