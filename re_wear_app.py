import streamlit as st
import pandas as pd
import numpy as np
import time

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="RE-WEAR: Solusi Pakaian Berkelanjutan",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Dummy untuk Simulasi ---
if 'items_for_sale' not in st.session_state:
    st.session_state.items_for_sale = [
        {"id": 1, "nama": "Jaket Denim Vintage", "deskripsi": "Kondisi 90%. Ukuran L. Cocok untuk musim hujan.", "harga": 150000, "tipe": "Jual", "dampak": 2.5, "disukai": 12},
        {"id": 2, "nama": "Kemeja Flanel Merah", "deskripsi": "Gratis, cocok untuk didonasikan ke wilayah tertentu.", "harga": 0, "tipe": "Donasi", "dampak": 1.5, "disukai": 20},
        {"id": 3, "nama": "Sepatu Kanvas Putih", "deskripsi": "Perlu dicuci, tapi masih nyaman dipakai. Ukuran 40.", "harga": 80000, "tipe": "Jual", "dampak": 3.0, "disukai": 5},
    ]

# Data Dampak Global (simulasi)
global_impact = {
    "limbah_dihemat_kg": 5200,
    "pakaian_diselamatkan": 12500,
    "air_dihemat_liter": 6000000,
    "karbon_dikurangi_kg": 15000
}

# --- Fungsi Utility ---
def format_rupiah(angka):
    """Format angka menjadi string Rupiah."""
    return f"Rp {angka:,.0f}".replace(",", ".")

def add_new_item(nama, deskripsi, harga, tipe):
    """Menambahkan item baru ke daftar (simulasi)."""
    new_id = max(item['id'] for item in st.session_state.items_for_sale) + 1
    dampak = np.random.uniform(1.0, 5.0) # Dampak random
    st.session_state.items_for_sale.append({
        "id": new_id,
        "nama": nama,
        "deskripsi": deskripsi,
        "harga": harga,
        "tipe": tipe,
        "dampak": round(dampak, 2),
        "disukai": 0
    })
    st.success(f"Item '{nama}' berhasil ditambahkan ke daftar!")
    time.sleep(1)
    st.rerun()

# --- HEADER APLIKASI ---
st.title("♻️ RE-WEAR: Platform Fashion Berkelanjutan")
st.markdown("""
Aplikasi yang menghubungkan penjual, pembeli, dan pendonor baju bekas layak pakai.
""")
st.divider()

# --- SIDEBAR NAVIGASI ---
st.sidebar.title("MENU APLIKASI")
menu_selection = st.sidebar.radio(
    "Pilih Fitur Utama",
    ["Dashboard Dampak (Bab IV)", "Marketplace & Donasi (Bab III)", "AI Recommendation", "Gamifikasi & Edukasi"]
)

# --- BAGIAN 1: Dashboard Dampak (Bab IV) ---
if menu_selection == "Dashboard Dampak (Bab IV)":
    st.header("🤝 Dashboard Analytics & Kolaborasi")
    st.subheader("Mengukur Dampak Keberlanjutan RE-WEAR")
    st.markdown("""
    Bab ini menyajikan visualisasi kolaborasi multidisiplin, dengan fokus pada metrik dampak lingkungan dan sosial yang dihasilkan platform.
    """)

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Limbah Tekstil Dihemat", value=f"{global_impact['limbah_dihemat_kg']:,} kg", delta="↑ 15% dari bulan lalu")
    with col2:
        st.metric(label="Pakaian Diselamatkan", value=f"{global_impact['pakaian_diselamatkan']:,} pcs", delta="↑ 8% dari bulan lalu")
    with col3:
        st.metric(label="Air Dihemat (Simulasi)", value=f"{global_impact['air_dihemat_liter']:,} L", delta="↑ 12% dari bulan lalu")
    with col4:
        st.metric(label="Emisi Karbon Dikurangi (Simulasi)", value=f"{global_impact['karbon_dikurangi_kg']:,} kg CO2", delta="↑ 10% dari bulan lalu")

    st.subheader("Simulasi Data Tren Pakaian Bekas")
    
    # Data dummy untuk grafik tren
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Penjualan', 'Donasi', 'Daur Ulang']
    ).cumsum()
    
    st.area_chart(chart_data)

    st.subheader("Kolaborasi: Keahlian yang Terlibat")
    # Tampilkan bidang keahlian
    expertise = {
        "Teknologi": "Membangun aplikasi, cloud database, dan sistem AI.",
        "Analis Bisnis": "Memastikan fitur sesuai target pasar dan model bisnis.",
        "Desain UI/UX": "Merancang alur pengguna yang mulus untuk membangun kepercayaan.",
        "Operasional & Logistik": "Mengelola alur C2C, keamanan transaksi, dan penanganan komplain.",
        "Lingkungan & Komunikasi": "Mengukur dampak pengurangan limbah dan mengedukasi misi keberlanjutan."
    }
    
    cols = st.columns(len(expertise))
    for i, (key, value) in enumerate(expertise.items()):
        with cols[i]:
            st.info(f"**{key}**\n\n_{value}_")
            

