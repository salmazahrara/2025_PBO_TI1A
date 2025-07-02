from datetime import date

class Tugas:
    def __init__(self, id, nama, deadline, kategori, status_selesai, tanggal_pengumpulan):
        self.id = id
        self.nama = nama
        self.deadline = date.fromisoformat(deadline)
        self.kategori = kategori
        self.status_selesai = bool(status_selesai)
        self.tanggal_pengumpulan = (
            date.fromisoformat(tanggal_pengumpulan) if tanggal_pengumpulan else None
        )

    def sisa_hari(self):
        if self.status_selesai:
            return 0
        return max((self.deadline - date.today()).days, 0)

    def deskripsi(self):
        status = "✅ Selesai" if self.status_selesai else "⏳ Belum"
        return f"{self.nama} [{self.kategori}] - Deadline: {self.deadline} - {status}"

class TugasPrioritas(Tugas):
    def __init__(self, id, nama, deadline, kategori, status_selesai, tanggal_pengumpulan, level_prioritas):
        super().__init__(id, nama, deadline, kategori, status_selesai, tanggal_pengumpulan)
        self.level_prioritas = level_prioritas

    def deskripsi(self):
        dasar = super().deskripsi()
        return f"{dasar} | 🔥 Prioritas: {self.level_prioritas}"
