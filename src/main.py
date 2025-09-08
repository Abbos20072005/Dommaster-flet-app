import flet as ft
from pages.home import home_page

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_200 
      
    home_page(page)  
                                       
ft.run(main, view=ft.AppView.FLET_APP)             
                                