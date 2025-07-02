import streamlit as st
from datetime import date
import manajer
from tugas import Tugas, TugasPrioritas

manajer.init_db()
st.title("📋 To-Do List Mahasiswa")
st.caption("Tambahkan tugas kalian di bawah ini!")

# Form Tambah Tugas
with st.form("form_tugas"):
    nama = st.text_input("Nama Tugas")
    deadline = st.date_input("Deadline", min_value=date.today())
    kategori = st.text_input("Kategori", value="Umum")
    prioritas = st.selectbox("Prioritas", ["Tinggi", "Sedang", "Rendah"])
    submitted = st.form_submit_button("Tambah Tugas")

    if submitted and nama:
        manajer.tambah_tugas(nama, deadline, kategori, prioritas)
        st.success("Tugas berhasil ditambahkan!")
        st.rerun()

# Ambil semua tugas dari database
raw_data = manajer.ambil_semua_tugas()
semua_tugas = []
for row in raw_data:
    if len(row) == 7:
        tugas = TugasPrioritas(*row)
    else:
        tugas = Tugas(*row[:-1])
    semua_tugas.append(tugas)

# Ringkasan
st.subheader("📊 Ringkasan")
total = len(semua_tugas)
selesai = len([t for t in semua_tugas if t.status_selesai])
belum = total - selesai
persen = int((selesai / total) * 100) if total > 0 else 0
st.metric("Total", total)
st.metric("Selesai", selesai)
st.metric("Belum", belum)
st.progress(persen / 100)

# Daftar Tugas
st.subheader("📚 Daftar Tugas")
for t in semua_tugas:
    col1, col2, col3 = st.columns([4, 2, 2])

    with col1:
        st.write(t.deskripsi())
        st.caption(f"Sisa hari: {t.sisa_hari()} hari")
        with st.expander("✏️ Edit Tugas", expanded=False):
            with st.form(f"form_edit_{t.id}", clear_on_submit=False):
                new_nama = st.text_input("Edit Nama", value=t.nama)
                new_deadline = st.date_input("Edit Deadline", value=t.deadline)
                new_kategori = st.text_input("Edit Kategori", value=t.kategori)
                new_prioritas = st.selectbox(
                    "Edit Prioritas",
                    ["Tinggi", "Sedang", "Rendah"],
                    index=["Tinggi", "Sedang", "Rendah"].index(
                        t.level_prioritas if hasattr(t, "level_prioritas") else "Sedang"
                    )
                )
                new_status = st.selectbox("Status", ["Belum", "Selesai"], index=1 if t.status_selesai else 0)
                submit_edit = st.form_submit_button("Simpan Perubahan")

                if submit_edit:
                    status_selesai = 1 if new_status == "Selesai" else 0
                    tanggal_pengumpulan = date.today().isoformat() if status_selesai else None
                    manajer.edit_tugas(
                        t.id,
                        new_nama,
                        new_deadline,
                        new_kategori,
                        new_prioritas,
                        status_selesai,
                        tanggal_pengumpulan
                    )
                    st.success("Tugas berhasil diubah!")
                    st.rerun()

    with col2:
        if not t.status_selesai:
            if st.button("Tandai Selesai ✅", key=f"selesai_{t.id}"):
                manajer.tandai_selesai(t.id, date.today())
                st.rerun()

    with col3:
        if st.button("Hapus ❌", key=f"hapus_{t.id}"):
            manajer.hapus_tugas(t.id)
            st.rerun()
