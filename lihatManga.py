import flet as ft
from db import *


class LihatManga:
    def __init__(self, page, edit_manga_callback, go_home_callback):
        self.page = page
        self.edit_manga_callback = edit_manga_callback
        self.go_home_callback = go_home_callback

    def lihat_manga(self, e=None, manga=None):
        if manga is None:
            manga = e.control.data

        genres = get_genre_by_judul(manga[0])

        font_size = 20

        manga_details = [
            ft.Text(f"Judul: {manga[0]}", style=ft.TextStyle(size=font_size)),
            ft.Text(f"Status: {manga[1]}", style=ft.TextStyle(size=font_size)),
            ft.Text(f"Chapter: {manga[2]}", style=ft.TextStyle(size=font_size)),
            ft.Text(f"Jumlah Chapter: {manga[3]}", style=ft.TextStyle(size=font_size)),
            ft.Text(f"Added Date: {manga[4]}", style=ft.TextStyle(size=font_size)),
            ft.Text(f"Last Read: {manga[5]}", style=ft.TextStyle(size=font_size)),
            ft.Text(f"Notes: {manga[6]}", style=ft.TextStyle(size=font_size)),
            ft.Text(f"Genre: {genres}", style=ft.TextStyle(size=font_size)),
        ]

        edit_button = ft.ElevatedButton(
            "Ubah Manga", on_click=lambda _: self.edit_manga_callback(manga)
        )
        go_home_button = ft.ElevatedButton(
            "Go Home", on_click=lambda _: self.go_home_callback(None)
        )

        button_row = ft.Row(
            controls=[edit_button, go_home_button],
            alignment="center",  # Menjaga tombol tetap di tengah secara horizontal
            spacing=20,  # Menambahkan spasi antar tombol
        )

        content = manga_details + [button_row]

        # Membuat kontainer dengan alignment di tengah
        centered_container = ft.Container(
            content=ft.Column(
                controls=content, alignment="center", horizontal_alignment="center"
            ),
            alignment=ft.alignment.center,
        )

        # hapus tombol lihat manga berdasarkan status
        self.page.controls[0].controls = []

        self.page.controls[-1].controls = [centered_container]
        self.page.update()
