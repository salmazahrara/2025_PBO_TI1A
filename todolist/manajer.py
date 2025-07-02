import sqlite3
from datetime import date

def init_db():
    conn = sqlite3.connect("tugas.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tugas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            deadline TEXT,
            kategori TEXT,
            status_selesai INTEGER DEFAULT 0,
            tanggal_pengumpulan TEXT,
            prioritas TEXT DEFAULT 'Sedang'
        )
    """)
    conn.commit()
    conn.close()

def tambah_tugas(nama, deadline, kategori, prioritas):
    conn = sqlite3.connect("tugas.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO tugas (nama, deadline, kategori, prioritas) 
        VALUES (?, ?, ?, ?)
    """, (nama, deadline.isoformat(), kategori, prioritas))
    conn.commit()
    conn.close()

def ambil_semua_tugas():
    conn = sqlite3.connect("tugas.db")
    c = conn.cursor()
    c.execute("""
        SELECT id, nama, deadline, kategori, status_selesai, 
               tanggal_pengumpulan, prioritas 
        FROM tugas
    """)
    data = c.fetchall()
    conn.close()
    return data

def tandai_selesai(tugas_id, tanggal_pengumpulan):
    conn = sqlite3.connect("tugas.db")
    c = conn.cursor()
    c.execute("""
        UPDATE tugas 
        SET status_selesai = 1, tanggal_pengumpulan = ?
        WHERE id = ?
    """, (tanggal_pengumpulan.isoformat(), tugas_id))
    conn.commit()
    conn.close()

def hapus_tugas(tugas_id):
    conn = sqlite3.connect("tugas.db")
    c = conn.cursor()
    c.execute("DELETE FROM tugas WHERE id = ?", (tugas_id,))
    conn.commit()
    conn.close()

def edit_tugas(tugas_id, nama, deadline, kategori, prioritas, status_selesai, tanggal_pengumpulan):
    conn = sqlite3.connect("tugas.db")
    c = conn.cursor()
    c.execute("""
        UPDATE tugas 
        SET nama = ?, deadline = ?, kategori = ?, prioritas = ?, 
            status_selesai = ?, tanggal_pengumpulan = ?
        WHERE id = ?
    """, (nama, deadline.isoformat(), kategori, prioritas, status_selesai, tanggal_pengumpulan, tugas_id))
    conn.commit()
    conn.close()
