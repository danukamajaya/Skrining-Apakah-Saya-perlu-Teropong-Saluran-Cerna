# app.py
# Skrining Mandiri Kolonoskopi – versi 1.1 (Bahasa Pasien, 2025)
# © dr. Danu Kamajaya, Sp.PD – RSUP Dr. Kariadi Semarang
# Jalankan dengan: streamlit run app.py

import streamlit as st
from datetime import datetime
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Skrining Mandiri Kolonoskopi", page_icon="🧾", layout="centered")

# ================== THEME & STYLE ==================
CUSTOM_CSS = """
<style>
/* App background: gradasi putih-kehijauan (lembut, bersih) */
[data-testid="stAppViewContainer"] {
  background:
    radial-gradient(1100px 600px at 90% 0%, rgba(209, 250, 229, 0.6), transparent 60%),
    linear-gradient(180deg, #ffffff 0%, #f0fdf4 100%);
}

/* Hilangkan footer & menu default agar bersih */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Lebar konten lebih nyaman dibaca */
.block-container {max-width: 880px; padding-top: 1.5rem;}

/* Kartu konten utama (glass) */
.app-card {
  background: rgba(255,255,255,0.75);
  border: 1px solid rgba(16, 185, 129, 0.12);
  box-shadow:
    0 10px 15px -3px rgba(16, 185, 129, 0.1),
    0 4px 6px -2px rgba(16, 185, 129, 0.06);
  backdrop-filter: saturate(120%) blur(6px);
  border-radius: 1.25rem;
  padding: 1.25rem 1.25rem 1rem 1.25rem;
}

/* Header title */
h1, h2, h3 { letter-spacing: 0.2px; }
h1 { font-weight: 700; }
h3 { margin-top: 0.75rem; }

/* Expander halus */
.streamlit-expanderHeader, .st-expanderHeader {
  font-weight: 600;
}
.st-expander {
  border: 1px solid rgba(16, 185, 129, 0.20);
  border-radius: 1rem !important;
  background: rgba(255,255,255,0.6);
}

/* Checkbox label line-height agar rapi */
.stCheckbox > label, label[data-baseweb="checkbox"] {
  line-height: 1.35rem !important;
}

/* Pill style (fallback bila HTML pill dipakai) */
.pill { padding: 6px 10px; border-radius: 999px; font-size: 0.95rem; font-weight: 600; display: inline-block; }

/* Header bar: tempat logo kanan atas */
.header-bar {
  display: flex; align-items: center; justify-content: space-between;
  gap: 1rem; margin-bottom: 0.25rem;
}
.header-right img {
  max-height: 64px; height: auto; width: auto;
  object-fit: contain;
  filter: drop-shadow(0 1px 0 rgba(0,0,0,0.04));
}

/* Rekomendasi section spacing */
.reco { margin-top: 0.5rem; margin-bottom: 0.25rem; }

/* Divider tipis berwarna hijau muda */
.hr-soft { height: 1px; background: linear-gradient(90deg, transparent, rgba(16,185,129,0.35), transparent); border: 0; margin: 1rem 0; }

.caption-foot { color: #065f46; font-size: 0.8rem; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ================== HELPERS ==================
def pill(text, kind="info"):
    colors = {
        "danger": ("#ffffff", "#dc2626"),
        "warn":   ("#111111", "#fbbf24"),
        "ok":     ("#ffffff", "#16a34a"),
        "info":   ("#ffffff", "#2563eb"),
        "muted":  ("#111111", "#9ca3af"),
    }
    fg, bg = colors.get(kind, colors["info"])
    st.markdown(
        f"<span class='pill' style='background:{bg}; color:{fg}'>{text}</span>",
        unsafe_allow_html=True
    )

def section_title(title):
    st.markdown(f"### {title}")

def hr():
    st.markdown("<div class='hr-soft'></div>", unsafe_allow_html=True)

# ================== HEADER ==================
# Logo: coba muat dari file lokal; jika gagal, bisa upload manual
def load_logo_from_file(path="logo_kariadi.png"):
    try:
        img = Image.open(path)
        return img
    except Exception:
        return None

logo_img = load_logo_from_file()

if logo_img is not None:
    st.image(logo_img, width=96)   # ← ganti dari use_container_width
else:
    up = st.file_uploader("Unggah logo RS Kariadi (PNG)", type=["png"], label_visibility="collapsed")
    if up is not None:
        logo_img = Image.open(up)
        st.image(logo_img, width=96)

col_header = st.container()
with col_header:
    st.markdown("<div class='header-bar'>", unsafe_allow_html=True)
    st.markdown("<div class='header-left'></div>", unsafe_allow_html=True)
    # Judul + subjudul di-render biasa agar tetap selectable
    st.title("🧾 Skrining Mandiri Kolonoskopi")
    st.caption(
        "Panduan sederhana untuk membantu mengenali apakah Anda sebaiknya menjalani pemeriksaan kolonoskopi. "
        "Form ini bersifat edukatif dan tidak menggantikan konsultasi medis dengan dokter."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Logo kanan atas
    right = st.container()
    with right:
        cols = st.columns([1, 0.35])
        with cols[0]:
            pass
        with cols[1]:
            st.markdown("<div class='header-right'>", unsafe_allow_html=True)
            if logo_img is not None:
                st.image(logo_img, use_container_width=False)
            else:
                # Uploader jika file belum ada
                up = st.file_uploader("Unggah logo RS Kariadi (PNG)", type=["png"], label_visibility="collapsed")
                if up is not None:
                    logo_img = Image.open(up)
                    st.image(logo_img, use_container_width=False)
            st.markdown("</div>", unsafe_allow_html=True)

# ================== KARTU KONTEN ==================
with st.container():
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)

    # -------- DATA DASAR OPSIONAL --------
    with st.expander("🧑‍⚕️ Data dasar (opsional)", expanded=False):
        nama = st.text_input("Nama (opsional)", "")
        usia = st.number_input("Usia (tahun)", min_value=0, max_value=120, value=45, step=1)
        jenis_kelamin = st.selectbox("Jenis kelamin", ["Tidak diisi", "Laki-laki", "Perempuan"], index=0)

    hr()

    # -------- BAGIAN A --------
    section_title("A. Gejala yang Perlu Diperhatikan")
    q1 = st.checkbox("Sering buang air besar disertai darah merah segar (berulang dalam 3 bulan terakhir)")
    q2 = st.checkbox("Perubahan pola buang air besar (lebih sering/lebih jarang atau feses mengecil) > 4 minggu")
    q3 = st.checkbox("Diare ≥ 4 minggu tanpa perbaikan")
    q4 = st.checkbox("Penurunan berat badan tanpa sebab jelas dalam 3 bulan terakhir")
    q5 = st.checkbox("Nyeri/kembung perut, terutama sebelum buang air besar")
    q6 = st.checkbox("Pernah didiagnosis **anemia defisiensi besi**")
    q7 = st.checkbox("Tes feses pernah menunjukkan darah samar (FOBT/FIT positif)")

    # -------- BAGIAN B --------
    section_title("B. Keluhan yang Memerlukan Pemeriksaan Segera")
    q8  = st.checkbox("BAB berdarah disertai nyeri perut dan demam")
    q9  = st.checkbox("BAB hitam pekat banyak, atau sangat lemas/pusing seperti mau pingsan")
    q10 = st.checkbox("Perdarahan rektal banyak (menetes/membasahi kloset)")
    st.caption("Jika menjawab 'Ya' pada salah satu, segera ke unit gawat darurat untuk pemeriksaan lebih lanjut.")

    # -------- BAGIAN C --------
    section_title("C. Riwayat dan Faktor Risiko")
    q11 = st.checkbox("Usia 45–75 tahun dan belum pernah skrining kanker usus besar")
    q12 = st.checkbox("Keluarga dekat dengan riwayat kanker usus besar atau polip")
    q13 = st.checkbox("Pernah ditemukan polip usus besar sebelumnya")
    q14 = st.checkbox("Memiliki radang usus kronis (kolitis ulseratif/Crohn)")
    q15 = st.checkbox("Tes tinja darah samar positif dan belum dievaluasi kolonoskopi")

    # -------- BAGIAN D --------
    section_title("D. Lain-lain")
    q16 = st.checkbox("Sering merasa BAB belum tuntas atau diameter feses mengecil")
    q17 = st.checkbox("Ada lendir keluar bersama feses selama beberapa waktu")

    hr()

    # -------- LOGIKA PENILAIAN --------
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
            return "PERLU KONSULTASI SEGERA", "Konsultasi ke Sp.PD/Gastro dalam 1–2 minggu untuk pertimbangan kolonoskopi.", ("warn", "⏱️"), reasons

        if any(screening_flags):
            reasons.append("Terdapat faktor risiko atau usia yang memenuhi kriteria skrining.")
            return "LAYAK UNTUK SKRINING", "Sebaiknya melakukan skrining kanker usus besar. Kolonoskopi adalah pilihan utama.", ("info", "📅"), reasons

        # Catatan: usia default 45; jika user belum membuka Data Dasar, gunakan 45 sebagai default aman
        usia_val = locals().get("usia", 45)
        if any(soft_flags) or (usia_val < 45):
            reasons.append("Keluhan ringan tanpa tanda bahaya, atau usia masih di bawah batas skrining rutin.")
            return "TINDAK LANJUT BIASA", "Pantau gejala dan periksa bila keluhan menetap/bertambah berat.", ("muted", "ℹ️"), reasons

        reasons.append("Tidak ada keluhan atau faktor risiko yang memerlukan tindakan khusus saat ini.")
        return "AMAN SAAT INI", "Terus pantau kesehatan pencernaan Anda dan lakukan skrining saat usia ≥45 tahun.", ("ok", "✅"), reasons

    verdict, advice, badge, reasons = evaluate()
    kind, icon = badge

    # -------- HASIL --------
    st.subheader("Hasil Skrining")
    pill(f"{icon} {verdict}", kind)
    st.markdown(f"<div class='reco'><strong>Rekomendasi:</strong> {advice}</div>", unsafe_allow_html=True)

    with st.expander("Penjelasan Singkat"):
        for r in reasons:
            st.markdown(f"- {r}")
        st.caption("Catatan: hasil ini bersifat edukatif. Keputusan akhir mengenai kolonoskopi ditentukan oleh dokter.")

    st.markdown("</div>", unsafe_allow_html=True)  # end .app-card

# ================== FOOTER ==================
hr()
st.caption("© 2025 Skrining Mandiri Kolonoskopi – RSUP Dr. Kariadi Semarang | Edukasi Pasien")
