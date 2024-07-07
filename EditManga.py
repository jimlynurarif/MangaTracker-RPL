import flet as ft
from db import *


class EditManga:
    def __init__(self, page, go_home_callback):
        self.page = page
        self.go_home_callback = go_home_callback

    def ubah_manga(self, manga):
        self.edit_status = ft.Dropdown(
            label="Status*",
            value=manga[1],
            options=[
                ft.dropdown.Option("ongoing"),
                ft.dropdown.Option("finished"),
                ft.dropdown.Option("wishlist"),
            ],
            on_change=lambda _: self.ubah_sesuai_status(manga),
        )
        # self.page.controls[-1].controls = [self.edit_status]
        # self.page.update()
        self.ubah_sesuai_status(manga)

    def ubah_sesuai_status(self, manga):
        self.edit_judul = ft.TextField(label="Judul*", value=manga[0])
        self.new_genre = ft.TextField(label="Genre", value=get_genre_by_judul(manga[0]))

        self.edit_chapter = ft.TextField(label="Chapter", value=manga[2])
        self.edit_chapterCnt = ft.TextField(
            label="Jumlah Chapter*", value=str(manga[3])
        )

        added_date_label = ft.Text("Tanggal Ditambahkan")
        date_button_a = ft.ElevatedButton(
            "Pick date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: self.edit_addedDate.pick_date(),
        )
        self.edit_addedDate = ft.DatePicker(
            value=manga[4],
            on_change=self.tampilkan_addedDate_terpilih,
        )
        self.added_date_value = ft.Text(manga[4])

        last_read_label = ft.Text("Tanggal Terakhir dibaca")
        date_button_b = ft.ElevatedButton(
            "Pick date",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: self.edit_lastRead.pick_date(),
        )
        self.edit_lastRead = ft.DatePicker(
            value=manga[5],
            on_change=self.tampilkan_lastRead_terpilih,
        )
        self.last_read_value = ft.Text(manga[5])

        self.edit_notes = ft.TextField(label="Notes", value=manga[6])

        save_button = ft.ElevatedButton(
            "Simpan", on_click=lambda _: self.simpan_perubahan(manga[0])
        )
        cancel_button = ft.ElevatedButton(
            "Batal", on_click=lambda _: self.go_home_callback(None)
        )

        # hapus tombol lihat manga berdasarkan status
        self.page.controls[0].controls = []

        if self.edit_status.value == "wishlist":
            self.page.controls[-1].controls = [
                self.edit_status,
                self.edit_judul,
                self.edit_chapterCnt,
                save_button,
                cancel_button,
            ]
        else:
            self.page.controls[-1].controls = [
                self.edit_status,
                self.edit_judul,
                self.new_genre,
                self.edit_chapter,
                self.edit_chapterCnt,
                added_date_label,
                date_button_a,
                self.added_date_value,
                self.edit_addedDate,
                last_read_label,
                date_button_b,
                self.last_read_value,
                self.edit_lastRead,
                self.edit_notes,
                save_button,
                cancel_button,
            ]
        self.page.update()

    def tampilkan_addedDate_terpilih(self, e):
        self.added_date_value.value = self.edit_addedDate.value.strftime("%Y-%m-%d")
        print(self.added_date_value.value)
        self.page.update()

    def tampilkan_lastRead_terpilih(self, e):
        self.last_read_value.value = self.edit_lastRead.value.strftime("%Y-%m-%d")
        print(self.last_read_value.value)
        self.page.update()

    def simpan_perubahan(self, judulawal):
        if self.edit_chapter.value != "":
            self.edit_chapter.value = str(self.edit_chapter.value)
        if (
            self.edit_judul.value == ""
            or self.edit_status.value == ""
            or self.edit_chapterCnt.value == ""
        ):
            alert_dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Judul, Status, dan Jumlah Chapter harus diisi."),
            )
            self.page.dialog = alert_dialog
            alert_dialog.open = True
            self.page.update()

        elif not self.edit_chapterCnt.value.isdigit() or (
            not self.edit_chapter.value.isdigit() and self.edit_chapter.value != ""
        ):
            alert_dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("Chapter harus diisi angka"),
            )
            self.page.dialog = alert_dialog
            alert_dialog.open = True
            self.page.update()
        else:
            judul = self.edit_judul.value
            status = self.edit_status.value
            chapter = ""
            if self.edit_chapter.value != "":
                chapter = int(self.edit_chapter.value)
            chapter_count = int(self.edit_chapterCnt.value)
            added_date = self.added_date_value.value
            last_read = self.last_read_value.value
            personal_notes = self.edit_notes.value
            genre = [g.strip() for g in self.new_genre.value.split(",")]
            # Call the update function
            ubah_manga(
                judulawal,
                judul,
                status,
                chapter,
                chapter_count,
                added_date,
                last_read,
                personal_notes,
                genre,
            )

            # Navigate back to the home screen
            self.go_home_callback(None)
