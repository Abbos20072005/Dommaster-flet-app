import flet as ft
from pages.controllers.home_controllers import home_categories_data
from pages.controllers.home_controllers import home_banner_data
from pages.controllers.home_controllers import home_main_sale_data
from pages.utils.widgets import on_navigation_bar

def home_page(page):
    page.clean()
    page.appbar = None
    page.navigation_bar = ft.NavigationBar(
        on_change=on_navigation_bar,
        adaptive=True,
        selected_index=0,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME,
                label="Home"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.CATEGORY,
                label="Categories"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SHOP, 
                label="Shop"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.FAVORITE_OUTLINE,
                label="Favorites"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PERSON,
                label="Profile"
            )
        ]
    )
    page.overlay.clear()
    page.overlay.append(
        ft.SafeArea(
            content=ft.Container(
                padding=8,
                height=110,
                bgcolor='white',
                content=ft.Column(
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(
                                            icon=ft.Icons.LOCATION_ON_OUTLINED,
                                            size=30
                                        ),
                                        ft.Text(
                                            value="Tashkent",
                                            size=18
                                        )
                                    ]
                                ),
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.NOTIFICATIONS,
                                            on_click=None
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.PHONE,
                                            # on_click=page.launch_url("tel:+998901234567")
                                        )
                                    ]
                                )
                            ]
                        ),
                        ft.SearchBar(
                            height=40,
                            
                            bar_leading=ft.Icon(
                                icon=ft.Icons.SEARCH
                            ),
                            value="Search something"
                        )
                    ]
                )
            )
        )
    )

    page.add(
        ft.SafeArea(
            content=ft.ListView(
                spacing=10,
                adaptive=True,
                height=page.window.width,
                controls=[
                    ft.Divider(height=120),
                    home_categories_data(),
                    home_banner_data(),
                    home_main_sale_data()
                ]
            )
        )
    )