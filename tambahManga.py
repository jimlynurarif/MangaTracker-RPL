import flet as ft
from db import *
import datetime


class TambahManga:
    def __init__(self, page, mangas, go_home_callback):
        self.page = page
        self.mangas = mangas
        self.go_home_callback = go_home_callback

    def tampilkan_form_tambah_manga(self):
        self.new_status = ft.Dropdown(
            label="Status*",
            options=[
                ft.dropdown.Option("ongoing"),
                ft.dropdown.Option("finished"),
                ft.dropdown.Option("wishlist"),
            ],
            on_change=lambda _: self.tampilkan_form_berdasarkan_status(),
        )

        # hapus tombol lihat manga berdasarkan status
        self.page.controls[0].controls = []

        self.page.controls[-1].controls = [self.new_status]
        self.page.update()

    def tampilkan_form_berdasarkan_status(self):

        # hapus tombol lihat manga berdasarkan status
        self.page.controls[0].controls = []

        self.new_judul = ft.TextField(label="Judul*")
        self.new_genre = ft.TextField(label="Genre")

        self.new_chapter = ft.TextField(label="Chapter")
        self.new_chapterCnt = ft.TextField(label="Jumlah Chapter*")

        added_date_label = ft.Text("Tanggal Ditambahkan")
        date_button_a = ft.ElevatedButton(
            "Pick date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: self.new_addedDate.pick_date(),
        )
        self.new_addedDate = ft.DatePicker(
            on_change=self.tampilkan_addedDate_terpilih,
        )
        self.added_date_value = ft.Text()

        last_read_label = ft.Text("Tanggal Terakhir dibaca")
        date_button_b = ft.ElevatedButton(
            "Pick date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: self.new_lastRead.pick_date(),
        )
        self.new_lastRead = ft.DatePicker(
            on_change=self.tampilkan_lastRead_terpilih,
        )
        self.last_read_value = ft.Text()

        self.new_notes = ft.TextField(label="Notes")
        save_button = ft.ElevatedButton("Tambah", on_click=self.simpan_manga_baru)
        cancel_button = ft.ElevatedButton(
            "Batal", on_click=lambda _: self.go_home_callback(None)
        )

        if self.new_status.value == "wishlist":
            self.page.controls[-1].controls = [
                self.new_status,
                self.new_judul,
                self.new_chapterCnt,
                save_button,
                cancel_button,
            ]
        else :
            self.page.controls[-1].controls = [
                self.new_status,
                self.new_judul,
                self.new_genre,
                self.new_chapter,
                self.new_chapterCnt,
                added_date_label,
                ft.Row(
                    controls=[
                        date_button_a,
                        self.added_date_value,
                    ],
                ),
                self.new_addedDate,
                last_read_label,
                ft.Row(
                    controls=[
                        date_button_b,
                        self.last_read_value,
                    ],
                ),
                self.new_lastRead,
                self.new_notes,
                save_button,
                cancel_button,
            ]
        self.page.update()

    def tampilkan_addedDate_terpilih(self, e):
        self.added_date_value.value = self.new_addedDate.value.strftime("%Y-%m-%d")
        print(self.added_date_value.value)
        self.page.update()

    def tampilkan_lastRead_terpilih(self, e):
        self.last_read_value.value = self.new_lastRead.value.strftime("%Y-%m-%d")
        print(self.last_read_value.value)
        self.page.update()

    def simpan_manga_baru(self, e):
        judul = self.new_judul.value
        status = self.new_status.value

        chapter = self.new_chapter.value

        chapter_count = self.new_chapterCnt.value

        added_date = self.added_date_value.value
        last_read = self.last_read_value.value
        personal_notes = self.new_notes.value
        genre = [g.strip() for g in self.new_genre.value.split(",")]
        # print([g.strip() for g in self.new_genre.value.split(",")])

        if judul == "" or status == "" or chapter_count == "":
            alert_dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Judul, Status, dan Jumlah Chapter harus diisi."),
            )
            self.page.dialog = alert_dialog
            alert_dialog.open = True
            self.page.update()

        elif  not chapter_count.isdigit() or (not chapter.isdigit() and chapter !=""):
            alert_dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Chapter harus diisi angka"),
            )
            self.page.dialog = alert_dialog
            alert_dialog.open = True
            self.page.update()

        else:
            chapter_count = int(self.new_chapterCnt.value)
            if chapter != "":
                chapter = int(self.new_chapter.value)
            add_manga(judul,status,chapter,chapter_count,added_date,last_read,personal_notes,genre)

        self.go_home_callback(None)
