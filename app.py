# app.py — Skrining Terpadu Saluran Cerna Atas & Bawah
# © 2025 dr. Danu Kamajaya, Sp.PD – RSUP Dr. Kariadi Semarang

import streamlit as st
from datetime import datetime
from pathlib import Path
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Apakah Saya Perlu Teropong Saluran Cerna?",
    page_icon="🩺",
    layout="wide",
)

# ------------------ THEME / CSS ------------------
CUSTOM_CSS = """
<style>
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

.stApp {
  background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 55%, #e6fffb 100%);
  color: #1c1c1c;
}
.block-container { padding-top: 18px; padding-bottom: 2rem; }

h1, h2, h3 { color:#007C80; }
h1 { font-weight:800; }
h2, h3 { font-weight:700; }

/* Header tengah */
.header-center { text-align: center; }
.header-center img { max-height: 70px; margin-bottom: 6px; }

/* Ilustrasi */
.illustration-wrap {
  border:none;
  border-radius:12px;
  padding:0;
  background:none;
  text-align:center;
}
.illustration-wrap img { max-width:85%; border-radius:10px; box-shadow:0 3px 10px rgba(0,0,0,.05); }
.illustration-cap { color:#5b7580; font-size:.9rem; margin-top: .4rem; }

/* Expander custom — tanpa ikon panah */
.expander-custom {
  background:#f0fdfa;
  border:1px solid #b2dfdb;
  border-radius:10px;
  padding:1rem;
  margin-bottom:1rem;
  box-shadow:0 4px 10px rgba(0,0,0,.05);
}
.expander-custom h2 {
  color:#007C80;
  font-weight:700;
  font-size:1.2rem;
  margin-bottom:1rem;
}

/* Kartu hasil */
.result-card {
  border: 2px solid #00B3AD22; border-radius: 14px; padding: 1rem 1.2rem;
  background: #ffffffcc; box-shadow: 0 6px 18px rgba(0,0,0,.06);
  margin-bottom: 1rem;
}
.badge { display:inline-block; padding:.35rem .65rem; border-radius:999px; font-weight:700; }
.badge-red  { background:#ffebee; color:#c62828; border:1px solid #ffcdd2; }
.badge-green{ background:#e8f5e9; color:#1b5e20; border:1px solid #c8e6c9; }
.badge-gray { background:#eceff1; color:#37474f; border:1px solid #cfd8dc; }

.footer-note { color:#004d40; font-size:.9rem; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ------------------ LOAD ASSETS ------------------
def pick_first_existing(paths):
    for p in paths:
        if Path(p).exists():
            return p
    return None

logo_path = pick_first_existing(["logo_kariadi.png", "./logo_kariadi.png"])
egd_img   = pick_first_existing(["ilustrasi_egd.png", "egd_image.png"])
colo_img  = pick_first_existing(["ilustrasi_colonoscopy.png", "colonoscopy.png"])

# ------------------ HEADER ------------------
with st.container():
    st.markdown("<div class='header-center'>", unsafe_allow_html=True)
    if logo_path:
        st.image(logo_path)
    st.markdown("""
        <h1>Apakah Saya Perlu Teropong Saluran Cerna?</h1>
        <p style='font-size:1.05rem; color:#333;'>
        Alat bantu sederhana untuk membantu Anda menilai apakah perlu pemeriksaan
        teropong saluran cerna atas (<i>endoskopi/EGD</i>) maupun bawah (<i>kolonoskopi</i>).
        Berdasarkan panduan klinis terbaru. Hasil bersifat edukatif, bukan diagnosis medis.
        </p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------ ILUSTRASI ------------------
