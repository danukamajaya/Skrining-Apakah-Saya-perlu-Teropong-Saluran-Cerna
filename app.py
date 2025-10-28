# app.py
# Skrining Mandiri Kolonoskopi – versi 1.1 (Bahasa Pasien, 2025)
# © dr. Danu Kamajaya, Sp.PD – RSUP Dr. Kariadi Semarang
# Jalankan dengan: streamlit run app.py

import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Skrining Mandiri Kolonoskopi", page_icon="🧾", layout="centered")

# ------------------ STYLE ------------------
def pill(text, kind="info"):
    colors = {
        "danger": ("#fff", "#dc2626"),
        "warn": ("#111", "#f59e0b"),
        "ok": ("#fff", "#16a34a"),
        "info": ("#fff", "#2563eb"),
        "muted": ("#111", "#9ca3af"),
    }
    fg, bg = colors.get(kind, colors["info"])
    st.markdown(
        f"<span style='padding:6px 10px; border-radius:999px; background:{bg}; color:{fg}; font-size:0.9rem'>{text}</span>",
        unsafe_allow_html=True
    )

def section_title(title):
    st.markdown(f"### {title}")

def hr():
    st.markdown("---")

# ------------------ HEADER ------------------
st.title("🧾 Skrining Mandiri Kolonoskopi")
st.caption("Panduan sederhana untuk membantu mengenali apakah Anda sebaiknya menjalani pemeriksaan kolonoskopi. "
           "Form ini bersifat edukatif dan tidak menggantikan konsultasi medis dengan dokter.")

# ------------------ DATA DASAR OPSIONAL ------------------
with st.expander("🧑‍⚕️ Data dasar (opsional)"):
    nama = st.text_input("Nama (opsional)", "")
    usia = st.number_input("Usia (tahun)", min_value=0, max_value=120, value=45, step=1)
    jenis_kelamin = st.selectbox("Jenis kelamin", ["Tidak diisi", "Laki-laki", "Perempuan"], index=0)

# ------------------ BAGIAN A ------------------
section_title("A. Gejala yang Perlu Diperhatikan")
q1 = st.checkbox("Apakah Anda sering buang air besar disertai darah merah segar (berulang dalam 3 bulan terakhir)?")
q2 = st.checkbox("Apakah pola buang air besar Anda berubah (lebih sering/lebih jarang atau feses menjadi lebih kecil) "
                 "dan berlangsung lebih dari 4 minggu?")
q3 = st.checkbox("Apakah Anda mengalami diare selama 4 minggu atau lebih tanpa membaik?")
q4 = st.checkbox("Apakah berat badan Anda turun tanpa sebab yang jelas dalam 3 bulan terakhir?")
q5 = st.checkbox("Apakah sering terasa nyeri atau kembung di perut, terutama sebelum buang air besar?")
q6 = st.checkbox("Apakah pernah diberitahu dokter bahwa Anda mengalami **anemia defisiensi besi** (darah rendah akibat kekurangan zat besi)?")
q7 = st.checkbox("Apakah hasil pemeriksaan tinja Anda menunjukkan adanya darah samar (tes feses positif)?")

# ------------------ BAGIAN B ------------------
section_title("B. Keluhan yang Memerlukan Pemeriksaan Segera")
q8  = st.checkbox("Apakah Anda mengalami buang air besar berdarah disertai nyeri perut dan demam?")
q9  = st.checkbox("Apakah Anda buang air besar hitam pekat dalam jumlah banyak, atau merasa sangat lemas/pusing seperti mau pingsan?")
q10 = st.checkbox("Apakah darah keluar banyak dari anus (menetes atau membasahi kloset)?")

st.caption("Bila Anda menjawab 'Ya' pada pertanyaan di atas, sebaiknya segera ke unit gawat darurat untuk pemeriksaan lebih lanjut.")

