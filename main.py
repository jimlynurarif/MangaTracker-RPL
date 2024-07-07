import flet as ft
from db import *
from MenuUtama import MenuUtama
from tambahManga import TambahManga
from EditManga import EditManga
from lihatManga import LihatManga


class MangaTrackerApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Manga Tracker"
        self.mangas = get_all_manga()

        self.page.appbar = ft.AppBar(
            title=ft.Row(
                controls=[
                    ft.Image(src="./assets/logo.png", width=40, height=40),
                    ft.Text("Manga Tracker"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(icon=ft.icons.HOME, on_click=self.go_home),
                ft.IconButton(icon=ft.icons.ADD, on_click=self.tambah_manga),
            ],
        )

        self.search_bar = ft.TextField(
            hint_text="Cari Manga...",
            on_change=self.cari_manga,
            expand=False,
        )

        self.all_button = ft.ElevatedButton(
            text="All",
            on_click= self.manga_based_status_all
        )
        self.wishlist_button = ft.ElevatedButton(
            text="Wishlist",
            on_click= self.manga_based_status_wishlist
        )
        self.ongoing_button = ft.ElevatedButton(
            text="Ongoing",
            on_click= self.manga_based_status_ongoing
        )
        self.finished_button = ft.ElevatedButton(
            text="Finished",
            on_click= self.manga_based_status_finished
        )

        self.page.add(ft.Row(controls=[
            self.all_button, self.wishlist_button, self.ongoing_button, self.finished_button
        ]))

        self.page.add(ft.Column(controls=[self.search_bar,]))

        self.menu_utama = MenuUtama(
            self.page, self.mangas, self.search_bar, self.go_home, self.lihat_manga, self.all_button, self.wishlist_button, self.ongoing_button, self.finished_button
        )
        self.menu_utama.display_mangas()

        self.tambah_manga_page = TambahManga(self.page, self.mangas, self.go_home)
        self.edit_manga_page = EditManga(self.page, self.go_home)
        self.lihat_manga_page = LihatManga(
            self.page, self.edit_manga_page.ubah_manga, self.go_home
        )
    def manga_based_status_all(self, e):
        self.menu_utama.display_mangas()
        self.page.update()

    def manga_based_status_wishlist(self, e):
        filtered_mangas = [manga for manga in self.mangas if manga[1] == "wishlist"]
        self.menu_utama.display_mangas(filtered_mangas)
        self.page.update()

    def manga_based_status_ongoing(self, e):
        filtered_mangas = [manga for manga in self.mangas if manga[1] == "ongoing"]
        self.menu_utama.display_mangas(filtered_mangas)
        self.page.update()

    def manga_based_status_finished(self, e):
        filtered_mangas = [manga for manga in self.mangas if manga[1] == "finished"]
        self.menu_utama.display_mangas(filtered_mangas)
        self.page.update()

    def cari_manga(self, e):
        query = e.control.value.lower()
        filtered_mangas = [manga for manga in self.mangas if query in manga[0].lower()]
        if filtered_mangas == [] and len(query) > 0:
            # hapus tombol lihat manga berdasarkan status
            self.page.controls[0].controls = []

            self.page.controls[-1].controls = [
                self.search_bar,
                ft.Text("Manga tidak ditemukan"),
            ] + [ft.ElevatedButton("Go Home", on_click=self.go_home)]
        else:
            self.menu_utama.display_mangas(filtered_mangas)
        self.page.update()

    def lihat_manga(self, e=None, manga=None):
        self.lihat_manga_page.lihat_manga(e, manga)

    def tambah_manga(self, e):
        self.page.route = "/tambah"
        self.tambah_manga_page.tampilkan_form_tambah_manga()
        self.page.update()

    def go_home(self, e):
        self.page.route = "/"
        self.mangas = get_all_manga()
        self.menu_utama.update_mangas(self.mangas)
        self.menu_utama.display_mangas()


def main(page: ft.Page):
    page.scroll = ft.ScrollMode.ALWAYS
    app = MangaTrackerApp(page)

    def route_change(route):
        if route == "/":
            app.menu_utama.display_mangas()
        elif route == "/tambah":
            app.tambah_manga_page.tampilkan_form_tambah_manga()

    page.on_route_change = route_change
    page.go("/")


ft.app(target=main)