c1, c2 = st.columns(2)
with c1:
    if egd_img:
        st.markdown("<div class='illustration-wrap'>", unsafe_allow_html=True)
        st.image(egd_img, use_container_width=True)
        st.markdown("<div class='illustration-cap'>Pemeriksaan endoskopi saluran cerna atas (EGD)</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
with c2:
    if colo_img:
        st.markdown("<div class='illustration-wrap'>", unsafe_allow_html=True)
        st.image(colo_img, use_container_width=True)
        st.markdown("<div class='illustration-cap'>Pemeriksaan endoskopi saluran cerna bawah (kolonoskopi)</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ------------------ DATA DASAR ------------------
with st.expander("🧑‍⚕️ Data Diri (opsional)", expanded=False):
    name = st.text_input("Nama")
    age = st.number_input("Usia (tahun)", min_value=0, max_value=120, value=40)
    sex = st.selectbox("Jenis kelamin", ["Laki-laki", "Perempuan", "Lainnya"], index=0)
today = datetime.today().strftime("%d %b %Y")

# ------------------ PERTANYAAN EGD ------------------
st.markdown("<div class='expander-custom'>", unsafe_allow_html=True)
st.markdown("<h2>🩺 Apakah Saya Perlu Teropong Saluran Cerna Atas (EGD)?</h2>", unsafe_allow_html=True)

egd_alarm = [
    "Saya pernah muntah darah.",
    "BAB saya berwarna hitam pekat seperti aspal.",
    "Saya merasa makin sulit atau nyeri saat menelan.",
    "Berat badan saya turun tanpa sebab jelas.",
    "Saya sering lemas/pucat atau diberi tahu darah saya kurang.",
]
egd_risk = [
    "Saya berusia di atas 50 tahun dan baru mengalami keluhan lambung.",
    "Ada anggota keluarga yang pernah menderita kanker lambung.",
]
egd_other = [
    "Keluhan perut atas/nyeri ulu hati yang menetap lebih dari 4 minggu.",
    "Nyeri ulu hati tidak membaik meski sudah minum obat lambung.",
    "Sering merasa panas di dada atau asam naik ke tenggorokan.",
]

egd_selected = []
for cat, questions in [("🚨 Tanda Bahaya", egd_alarm), ("⚠️ Faktor Risiko", egd_risk), ("🩹 Keluhan Umum", egd_other)]:
    st.subheader(cat)
    for q in questions:
        if st.checkbox(q, key=f"egd_{q}"):
            egd_selected.append(q)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------ PERTANYAAN KOLO ------------------
st.markdown("<div class='expander-custom'>", unsafe_allow_html=True)
st.markdown("<h2>💩 Apakah Saya Perlu Teropong Saluran Cerna Bawah (Kolonoskopi)?</h2>", unsafe_allow_html=True)

colo_alarm = [
    "Saya buang air besar berdarah atau darah keluar dari anus.",
    "Berat badan saya turun tanpa sebab yang jelas.",
    "Saya tampak pucat atau diberi tahu mengalami anemia.",
]
colo_risk = [
    "Saya berusia di atas 50 tahun.",
    "Ada keluarga dekat yang pernah menderita kanker usus besar.",
]
colo_other = [
    "BAB saya berubah: lebih sering, lebih jarang, atau bentuknya mengecil.",
    "Saya mengalami sembelit atau diare lama lebih dari 3 minggu.",
    "BAB saya disertai lendir atau darah sedikit berulang.",
]

colo_selected = []
for cat, questions in [("🚨 Tanda Bahaya", colo_alarm), ("⚠️ Faktor Risiko", colo_risk), ("🩹 Keluhan Umum", colo_other)]:
    st.subheader(cat)
    for q in questions:
        if st.checkbox(q, key=f"colo_{q}"):
            colo_selected.append(q)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------ PENILAIAN ------------------
def verdict(selected, organ):
    if any("darah" in s or "anemia" in s or "turun" in s for s in selected):
        return f"🔴 Anda **perlu {organ} segera**", "badge badge-red", "Segera periksa ke unit gawat darurat atau konsultasikan ke dokter."
    elif selected:
        return f"🟢 Anda **dapat menjadwalkan {organ} (elektif)**", "badge badge-green", "Konsultasikan ke dokter untuk perencanaan pemeriksaan lebih lanjut."
    else:
        return f"⚪ Saat ini belum tampak kebutuhan mendesak untuk {organ}.", "badge badge-gray", "Lanjutkan pemantauan, segera periksa bila keluhan berlanjut."

v_egd, b_egd, a_egd = verdict(egd_selected, "endoskopi saluran cerna atas (EGD)")
v_colo, b_colo, a_colo = verdict(colo_selected, "kolonoskopi (saluran cerna bawah)")

# ------------------ HASIL ------------------
st.subheader("📋 Hasil Skrining")
cA, cB = st.columns(2)
with cA:
    st.markdown(f"<div class='result-card'><span class='{b_egd}'>{v_egd}</span><br/>{a_egd}</div>", unsafe_allow_html=True)
with cB:
    st.markdown(f"<div class='result-card'><span class='{b_colo}'>{v_colo}</span><br/>{a_colo}</div>", unsafe_allow_html=True)

# ------------------ PDF EXPORT ------------------
def build_pdf(name, age, sex, today, v1, a1, v2, a2, logo):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=28, bottomMargin=28)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Center", alignment=1))
    styles.add(ParagraphStyle(name="SmallGray", textColor=colors.gray, fontSize=10))

    elems = []

    # Kop surat (logo kiri + teks tengah)
    img = Image(logo, width=90, height=45) if logo and Path(logo).exists() else ""
    kop_tbl = Table([[img, Paragraph(
        "<b>RUMAH SAKIT UMUM PUSAT DOKTER KARIADI</b><br/>"
        "Jalan Dr. Sutomo No 16 Semarang PO BOX 1104<br/>"
        "Telepon : (024) 8413993, 8413476, 8413764 &nbsp;&nbsp; <b>Fax :</b> (024) 8318617<br/>"
        "Website : http://www.rskariadi.co.id", styles["Center"]
    )]], colWidths=[100, 400])
    kop_tbl.setStyle(TableStyle([("VALIGN",(0,0),(1,0),"MIDDLE")]))
    elems += [kop_tbl, Spacer(1,10), Table([[""]], colWidths=[530], style=[("LINEBELOW",(0,0),(0,0),1,colors.HexColor("#9dd8d3"))]), Spacer(1,6)]

    # Isi
    elems.append(Paragraph("<b>HASIL SKRINING ENDOSKOPI SALURAN CERNA</b>", styles["Center"]))
    elems.append(Spacer(1,10))
    elems.append(Paragraph(f"<b>Tanggal:</b> {today}", styles["Normal"]))
    elems.append(Paragraph(f"<b>Nama:</b> {name if name else '-'}", styles["Normal"]))
    elems.append(Paragraph(f"<b>Usia:</b> {age} tahun", styles["Normal"]))
    elems.append(Paragraph(f"<b>Jenis kelamin:</b> {sex}", styles["Normal"]))
    elems.append(Spacer(1,10))

    elems.append(Paragraph("<b>1️⃣ Saluran Cerna Atas (EGD)</b>", styles["Normal"]))
    elems.append(Paragraph(v1, styles["Normal"]))
    elems.append(Paragraph(a1, styles["Normal"]))
    elems.append(Spacer(1,8))
    elems.append(Paragraph("<b>2️⃣ Saluran Cerna Bawah (Kolonoskopi)</b>", styles["Normal"]))
    elems.append(Paragraph(v2, styles["Normal"]))
    elems.append(Paragraph(a2, styles["Normal"]))
    elems.append(Spacer(1,12))

    elems.append(Paragraph(
        "Hasil ini bersifat edukatif dan tidak menggantikan penilaian dokter. "
        "Jika keluhan berat, mendadak, atau menetap, segera konsultasikan ke dokter penyakit dalam.",
        styles["Italic"]
    ))
    doc.build(elems)
    return buffer.getvalue()

pdf_bytes = build_pdf(name or "", int(age), sex, today, v_egd, a_egd, v_colo, a_colo, logo_path)

st.download_button(
    label="⬇️ Unduh Surat Hasil (PDF)",
    data=pdf_bytes,
    file_name=f"Hasil_Skrining_Saluran_Cerna_{today.replace(' ','_')}.pdf",
    mime="application/pdf",
)

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("🔒 **Privasi:** Aplikasi ini tidak menyimpan data pribadi Anda. Semua isian hanya tampil di perangkat Anda.")
st.caption("© 2025 | Aplikasi edukasi oleh **dr. Danu Kamajaya, Sp.PD** – RSUP Dr. Kariadi Semarang – Versi Awam")
