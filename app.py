# app.py — Skrining Terpadu EGD + Kolonoskopi
# Tema RS Kariadi • Tanpa Sidebar • 2 Ilustrasi • Export PDF Kopsurat
# © 2025 dr. Danu Kamajaya, Sp.PD – RSUP Dr. Kariadi Semarang

import streamlit as st
from datetime import datetime
from pathlib import Path
from io import BytesIO

# ==== PDF ====
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
/* Sembunyikan sidebar bila ada */
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

/* Header pusat: logo di atas judul */
.header-center { text-align: center; }
.header-center img { max-height: 88px; margin-bottom: 20px; }

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

/* Expander header */
.streamlit-expanderHeader {
  background:#f0fdfa; color:#007C80; font-weight:700; border:1px solid #b2dfdb;
  border-radius:10px;
}

/* Bingkai ilustrasi */
.illustration-wrap {
  border:1px solid #d6eceb; border-radius:12px; padding:6px; background:#ffffffcc;
  box-shadow:0 6px 18px rgba(0,0,0,.05);
  text-align:center;
}
.illustration-cap { color:#5b7580; font-size:.9rem; margin-top: .4rem; }

/* Responsif HP */
@media (max-width: 768px){
  .header-center img { max-height: 72px; }
  .title-text h1 { font-size: 1.9rem !important; }
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ------------------ ASSET PATHS ------------------
def pick_first_existing(paths):
    for p in paths:
        if Path(p).exists():
            return p
    return None

logo_path = pick_first_existing(["logo_kariadi.png", "./logo_kariadi.png", "/app/logo_kariadi.png"])
egd_img   = pick_first_existing(["ilustrasi_egd.png", "egd_illustration.png", "egd_image.png"])
colo_img  = pick_first_existing(["ilustrasi_colonoscopy.png", "colonoscopy.png"])

# ------------------ HEADER (logo tengah + judul) ------------------
with st.container():
    st.markdown("<div class='header-center'>", unsafe_allow_html=True)
    if logo_path:
        st.image(logo_path)
    st.markdown(
        """
        <div class="title-text">
          <h1 style='margin-top:0.25rem; margin-bottom:0.4rem;'>Apakah Saya Perlu Teropong Saluran Cerna?</h1>
          <p style='font-size:1.05rem; color:#333;'>
            Alat bantu sederhana untuk menilai apakah Anda mungkin memerlukan pemeriksaan teropong
            saluran cerna atas (<i>esophagogastroduodenoscopy</i>/EGD) maupun saluran cerna bawah
            (<i>kolonoskopi</i>). Berdasarkan panduan klinis; hasil bersifat edukasi dan tidak menggantikan
            diagnosis medis.
          </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------ ILUSTRASI BERDAMPINGAN ------------------
c_il_1, c_il_2 = st.columns([1,1], vertical_alignment="center")
with c_il_1:
    if egd_img:
        st.markdown("<div class='illustration-wrap'>", unsafe_allow_html=True)
        st.image(egd_img, use_container_width=True)
        st.markdown("<div class='illustration-cap'>Skema endoskopi saluran cerna atas (EGD)</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
with c_il_2:
    if colo_img:
        st.markdown("<div class='illustration-wrap'>", unsafe_allow_html=True)
        st.image(colo_img, use_container_width=True)
        st.markdown("<div class='illustration-cap'>Skema endoskopi saluran cerna bawah (Kolonoskopi)</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ------------------ DATA DASAR (opsional) ------------------
with st.expander("🧑‍⚕️ Data dasar (opsional)", expanded=False):
    name = st.text_input("Nama")
    age  = st.number_input("Usia (tahun)", min_value=0, max_value=120, value=45, step=1)
    sex  = st.selectbox("Jenis kelamin", ["Laki-laki", "Perempuan", "Lainnya"], index=0)
today = datetime.today().strftime("%d %b %Y")

# ------------------ PERTANYAAN: EGD (Atas) ------------------
ALARM_EGD = [
    "Saya **muntah darah** (hematemesis)",
    "BAB saya **hitam pekat seperti aspal** (melena)",
    "Saya makin **sulit menelan** (disfagia progresif)",
    "Saya **nyeri saat menelan** (odynofagia)",
    "Berat badan saya **turun banyak tanpa sebab jelas**",
    "Saya diberi tahu darah saya **kurang (anemia)** atau tampak pucat/lemas",
    "Saya **sering muntah berulang atau tidak bisa makan/minum**",
    "Perut bagian atas terasa **penuh / cepat kenyang / tersumbat** (curiga sumbatan lambung)",
]
RISK_EGD = [
    "Saya **baru mengalami keluhan lambung** setelah **usia ≥50 tahun**",
    "Ada **keluarga dekat** pernah terkena **kanker lambung**",
]
OTHER_EGD = [
    "Keluhan perut atas/nyeri ulu hati/panas di dada **>4–6 minggu** dan belum membaik",
    "**Nyeri ulu hati** tetap ada meski sudah minum PPI **4–8 minggu**",
    "Sering **asam/panas naik ke tenggorokan (refluks/GERD)** dan **tidak membaik** dengan obat",
    "Riwayat **tukak/ulkus** lambung atau duodenum dan keluhan berlanjut",
    "Riwayat **infeksi H. pylori** dan masih ada keluhan setelah pengobatan",
    "Sering memakai **NSAID/pengencer darah** disertai keluhan perut",
    "Dugaan **perdarahan samar** (tes darah feses positif) tanpa penyebab jelas",
    "Kontrol endoskopi pasca terapi (ulkus/varises/polipektomi) sesuai anjuran dokter",
]

with st.expander("🔼 Apakah Saya perlu teropong saluran cerna **atas (EGD)** ?", expanded=False):
    e1, e2, e3 = st.columns(3)
    egd_alarm_sel, egd_risk_sel, egd_other_sel = [], [], []

    with e1:
        st.subheader("🚨 Tanda Bahaya")
        st.caption("Jika ada salah satu, endoskopi biasanya **dianjurkan segera**.")
        for i, q in enumerate(ALARM_EGD):
            if st.checkbox(q, key=f"egd_alarm_{i}"):
                egd_alarm_sel.append(q)

    with e2:
        st.subheader("⚠️ Faktor Risiko")
        for i, q in enumerate(RISK_EGD):
            if st.checkbox(q, key=f"egd_risk_{i}"):
                egd_risk_sel.append(q)

    with e3:
        st.subheader("🩹 Indikasi Lain (Elektif)")
        for i, q in enumerate(OTHER_EGD):
            if st.checkbox(q, key=f"egd_other_{i}"):
                egd_other_sel.append(q)

# ------------------ PERTANYAAN: KOLONOSKOPI (Bawah) ------------------
ALARM_COLO = [
    "Saya **keluar darah segar dari dubur** sedang–berat / **menetes**",
    "Saya **anemia defisiensi besi** atau tampak pucat/lemas",
    "Berat badan saya **turun tanpa sebab jelas**",
    "Terjadi **perubahan pola BAB progresif** (>4–6 minggu) disertai darah",
    "Nyeri perut berat menetap, **diare berdarah/demam** (curiga kolitis/IBD berat)",
]
RISK_COLO = [
    "Usia **≥50 tahun** dengan keluhan saluran cerna bawah",
    "Ada **keluarga dekat** dengan **kanker kolorektal/polip adenoma**",
    "**FIT/FOBT positif**",
    "Riwayat **IBD** (kolitis ulseratif/Crohn) — evaluasi/monitoring",
    "Riwayat **polip/operasi CRC** — perlu **surveilans** berkala",
]
OTHER_COLO = [
    "**Perubahan kebiasaan BAB** >4–6 minggu (lebih sering/konstipasi/mengecil) tanpa alarm",
    "**Konstipasi kronik** tidak membaik meski sudah tata laksana awal",
    "**Diare kronik** >4 minggu",
    "Nyeri perut bawah berulang disertai perubahan BAB (evaluasi lanjut bila tidak membaik)",
    "Keluar **lendir/darah sedikit** berulang dari anus",
    "Skrining polip/CRC **elektif** sesuai usia/risiko",
]

with st.expander("🔽 Apakah Saya perlu teropong saluran cerna **bawah (Kolonoskopi)** ?", expanded=False):
    c1, c2, c3 = st.columns(3)
    colo_alarm_sel, colo_risk_sel, colo_other_sel = [], [], []

    with c1:
        st.subheader("🚨 Tanda Bahaya")
        st.caption("Jika ada salah satu, kolonoskopi biasanya **dianjurkan segera**.")
        for i, q in enumerate(ALARM_COLO):
            if st.checkbox(q, key=f"colo_alarm_{i}"):
                colo_alarm_sel.append(q)

    with c2:
        st.subheader("⚠️ Faktor Risiko")
        for i, q in enumerate(RISK_COLO):
            if st.checkbox(q, key=f"colo_risk_{i}"):
                colo_risk_sel.append(q)

    with c3:
        st.subheader("🩹 Indikasi Lain (Elektif)")
        for i, q in enumerate(OTHER_COLO):
            if st.checkbox(q, key=f"colo_other_{i}"):
                colo_other_sel.append(q)

st.markdown("---")

# ------------------ PENILAIAN HASIL ------------------
def verdict_and_advice(alarm_list, risk_list, other_list, organ_name):
    alarm = len(alarm_list) > 0
    risk  = len(risk_list)  > 0
    other = len(other_list) > 0

    if alarm:
        verdict = f"🔴 Anda **perlu {organ_name} segera**"
        badge = "badge badge-red"
        advice = "Segera periksa ke unit gawat darurat atau **konsultasikan ke dokter Anda.**"
    elif risk or other:
        verdict = f"🟢 Anda **dapat menjadwalkan {organ_name} (elektif)**"
        badge = "badge badge-green"
        advice = "Buat janji melalui poliklinik atau **konsultasikan ke dokter Anda** untuk rencana pemeriksaan."
    else:
        verdict = f"⚪ Saat ini **belum tampak kebutuhan mendesak untuk {organ_name}**"
        badge = "badge badge-gray"
        advice = ("Lanjutkan tata laksana konservatif dan pemantauan. Bila keluhan **tidak membaik 4–6 minggu** "
                  "atau muncul **tanda bahaya**, segera periksa ke dokter penyakit dalam.")
    reasons = alarm_list + risk_list + other_list
    return verdict, badge, advice, reasons

v_egd, b_egd, a_egd, r_egd   = verdict_and_advice(egd_alarm_sel, egd_risk_sel, egd_other_sel, "endoskopi saluran cerna atas (EGD)")
v_colo, b_colo, a_colo, r_colo = verdict_and_advice(colo_alarm_sel, colo_risk_sel, colo_other_sel, "kolonoskopi (saluran cerna bawah)")

st.subheader("📋 Hasil Skrining")
colA, colB = st.columns(2)

with colA:
    st.markdown(f'<div class="result-card"><span class="{b_egd}">{v_egd}</span><br/>{a_egd}</div>', unsafe_allow_html=True)
    with st.expander("Alasan (Atas/EGD)"):
        if r_egd: 
            for i, r in enumerate(r_egd, 1): st.write(f"{i}. {r}")
        else:
            st.write("Tidak ada pilihan yang tercentang.")

with colB:
    st.markdown(f'<div class="result-card"><span class="{b_colo}">{v_colo}</span><br/>{a_colo}</div>', unsafe_allow_html=True)
    with st.expander("Alasan (Bawah/Kolonoskopi)"):
        if r_colo: 
            for i, r in enumerate(r_colo, 1): st.write(f"{i}. {r}")
        else:
            st.write("Tidak ada pilihan yang tercentang.")

# ------------------ PDF EXPORT (Kopsurat RS Kariadi) ------------------
def build_pdf_letterhead(
    name: str, age: int, sex: str, today: str,
    v_egd: str, a_egd: str, r_egd: list,
    v_colo: str, a_colo: str, r_colo: list,
    logo_path: str | None
) -> bytes:
    """Bangun PDF surat hasil dengan kop RS Kariadi (logo + alamat) + 2 ringkasan hasil."""
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=32, rightMargin=32, topMargin=30, bottomMargin=28)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="H1", parent=styles["Title"], alignment=1, leading=20, spaceAfter=12))
    styles.add(ParagraphStyle(name="SmallGray", parent=styles["Normal"], textColor=colors.HexColor("#444"), fontSize=10))

    elems = []

    # Kop RS
    kop_tbl_data = []
    img_width = 110
    img = None
    if logo_path and Path(logo_path).exists():
        img = Image(logo_path, width=img_width, height=img_width*0.45)  # jaga proporsi
    kop_left  = img if img else ""
    kop_right = Paragraph(
        "<b>RUMAH SAKIT UMUM PUSAT DOKTER KARIADI</b><br/>"
        "Jalan Dr. Sutomo No 16 Semarang PO BOX 1104<br/>"
        "Telepon : (024) 8413993, 8413476, 8413764 &nbsp;&nbsp; "
        "<font color='#2e7d32'><b>Fax :</b> (024) 8318617</font><br/>"
        "Website : http://www.rskariadi.co.id",
        styles["Normal"]
    )
    kop_tbl = Table([[kop_left, kop_right]], colWidths=[img_width+8, 450], hAlign="LEFT")
    kop_tbl.setStyle(TableStyle([("VALIGN",(0,0),(1,0),"MIDDLE")]))
    elems += [kop_tbl, Spacer(1,10), Table([[""]], colWidths=[530], style=[("LINEBELOW",(0,0),(0,0),1,colors.HexColor("#9dd8d3"))]), Spacer(1,6)]

    # Judul
    elems.append(Paragraph("HASIL SKRINING ENDOSKOPI SALURAN CERNA", styles["H1"]))
    elems.append(Paragraph("(EGD & Kolonoskopi)", styles["SmallGray"]))
    elems.append(Spacer(1,6))

    # Identitas
    ident = [
        Paragraph(f"<b>Tanggal:</b> {today}", styles["Normal"]),
        Paragraph(f"<b>Nama:</b> {name if name else '-'}", styles["Normal"]),
        Paragraph(f"<b>Usia:</b> {age} tahun", styles["Normal"]),
        Paragraph(f"<b>Jenis kelamin:</b> {sex}", styles["Normal"]),
    ]
    for p in ident: elems.append(p)
    elems.append(Spacer(1,10))

    # Seksi 1: EGD
    elems.append(Paragraph("<b>1) Saluran Cerna Atas (EGD)</b>", styles["Normal"]))
    elems.append(Spacer(1,2))
    elems.append(Paragraph(f"<b>Kesimpulan:</b> {v_egd}", styles["Normal"]))
    elems.append(Paragraph(a_egd.replace("\n","<br/>"), styles["Normal"]))
    if r_egd:
        elems.append(Spacer(1,4))
        elems.append(Paragraph("<b>Faktor yang terdeteksi:</b>", styles["Normal"]))
        for r in r_egd: elems.append(Paragraph(f"- {r}", styles["Normal"]))
    elems.append(Spacer(1,10))

    # Seksi 2: Kolonoskopi
    elems.append(Paragraph("<b>2) Saluran Cerna Bawah (Kolonoskopi)</b>", styles["Normal"]))
    elems.append(Spacer(1,2))
    elems.append(Paragraph(f"<b>Kesimpulan:</b> {v_colo}", styles["Normal"]))
    elems.append(Paragraph(a_colo.replace("\n","<br/>"), styles["Normal"]))
    if r_colo:
        elems.append(Spacer(1,4))
        elems.append(Paragraph("<b>Faktor yang terdeteksi:</b>", styles["Normal"]))
        for r in r_colo: elems.append(Paragraph(f"- {r}", styles["Normal"]))
    elems.append(Spacer(1,12))

    # Catatan
    elems.append(Paragraph(
        "Hasil ini bersifat edukatif dan tidak menggantikan penilaian dokter. "
        "Jika keluhan berat, mendadak, atau menetap, segera konsultasikan ke dokter penyakit dalam.",
        styles["Italic"]
    ))

    doc.build(elems)
    return buf.getvalue()

pdf_bytes = build_pdf_letterhead(
    name or "", int(age), sex, today,
    v_egd, a_egd, r_egd,
    v_colo, a_colo, r_colo,
    logo_path
)

st.download_button(
    label="⬇️ Unduh Surat Hasil (PDF)",
    data=pdf_bytes,
    file_name=f"Hasil_Skrining_Saluran_Cerna_{today.replace(' ','_')}.pdf",
    mime="application/pdf",
)

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("🔒 **Privasi:** Aplikasi ini tidak menyimpan data pribadi Anda. Semua isian hanya tampil di perangkat Anda.",
            help="Tidak ada penyimpanan server.")
st.caption("© 2025 | Aplikasi edukasi oleh **dr. Danu Kamajaya, Sp.PD** – RSUP Dr. Kariadi Semarang – Versi Awam")