# --- BAGIAN 2: Marketplace & Donasi (Bab III) ---
elif menu_selection == "Marketplace & Donasi (Bab III)":
    st.header("🛒 Marketplace Pakaian Bekas & Menu Donasi Otomatis")
    st.markdown("""
    Ini adalah jantung dari RE-WEAR. Pengguna dapat menjual, membeli, atau mendonasikan pakaian layak pakai.
    """)

    tab1, tab2 = st.tabs(["Lihat Item", "Jual / Donasi Item Baru"])
    
    with tab1:
        st.subheader("Daftar Pakaian Tersedia")
        
        items_df = pd.DataFrame(st.session_state.items_for_sale)
        
        # Filter Tipe
        tipe_filter = st.radio("Tampilkan:", ["Semua", "Jual", "Donasi"], horizontal=True)
        if tipe_filter != "Semua":
            items_df = items_df[items_df['tipe'] == tipe_filter]

        
        # Tampilkan dalam format kartu
        cols = st.columns(3)
        for i, row in items_df.iterrows():
            with cols[i % 3]:
                card_title = f"{row['nama']} ({row['tipe']})"
                card_body = f"""
                **{format_rupiah(row['harga'])}**
                
                *Dampak Lingkungan:* {row['dampak']} Poin 🍃
                
                {row['deskripsi']}
                """
                
                if row['tipe'] == 'Donasi':
                    st.success(f"**{card_title}**\n\n{card_body}")
                    st.button("Minta Donasi", key=f"d{row['id']}")
                else:
                    st.warning(f"**{card_title}**\n\n{card_body}")
                    st.button("Beli Sekarang", key=f"b{row['id']}")
                    
    with tab2:
        st.subheader("Tambahkan Pakaian Anda")
        
        with st.form("form_add_item"):
            input_nama = st.text_input("Nama Pakaian (Contoh: Kemeja Batik Modern)")
            input_deskripsi = st.text_area("Deskripsi & Kondisi Pakaian")
            input_tipe = st.radio("Pilih Tipe Transaksi:", ["Jual", "Donasi"], horizontal=True)
            
            input_harga = 0
            if input_tipe == "Jual":
                input_harga = st.number_input("Harga Jual (Rp)", min_value=10000, value=50000, step=10000)
            else:
                st.info("Pakaian Donasi akan disalurkan otomatis berdasarkan kebutuhan mitra kami.")
                
            submitted = st.form_submit_button("Submit Item")
            
            if submitted:
                if input_nama and input_deskripsi:
                    add_new_item(input_nama, input_deskripsi, input_harga, input_tipe)
                else:
                    st.error("Nama dan Deskripsi harus diisi!")

