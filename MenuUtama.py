import flet as ft
from db import *
import math


class MenuUtama:
    def __init__(
        self, page, mangas, search_bar, go_home_callback, lihat_manga_callback, all_button, wishlist_button, ongoing_button, finished_button
    ):
        self.page = page
        self.mangas = mangas
        self.search_bar = search_bar
        self.go_home_callback = go_home_callback
        self.lihat_manga_callback = lihat_manga_callback
        self.all_button = all_button
        self.wishlist_button = wishlist_button
        self.ongoing_button = ongoing_button
        self.finished_button = finished_button
        self.row = []
        self.page.auto_scroll=True

    def update_mangas(self, mangas):
        self.mangas = mangas

    def hapus_manga(self, judul):
        delete_manga(judul)
        print(judul)
        self.mangas = get_all_manga()
        self.display_mangas()
        self.page.update()

    def mulai_baca(self, judul):
        ganti_status_manga(judul, "ongoing")
        self.mangas = get_all_manga()
        self.display_mangas()
        self.page.update()

    def selesai_baca(self, judul):
        ganti_status_manga(judul, "finished")
        self.mangas = get_all_manga()
        self.display_mangas()
        self.page.update()

    def baca_ulang(self, judul):
        ganti_status_manga(judul, "ongoing")
        self.mangas = get_all_manga()
        self.display_mangas()
        self.page.update()

    def display_mangas(self, filtered_mangas=None):
        mangas_to_display = filtered_mangas if filtered_mangas else self.mangas
        self.row.clear()
        button = ft.ElevatedButton()

        for manga in mangas_to_display:
            if manga[1] == "finished":
                status = "Finished"
                status_color = ft.colors.LIGHT_GREEN_ACCENT_400
                button = ft.ElevatedButton(
                    "Baca Ulang",
                    top=20,
                    right=200,
                    on_click=lambda e, judul=manga[0]: self.baca_ulang(judul),
                )

            elif manga[1] == "ongoing":
                status = "Ongoing"
                status_color = ft.colors.ORANGE_100
                button = ft.ElevatedButton(
                    "Selesai Baca",
                    top=20,
                    right=200,
                    on_click=lambda e, judul=manga[0]: self.selesai_baca(judul),
                )

            else:
                status = "Wishlist"
                status_color = ft.colors.GREY
                button = ft.ElevatedButton(
                    "Mulai Baca",
                    top=20,
                    right=200,
                    on_click=lambda e, judul=manga[0]: self.mulai_baca(judul),
                )

            self.row.append(
                ft.Stack(
                    [
                        ft.Container(
                            height=70,
                            border_radius=10,
                            border=ft.Border(
                                top=ft.BorderSide(width=1),
                                bottom=ft.BorderSide(width=1),
                                left=ft.BorderSide(width=1),
                                right=ft.BorderSide(width=1),
                            ),
                        ),
                        ft.Text(
                            max_lines=1,
                            overflow=ft.TextOverflow.CLIP,
                            top=20,
                            right=100,
                            value=status,
                            size=20,
                            color=status_color,
                        ),
                        ft.Text(
                            max_lines=1,
                            overflow=ft.TextOverflow.CLIP,
                            top=20,
                            left=20,
                            value=manga[0],
                            size=20,
                        ),
                        ft.Container(
                            height=70,
                            border_radius=10,
                            on_click=self.lihat_manga_callback,
                            data=manga,
                        ),
                        button,
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            right=5,
                            top=10,
                            on_click=lambda e, judul=manga[0]: self.hapus_manga(judul),
                        ),
                    ]
                )
            )

        # manga_buttons = [
        #     ft.ElevatedButton(
        #         manga[0], on_click=self.lihat_manga_callback, data=manga
        #     )
        #     for manga in mangas_to_display
        # ]

        self.page.controls[0].controls = [self.all_button, self.wishlist_button, self.ongoing_button, self.finished_button]
        self.page.controls[-1].controls = [self.search_bar] + self.row
        self.page.update()
