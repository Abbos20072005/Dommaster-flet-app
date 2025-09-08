import flet as ft
from .controllers.catalog_controllers import catalog_categories_data

def catalog_page(page):
    page.clean()
    page.overlay.clear()
    page.appbar = ft.AppBar(
        title=ft.Text(
            value="Catalog"
        ),
        center_title=False,
        force_material_transparency=True
    )
    page.scroll = ft.ScrollMode.ALWAYS

    page.add(
        ft.SafeArea(
            content=ft.Container(
                padding=10,
                content=catalog_categories_data()
            )
        )
    )