# ------------------ BAGIAN C ------------------
section_title("C. Riwayat dan Faktor Risiko")
q11 = st.checkbox("Apakah Anda berusia 45–75 tahun dan belum pernah menjalani skrining kanker usus besar sebelumnya?")
q12 = st.checkbox("Apakah ada anggota keluarga dekat (orang tua, saudara kandung, atau anak) yang pernah menderita "
                  "kanker usus besar atau polip di usus?")
q13 = st.checkbox("Apakah Anda pernah ditemukan memiliki polip (benjolan kecil) di usus besar pada pemeriksaan sebelumnya?")
q14 = st.checkbox("Apakah Anda memiliki penyakit radang usus kronis, seperti kolitis ulseratif atau penyakit Crohn?")
q15 = st.checkbox("Apakah hasil tes tinja Anda menunjukkan darah samar dan belum pernah diperiksa lebih lanjut dengan kolonoskopi?")

# ------------------ BAGIAN D ------------------
section_title("D. Lain-lain")
q16 = st.checkbox("Apakah Anda sering merasa buang air besar belum tuntas atau diameter feses menjadi lebih kecil dari biasanya?")
q17 = st.checkbox("Apakah terdapat lendir yang keluar bersama feses selama beberapa waktu?")

hr()

# ------------------ LOGIKA PENILAIAN ------------------
def evaluate():
    emergent_flags = [q8, q9, q10]
    urgent_flags   = [q1, q2, q3, q4, q5, q6, q7]
    screening_flags = [q11, q12, q13, q14, q15]
    soft_flags = [q16, q17]

    reasons = []

    if any(emergent_flags):
        reasons.append("Terdapat tanda bahaya akut seperti perdarahan banyak atau gejala kolitis berat.")
        return "EMERGENSI", "Segera periksa ke unit gawat darurat atau fasilitas kesehatan terdekat.", ("danger", "🚑"), reasons

    if any(urgent_flags):
        reasons.append("Ada gejala peringatan yang perlu evaluasi dokter dalam waktu dekat.")
        return "PERLU KONSULTASI SEGERA", "Disarankan berkonsultasi ke dokter penyakit dalam atau gastroenterologi dalam 1–2 minggu untuk pertimbangan kolonoskopi.", ("warn", "⏱️"), reasons

    if any(screening_flags):
        reasons.append("Terdapat faktor risiko atau usia yang sudah memenuhi kriteria skrining.")
        return "LAYAK UNTUK SKRINING", "Sebaiknya melakukan pemeriksaan skrining kanker usus besar. Kolonoskopi adalah pilihan utama.", ("info", "📅"), reasons

    if any(soft_flags) or (usia < 45):
        reasons.append("Keluhan ringan tanpa tanda bahaya, atau usia masih di bawah batas skrining rutin.")
        return "TINDAK LANJUT BIASA", "Pantau gejala dan lakukan pemeriksaan bila keluhan menetap atau bertambah berat.", ("muted", "ℹ️"), reasons

    reasons.append("Tidak ada keluhan atau faktor risiko yang memerlukan tindakan khusus saat ini.")
    return "AMAN SAAT INI", "Terus pantau kesehatan pencernaan Anda dan lakukan skrining saat usia ≥45 tahun.", ("ok", "✅"), reasons

verdict, advice, badge, reasons = evaluate()
kind, icon = badge

# ------------------ HASIL ------------------
st.subheader("Hasil Skrining")
pill(f"{icon} {verdict}", kind)
st.markdown(f"**Rekomendasi:** {advice}")

with st.expander("Penjelasan Singkat"):
    for r in reasons:
        st.markdown(f"- {r}")
    st.caption("Catatan: hasil ini bersifat edukatif. Keputusan akhir mengenai pemeriksaan kolonoskopi ditentukan oleh dokter.")

hr()
st.caption("© 2025 Skrining Mandiri Kolonoskopi – RS Kariadi Semarang | Edukasi Pasien")
