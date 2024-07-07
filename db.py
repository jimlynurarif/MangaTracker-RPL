import sqlite3

def add_manga(
    judul,
    status,
    chapter,
    chapter_count,
    added_date,
    last_read,
    personal_notes,
    genre,
):
    # Menghubungkan ke database
    conn = sqlite3.connect("manga_database.db")
    c = conn.cursor()

    # Menambahkan data manga ke dalam tabel Manga
    c.execute(
        "INSERT INTO Manga (judul, status, chapter_count) VALUES (?, ?, ?)",
        (judul, status, chapter_count),
    )

    if chapter != "":
        c.execute("UPDATE Manga SET chapter = ? WHERE judul = ?", (chapter, judul))

    if added_date != "":
        c.execute("UPDATE Manga SET added_date = ? WHERE judul = ?", (added_date, judul))

    if last_read != "":
        c.execute(
            "UPDATE Manga SET last_read = ? WHERE judul = ?", (last_read, judul)
        )

    if personal_notes:
        c.execute(
            "UPDATE Manga SET personal_notes = ? WHERE judul = ?", (personal_notes, judul)
        )

    # Jika genre disertakan, tambahkan juga ke dalam tabel genre_manga
    if genre != "":
        for g in genre:
            c.execute(
                "INSERT INTO genre_manga (judul, genre) VALUES (?, ?)", (judul, g)
            )

    # Menyimpan perubahan dan menutup koneksi
    conn.commit()
    conn.close()
def ubah_manga(
    judulawal,
    judul,
    status,
    chapter,
    chapter_count,
    added_date,
    last_read,
    personal_notes,
    genre,
):
    # Menghubungkan ke database
    conn = sqlite3.connect("manga_database.db")
    c = conn.cursor()

    # Menambahkan data manga ke dalam tabel Manga
    query = "UPDATE Manga SET judul = ?, status = ?, chapter_count = ?,"
    params = [judul, status, chapter_count]

    if chapter != "":
        query += " chapter = ?,"
        params.append(chapter)

    if added_date != "":
        query += " added_date = ?,"
        params.append(added_date)

    if last_read != "":
        query += " last_read = ?,"
        params.append(last_read)

    if personal_notes:
        query += " personal_notes = ?,"
        params.append(personal_notes)
    query = query.rstrip(',') + " WHERE judul = ?"
    params.append(judulawal)
    c.execute(query, params)
    # Jika genre disertakan, tambahkan juga ke dalam tabel genre_manga

    c.execute("DELETE FROM genre_manga WHERE judul=?", (judulawal,))
    
    if genre != "":
        for g in genre:
            c.execute(
                "INSERT INTO genre_manga (judul, genre) VALUES (?, ?)", (judulawal, g)
            )
            c.execute("UPDATE genre_manga SET judul = ? WHERE judul = ?", (judul, judulawal))

    # Menyimpan perubahan dan menutup koneksi
    conn.commit()
    conn.close()


def get_all_manga():
    # Menghubungkan ke database
    conn = sqlite3.connect("manga_database.db")
    c = conn.cursor()

    # Mengambil data dari tabel Manga dan tabel genre_manga
    c.execute("SELECT * FROM Manga")
    mangas = c.fetchall()

    # Menutup koneksi
    conn.close()

    return mangas

def get_genre_by_judul(judul):
    # Menghubungkan ke database
    conn = sqlite3.connect("manga_database.db")
    c = conn.cursor()

    # Mengambil data dari tabel Manga dan tabel genre_manga
    genre_manga_query = "SELECT genre FROM genre_manga where judul = ?;"
    c.execute(genre_manga_query,(judul,))
    genres = c.fetchall()
    genre_manga = None

    if genres:
        genre_manga = ", ".join(g[0] for g in genres)

    # Menutup koneksi
    conn.close()

    return genre_manga


def ganti_status_manga(judul, status_baru):
    # Menghubungkan ke database
    conn = sqlite3.connect("manga_database.db")
    c = conn.cursor()

    # Memperbarui status manga berdasarkan judul
    c.execute("UPDATE Manga SET status = ? WHERE judul = ?", (status_baru, judul))

    # Menyimpan perubahan dan menutup koneksi
    conn.commit()
    conn.close()

    # # Memberikan konfirmasi bahwa status telah diubah
    # print(f"Status manga dengan judul '{judul}' telah diubah menjadi '{status_baru}'.")


def delete_manga(judul):
    # Menghubungkan ke database
    conn = sqlite3.connect("manga_database.db")
    c = conn.cursor()

    # Menghapus manga dari tabel Manga
    c.execute("DELETE FROM Manga WHERE judul=?", (judul,))

    # Menghapus entri genre manga terkait, jika ada, dari tabel genre_manga
    c.execute("DELETE FROM genre_manga WHERE judul=?", (judul,))

    # Menyimpan perubahan dan menutup koneksi
    conn.commit()
    conn.close()

    # print(f"Manga dengan judul '{judul}' telah dihapus dari database.")


# add_manga(
#     "blah",
#     "ongoing",
#     None,
#     1000,
#     "2024-05-13",
#     "2024-05-13",
#     "Menarik",
#     None,
# )

# Contoh hapu manga
# hapus_manga("One Piece")

# Contoh pemanggilan fungsi
# get_all_manga()
