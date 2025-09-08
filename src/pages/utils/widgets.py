import flet as ft
from math import floor

def on_navigation_bar(e):
    from pages.home import home_page
    from pages.catalog import catalog_page
    from pages.cart import cart_page
    from pages.favourites import favourites_page
    from pages.profile import profile_page

    if e.control.selected_index == 0:
        home_page(e.page)
    elif e.control.selected_index == 1:
        catalog_page(e.page)
    elif e.control.selected_index == 2:
        cart_page(e.page)
    elif e.control.selected_index == 3:
        favourites_page(e.page)
    elif e.control.selected_index == 4:
        profile_page(e.page)

def rating_row(value: float, reviews: int = None, size: int = 16, color: str = "#E31B23"):
    # Round to nearest 0.5
    v = round(value * 2) / 2
    full = floor(v)
    half = 1 if (v - full) >= 0.5 else 0
    empty = 5 - full - half

    stars = []
    for _ in range(full):
        stars.append(ft.Icon(ft.Icons.STAR, size=size, color=color))
    if half:
        stars.append(ft.Icon(ft.Icons.STAR_HALF, size=size, color=color))
    for _ in range(empty):
        stars.append(ft.Icon(ft.Icons.STAR_BORDER, size=size, color=color))

    if reviews is not None:
        stars.append(ft.Text(f"({reviews})", size=size-2, color=ft.Colors.GREY_600))

    return ft.Row(controls=stars, spacing=1, vertical_alignment=ft.CrossAxisAlignment.CENTER)

def quantity_number():
    txt_number = ft.Text(
        value="0",
        size=12,
        color=ft.Colors.BLACK,
    )

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)


    return ft.Container(
        adaptive=True,
        border_radius=10,
        height=30,
        padding=0,
        bgcolor=ft.Colors.GREY_200,
        alignment=ft.Alignment.CENTER_LEFT,
        content=ft.Row(
            expand=True,
            adaptive=True,
            spacing=0,
            controls=[
                ft.IconButton(
                    icon=ft.Icons.REMOVE, 
                    icon_size=0,
                    padding=0,
                    on_click=minus_click
                ),
                txt_number,
                ft.IconButton(
                    icon=ft.Icons.ADD,
                    icon_size=0,
                    padding=0,
                    on_click=plus_click
                ),
            ],
        )
    )
    





