import flet as ft
import httpx
from pages.utils.widgets import rating_row
from pages.utils.widgets import quantity_number

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
    
def home_categories_data():
    urls = f"https://api.dommaster.uz/api/v1/categories/"
    headers = {
        "Content-Type": "application/json",
        # "Authorization": f"Bearer {access_token}",
        # "Accept-Language": language
    }
    responses = httpx.get(url=urls, headers=headers)
    categories_data = ft.GridView(
        max_extent=130,
        height=230,
        horizontal=True
    )

    if responses.status_code == 200:
        categories = responses.json().get("result")
        for category in categories:
            categories_data.controls.append(
                ft.Button(
                    bgcolor=ft.Colors.GREY_200,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=20)
                    ),
                    content=ft.Stack(
                        alignment=ft.Alignment.TOP_CENTER,
                        controls=[
                            ft.Image(
                                src=category.get("image"),
                                fit=ft.BoxFit.COVER
                            ),
                            ft.Text(
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                value=category.get("name"),
                                size=10,
                                text_align=ft.TextAlign.CENTER
                            )
                        ]
                    )
                )
            )
        return ft.Container(
            content=categories_data,
            bgcolor=ft.Colors.WHITE,
            border_radius=15
        )
    
def home_banner_data():
    urls = f"https://api.dommaster.uz/api/v1/base/banner/"
    headers = {
        "Content-Type": "application/json",
        # "Authorization": f"Bearer {access_token}",
        # "Accept-Language": language
    }
    responses = httpx.get(url=urls, headers=headers)

    banner_data = ft.ListView(
        spacing=5,
        expand=True,
        height=200,
        horizontal=True,
    )

    if responses.status_code == 200:
        banners = responses.json().get("result")
        for banner in banners:
            banner_data.controls.append(
                ft.Button(
                    expand=True,
                    adaptive=True,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=20)
                    ),
                    content=ft.Image(
                        border_radius=20,
                        src=banner.get("mobile_image"),
                    ),
                    url=banner.get("link")
                )
            )
        
        return ft.Container(
            content=banner_data,
            bgcolor=ft.Colors.WHITE,
            border_radius=15
        )
    
def home_main_sale_data():
    urls = f"https://api.dommaster.uz/api/v1/sales/main/"
    headers = {
        "Content-Type": "application/json",
        # "Authorization": f"Bearer {access_token}",
        # "Accept-Language": language
    }
    responses = httpx.get(url=urls, headers=headers)
    products_list = ft.ListView(
        expand=True,
        horizontal=True,
        height=200,
        spacing=10
    )

    if responses.status_code == 200:
        main_sale = responses.json().get("result")
        products = main_sale.get("products")
        for product in products:
            products_list.controls.append(
                ft.Button(
                    width=130,
                    height=400,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=20)
                    ),
                    content=ft.Column(
                        controls=[
                            ft.Stack(
                                alignment=ft.Alignment(3, -2),
                                controls=[
                                    ft.Image(
                                        fit=ft.BoxFit.COVER,
                                        src=product.get("images")[0].get("image"),
                                        width=80,
                                        height=80
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.FAVORITE_BORDER,
                                        style=ft.ButtonStyle(
                                            shape=ft.CircleBorder()
                                        ),
                                        icon_color=ft.Colors.GREY
                                    )
                                ]
                            ),
                            ft.Text(
                                value=product.get("name"),
                                max_lines=3,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                size=10,
                                color=ft.Colors.BLACK
                            ),
                            rating_row(
                                value=product.get("rating"),
                                reviews=product.get("rating"),
                                size=10
                            ),
                            ft.Divider(
                                height=10,
                                color=ft.Colors.TRANSPARENT
                            ),
                            ft.Text(
                                value=f"{product.get("price")} cym",
                                size=12,
                                color=ft.Colors.BLACK
                            ),
                            quantity_number()
                        ]
                    )
                    
                )
            )

        return ft.Container(
            expand=True,
            adaptive=True,
            padding=10,
            height=400,
            border_radius=20,
            image=ft.DecorationImage(
                fit=ft.BoxFit.COVER,
                src=main_sale.get("bg_image")
            ),
            content=ft.Column(
                controls=[
                    ft.Text(
                        value=f"{main_sale.get("discount_from")} - {main_sale.get("discount_to")}",
                        color=ft.Colors.BLACK,
                        size=10,
                    ),
                    ft.Text(
                        value=main_sale.get("name"),
                        color=ft.Colors.BLACK,
                        size=15,
                    ),
                    products_list
                ]
            )
        )