# --- BAGIAN 3: AI Recommendation ---
elif menu_selection == "AI Recommendation":
    st.header("💡 AI Recommendation System")
    st.subheader("Mencocokkan Pakaian dengan Preferensi Anda")
    st.markdown("""
    Fitur ini menggunakan AI/Machine Learning untuk menganalisis riwayat pembelian, gaya, dan ukuran Anda, lalu memberikan rekomendasi item bekas yang paling relevan.
    """)
    
    st.image("https://placehold.co/800x200/4c7c59/ffffff?text=Simulasi+Sistem+Rekomendasi+AI", caption="Simulasi Tampilan Rekomendasi di Aplikasi", use_column_width=True)

    st.subheader("Profil Pengguna (Simulasi Input Data)")
    col_profile_1, col_profile_2, col_profile_3 = st.columns(3)
    
    with col_profile_1:
        st.selectbox("Ukuran Atasan", ["M", "L", "XL"], index=1)
        st.multiselect("Gaya Favorit", ["Minimalis", "Streetwear", "Vintage", "Formal"], default=["Vintage"])
        
    with col_profile_2:
        st.selectbox("Warna Dominan Pilihan", ["Hitam", "Putih", "Navy", "Coklat"])
        st.number_input("Budget Maksimum (Rp)", min_value=50000, value=300000, step=50000)
        
    with col_profile_3:
        st.slider("Prioritas Dampak Lingkungan (0=Gaya, 10=Dampak)", 0, 10, 8)
        
    st.button("Refresh Rekomendasi AI")
    
    st.subheader("Rekomendasi Terbaik untuk Anda:")
    
    # Item Rekomendasi (Disimulasikan berdasarkan item teratas di data dummy)
    reco_items = sorted(st.session_state.items_for_sale, key=lambda x: x['dampak'] * 0.5 + x['disukai'] * 0.5, reverse=True)[:3]
    
    col_reco = st.columns(3)
    
    for i, item in enumerate(reco_items):
        with col_reco[i]:
            st.info(f"**⭐ REKOMENDASI AI: {item['nama']}**")
            st.markdown(f"""
            - **Harga:** {format_rupiah(item['harga'])}
            - **Tipe:** {item['tipe']}
            - **Dampak Poin:** {item['dampak']} 🍃
            - *Alasan AI: Sesuai dengan gaya Vintage & Prioritas Dampak Tinggi.*
            """)
            st.button("Lihat Detail", key=f"reco{item['id']}")
            

# --- BAGIAN 4: Gamifikasi & Edukasi ---
elif menu_selection == "Gamifikasi & Edukasi":
    st.header("🏆 Gamifikasi & Edukasi Dampak")
    st.subheader("Membuat Keberlanjutan Menjadi Menarik")
    st.markdown("""
    Fitur ini mendorong partisipasi aktif pengguna melalui poin, lencana, dan papan peringkat, sekaligus menyediakan edukasi mengenai isu fast fashion.
    """)

    tab_gami_1, tab_gami_2 = st.tabs(["Dampak Personal Anda", "Edukasi & Tips"])
    
    # Data dummy untuk pengguna saat ini
    user_impact = {
        "nama": "Pengguna RE-WEAR",
        "total_poin": 850,
        "lencana": ["Pahlawan Donasi", "Penjual Ramah Lingkungan"],
        "limbah_dihemat_kg": 15,
        "posisi_leaderboard": 120
    }

    with tab_gami_1:
        st.subheader(f"Halo, {user_impact['nama']}!")
        
        col_gami_1, col_gami_2, col_gami_3 = st.columns(3)
        
        with col_gami_1:
            st.metric("Total Poin Keberlanjutan", f"{user_impact['total_poin']} Poin", "+50 hari ini")
        with col_gami_2:
            st.metric("Limbah Dihemat (Personal)", f"{user_impact['limbah_dihemat_kg']} kg")
        with col_gami_3:
            st.metric("Peringkat Leaderboard", f"#{user_impact['posisi_leaderboard']}")
            
        st.progress(user_impact['total_poin'] / 1000, text="Progress menuju Level 'Ambassador' (1000 Poin)")

        st.info(f"Lencana yang Anda Miliki: {' | '.join([f'🏅 {l}' for l in user_impact['lencana']])}")

    with tab_gami_2:
        st.subheader("Mengapa RE-WEAR Penting?")
        st.markdown("""
        **Fakta Cepat:** Industri fashion adalah salah satu penyumbang polusi terbesar di dunia.
        * **Air:** Produksi satu kaos katun membutuhkan hingga 2.700 liter air.
        * **Limbah:** Setiap tahun, jutaan ton tekstil berakhir di TPA, dan sebagian besar bisa digunakan kembali.
        
        **Tips Berkelanjutan Hari Ini:** Coba praktikkan aturan 3R (Reduce, Reuse, Recycle) untuk pakaian Anda. Dengan menjual atau mendonasikan di RE-WEAR, Anda sedang melakukan 'Reuse' yang berdampak besar!
        """)
        st.button("Pelajari Lebih Lanjut tentang Fast Fashion", type="primary")

# --- FOOTER ---
st.divider()
st.caption("Prototipe RE-WEAR | Solusi Berbasis Teknologi untuk Keberlanjutan - Diimplementasikan dengan Streamlit")