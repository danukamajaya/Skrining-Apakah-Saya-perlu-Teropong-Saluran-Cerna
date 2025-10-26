
# app.py
# Skrining Mandiri Kolonoskopi – versi 1.0 (ID)
# Cara menjalankan: streamlit run app.py

import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Skrining Mandiri Kolonoskopi", page_icon="🧾", layout="centered")

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
        f"<span style='padding: 6px 10px; border-radius: 999px; background:{bg}; color:{fg}; font-size:0.9rem'>{text}</span>",
        unsafe_allow_html=True
    )

def section_title(title, subtitle=None):
    st.markdown(f"### {title}")
    if subtitle:
        st.caption(subtitle)

def hr():
    st.markdown("---")

st.title("🧾 Skrining Mandiri Kolonoskopi")
st.caption("Alat bantu awal untuk mengenali indikasi kolonoskopi. Bukan pengganti konsultasi medis langsung.")

with st.expander("🧑‍⚕️ Data dasar (opsional)"):
    nama = st.text_input("Nama", "")
    usia = st.number_input("Usia (tahun)", min_value=0, max_value=120, value=45, step=1)
    jenis_kelamin = st.selectbox("Jenis kelamin", ["Tidak diisi", "Laki-laki", "Perempuan"], index=0)

section_title("A. Gejala 'Red Flag' saat ini")
q1 = st.checkbox("BAB berdarah merah segar (hematokezia) berulang dalam 3 bulan terakhir")
q2 = st.checkbox("Perubahan pola BAB baru (lebih sering/lebih jarang/konsistensi berubah) yang menetap ≥ 4 minggu")
q3 = st.checkbox("Diare kronik ≥ 4 minggu yang tidak membaik")
q4 = st.checkbox("Berat badan turun tanpa direncanakan (3 bulan terakhir)")
q5 = st.checkbox("Nyeri perut menetap/kolik berulang disertai kembung/tenesmus")
q6 = st.checkbox("Diberitahu dokter/hasil lab ada **anemia defisiensi besi** (IDA)")
q7 = st.checkbox("Tes feses **FIT/FOBT positif** (belum ditindaklanjuti kolonoskopi)")

section_title("B. Gejala yang memerlukan penilaian cepat")
q8  = st.checkbox("Diare berdarah + nyeri perut + demam")
q9  = st.checkbox("BAB hitam pekat (melena) banyak ATAU pusing/lemas seperti mau pingsan")
q10 = st.checkbox("Perdarahan rektal banyak (menetes/membasahi kloset)")

section_title("C. Riwayat & faktor risiko")
q11 = st.checkbox("Usia 45–75 tahun dan **belum pernah** skrining kanker kolorektal sesuai interval yang dianjurkan")
q12 = st.checkbox("Ada **riwayat keluarga** kanker/adenoma kolorektal pada keluarga inti (≤60 tahun) atau ≥2 keluarga inti usia berapa pun")
q13 = st.checkbox("Riwayat **polip adenoma** sebelumnya (sedang/harus kontrol surveilans)")
q14 = st.checkbox("Riwayat **IBD** (kolitis ulseratif/Crohn) > 8–10 tahun")
q15 = st.checkbox("Pernah/baru **FIT positif** dan **belum** ditindaklanjuti kolonoskopi")

section_title("D. Lain-lain")
q16 = st.checkbox("Nyeri saat BAB, rasa tidak tuntas (tenesmus), atau diameter feses mengecil yang baru muncul")
q17 = st.checkbox("Mukus/lendir pada feses yang menetap")

hr()

def evaluate():
    emergent_flags = [q8, q9, q10]
    urgent_flags   = [q1, q2, q3, q4, q5, q6, q7]
    screening_flags = [q11, q12, q13, q14, q15]
    soft_flags = [q16, q17]

    reasons = []

    if any(emergent_flags):
        reasons.append("Tanda bahaya akut: perdarahan aktif/kolitis berat/instabilitas (Q8–Q10).")
        return "EMERGENSI", "Segera periksa ke unit gawat darurat atau konsultasikan ke dokter Anda.", ("danger", "🚑"), reasons
    if any(urgent_flags):
        reasons.append("Gejala/temuan red flag (Q1–Q7).")
        return "RUJUKAN CEPAT (≤ 2 minggu)", "Jadwalkan konsultasi penyakit dalam/gastroenterologi untuk penilaian dan kemungkinan kolonoskopi.", ("warn", "⏱️"), reasons
    if any(screening_flags):
        reasons.append("Indikasi skrining/surveilans (Q11–Q15).")
        return "LAYAK SKRINING / SURVEILANS", "Diskusikan pilihan skrining; kolonoskopi adalah opsi utama.", ("info", "📅"), reasons
    if any(soft_flags) or (usia < 45):
        reasons.append("Keluhan non-spesifik tanpa red flag atau usia <45 tahun.")
        return "TINDAK LANJUT NON-URGENT", "Pertimbangkan evaluasi rawat jalan.", ("muted", "ℹ️"), reasons
    reasons.append("Tidak ada jawaban yang memicu indikasi kuat saat ini.")
    return "AMAN SAAT INI", "Terus pantau gejala.", ("ok", "✅"), reasons

verdict, advice, badge, reasons = evaluate()
kind, icon = badge

st.subheader("Hasil Skrining")
pill(f"{icon} {verdict}", kind)
st.markdown(f"**Rekomendasi:** {advice}")

with st.expander("Alasan & konteks medis (ringkas)"):
    for i, r in enumerate(reasons, start=1):
        st.markdown(f"- {r}")
    st.caption("Hasil skrining ini bersifat orientatif. Keputusan akhir tindakan medis ditetapkan oleh dokter.")

hr()
st.caption("Disclaimer: Form ini bersifat edukatif, bukan pengganti konsultasi medis.")
