import flet as ft
import httpx

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
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=1,
                        controls=[
                            ft.Text(
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                value=category.get("name"),
                                size=10,
                                text_align=ft.TextAlign.CENTER,
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
                    width=120,
                    height=400,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=20)
                    ),
                    content=ft.Column(
                        controls=[
                            ft.Stack(
                                alignment=ft.Alignment(3, -1.8),
                                controls=[
                                    ft.Image(
                                        # fit=ft.BoxFit.COVER,
                                        src=product.get("images")[0].get("image"),
                                        width=80,
                                        height=80
                                    ),
                                    ft.IconButton(
                                        # alignment=ft.Alignment.BOTTOM_RIGHT,
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
                            )
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
                        color=ft.Colors.WHITE,
                        size=10,
                    ),
                    ft.Text(
                        value=main_sale.get("name"),
                        color=ft.Colors.WHITE,
                        size=15,
                    ),
                    products_list
                ]
            )
        )
