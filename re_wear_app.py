import streamlit as st
import pandas as pd
import numpy as np
import time

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="RE-WEAR: Platform Fashion Berkelanjutan",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Dummy untuk Simulasi ---
if 'items_for_sale' not in st.session_state:
    st.session_state.items_for_sale = [
        {"id": 1, "nama": "Jaket Denim Vintage (L)", "deskripsi": "Kondisi: Good. Detail foto cacat minor ada di album.", "harga": 150000, "tipe": "Jual", "kualitas": "Good", "dampak": 2.5, "rating_penjual": 4.8},
        {"id": 2, "nama": "Kemeja Flanel Merah", "deskripsi": "Barang Donasi (Gratis). Otomatis disalurkan ke panti asuhan.", "harga": 0, "tipe": "Donasi", "kualitas": "Like New", "dampak": 1.5, "rating_penjual": 5.0},
        {"id": 3, "nama": "Sepatu Kanvas Putih (40)", "deskripsi": "Kondisi: Minor Defect. Ada noda kecil di sisi kiri.", "harga": 80000, "tipe": "Jual", "kualitas": "Minor Defect", "dampak": 3.0, "rating_penjual": 4.1},
        {"id": 4, "nama": "Dress Musim Panas (M)", "deskripsi": "Kondisi: Like New. Baru dipakai sekali untuk foto.", "harga": 120000, "tipe": "Jual", "kualitas": "Like New", "dampak": 1.8, "rating_penjual": 4.9},
    ]

# Data Dampak Global (simulasi metrik)
global_impact = {
    "limbah_dihemat_kg": 5200,
    "pakaian_diselamatkan": 12500,
    "air_dihemat_liter": 6000000,
}

# Data Dampak Personal
user_impact = {
    "nama": "Pengguna RE-WEAR ID: 900456",
    "total_poin": 850,
    "lencana": ["Pahlawan Donasi", "Penjual Ramah Lingkungan"],
    "limbah_dihemat_kg": 15,
    "posisi_leaderboard": 120
}

# --- Fungsi Utility ---
def format_rupiah(angka):
    """Format angka menjadi string Rupiah."""
    return f"Rp {angka:,.0f}".replace(",", ".")

def add_new_item(nama, deskripsi, harga, tipe, kualitas):
    """Menambahkan item baru ke daftar (simulasi)."""
    new_id = max(item['id'] for item in st.session_state.items_for_sale) + 1
    dampak = np.random.uniform(1.0, 5.0) # Dampak random
    st.session_state.items_for_sale.append({
        "id": new_id,
        "nama": nama,
        "deskripsi": deskripsi,
        "harga": harga,
        "tipe": tipe,
        "kualitas": kualitas,
        "dampak": round(dampak, 2),
        "rating_penjual": round(np.random.uniform(4.0, 5.0), 1)
    })
    st.success(f"Item '{nama}' berhasil ditambahkan! Dampak lingkungan sudah mulai terhitung.")
    time.sleep(1)
    st.rerun()

# --- HEADER APLIKASI ---
st.title("RE-WEAR ♻️")
st.markdown("Platform Digital untuk Jual-Beli, Donasi, dan Daur Ulang Pakaian Bekas.")
st.divider()

# --- SIDEBAR NAVIGASI BERDASARKAN FITUR UTAMA ---
st.sidebar.title("MENU DEMO APLIKASI")
menu_selection = st.sidebar.radio(
    "Pilih Fitur Kunci RE-WEAR",
    ["Marketplace & Donasi", "Dampak & Gamifikasi", "AI Rekomendasi Gaya", "Sistem Kepercayaan & C2C"]
)

# --- BAGIAN 1: Marketplace & Donasi ---
if menu_selection == "Marketplace & Donasi":
    st.header("🛒 Marketplace & Menu Donasi Otomatis")
    st.markdown("""
    Jual, beli, atau donasikan pakaian bekas layak pakai secara transparan.
    """)

    tab1, tab2 = st.tabs(["Telusuri Pakaian", "Jual / Donasi Item Baru"])
    
    with tab1:
        st.subheader("Pakaian Siap Pakai Hari Ini")
        
        items_df = pd.DataFrame(st.session_state.items_for_sale)
        
        # Filter berdasarkan Tipe & Kualitas
        col_filter_1, col_filter_2 = st.columns(2)
        with col_filter_1:
            tipe_filter = st.radio("Tampilkan:", ["Semua", "Jual", "Donasi"], horizontal=True, key="filter_tipe")
        with col_filter_2:
            kualitas_filter = st.selectbox("Filter Kualitas:", ["Semua", "Like New", "Good", "Minor Defect"], key="filter_kualitas")

        if tipe_filter != "Semua":
            items_df = items_df[items_df['tipe'] == tipe_filter]
        if kualitas_filter != "Semua":
            items_df = items_df[items_df['kualitas'] == kualitas_filter]

        
        # Tampilkan dalam format kartu
        st.write(f"Ditemukan {len(items_df)} item.")
        
        cols = st.columns(4)
        for i, row in items_df.iterrows():
            with cols[i % 4]:
                card_title = f"{row['nama']}"
                
                # Menentukan tampilan harga dan warna kotak berdasarkan tipe (Jual/Donasi)
                if row['tipe'] == 'Donasi':
                    harga_display = "**GRATIS / Donasi**"
                    box_func = st.success # Warna hijau untuk donasi
                    button_label = "Minta Donasi"
                    button_type = "secondary"
                else:
                    harga_display = format_rupiah(row['harga'])
                    box_func = st.info # Warna biru untuk dijual
                    button_label = "Beli / Tawar"
                    button_type = "primary"

                card_body = f"""
                **{harga_display}**
                
                Kualitas: **{row['kualitas']}** Dampak Poin: **{row['dampak']}** 🍃
                
                Penjual: ⭐ {row['rating_penjual']}
                """
                
                box_func(f"**{card_title}**\n\n{card_body}")
                st.button(button_label, key=f"b_{row['id']}", type=button_type, help=row['deskripsi'])
                    
    with tab2:
        st.subheader("Upload Pakaian Anda untuk Dijual atau Didonasikan")
        
        with st.form("form_add_item"):
            st.markdown("##### Informasi Pakaian")
            input_nama = st.text_input("Nama Pakaian (Contoh: Kemeja Batik Modern)")
            
            # Simulasi Standarisasi Kualitas & Kejujuran Penjual
            input_kualitas = st.selectbox("Pilih Standar Kualitas Pakaian:", 
                                         ["Like New (95%+)", "Good (Layak pakai, 80-95%)", "Minor Defect (Ada cacat kecil)"])
            
            st.file_uploader("Upload Foto Produk (Wajib, minimal 3 foto)", accept_multiple_files=True)
            if input_kualitas == "Minor Defect":
                st.warning("⚠️ Wajib Upload Foto Detail Cacat untuk transparansi!")
                st.file_uploader("Upload Foto Detail Cacat", accept_multiple_files=False)
                
            input_deskripsi = st.text_area("Deskripsi Pakaian & Detail Cacat (Jika ada)")

            st.markdown("##### Tipe Transaksi")
            input_tipe = st.radio("Pilih Transaksi:", ["Jual", "Donasi"], horizontal=True)
            
            input_harga = 0
            if input_tipe == "Jual":
                input_harga = st.number_input("Harga Jual (Rp)", min_value=10000, value=50000, step=10000)
            else:
                st.info("Otomatis: Pakaian Donasi akan diproses dan disalurkan ke mitra yayasan secara transparan.")
                
            submitted = st.form_submit_button("Submit Item")
            
            if submitted:
                if input_nama and input_deskripsi:
                    add_new_item(input_nama, input_deskripsi, input_harga, input_tipe, input_kualitas.split('(')[0].strip())
                else:
                    st.error("Nama dan Deskripsi harus diisi!")

# --- BAGIAN 2: Dampak & Gamifikasi ---
elif menu_selection == "Dampak & Gamifikasi":
    st.header("📈 Tracking Dampak & Gamifikasi Keberlanjutan")
    st.markdown("""
    Lihat dampak positif yang telah Anda berikan dan bersaing dalam papan peringkat.
    """)

    tab_gami_1, tab_gami_2 = st.tabs(["Dampak Personal Anda", "Dampak Global & Metrik"])
    
    with tab_gami_1:
        st.subheader(f"Dashboard Dampak Personal: {user_impact['nama']}")
        
        col_gami_1, col_gami_2, col_gami_3 = st.columns(3)
        
        with col_gami_1:
            st.metric("Total Poin Keberlanjutan", f"{user_impact['total_poin']} Poin", "+50 hari ini (Baru saja Donasi 1 item)")
        with col_gami_2:
            st.metric("Limbah Dihemat (Personal)", f"{user_impact['limbah_dihemat_kg']} kg", help="Metrik dihitung: 1 pakaian ≈ 0.2 kg limbah terselamatkan")
        with col_gami_3:
            st.metric("Peringkat Leaderboard", f"#{user_impact['posisi_leaderboard']}", "Level: Eco-Warrior")
            
        st.progress(user_impact['total_poin'] / 1000, text="Progress menuju Level 'Eco-Ambassador' (1000 Poin)")

        st.info(f"Lencana Aktif Anda: {' | '.join([f'🏅 {l}' for l in user_impact['lencana']])}")

    with tab_gami_2:
        st.subheader("Dampak Komunitas RE-WEAR (Global)")
        
        col_global_1, col_global_2, col_global_3 = st.columns(3)
        
        with col_global_1:
            st.metric(label="Total Pakaian Diselamatkan", value=f"{global_impact['pakaian_diselamatkan']:,} pcs", delta="↑ 8% dari bulan lalu")
        with col_global_2:
            st.metric(label="Total Limbah Tekstil Dihemat", value=f"{global_impact['limbah_dihemat_kg']:,} kg", delta="↑ 15% dari bulan lalu")
        with col_global_3:
            st.metric(label="Air Dihemat (Simulasi)", value=f"{global_impact['air_dihemat_liter']:,} L", delta="↑ 12% dari bulan lalu")

        st.bar_chart(
            pd.DataFrame({'Bulan': ['Jan', 'Feb', 'Mar', 'Apr', 'Mei'], 'Pakaian Terjual': [2000, 2500, 3000, 3500, 4200]}).set_index('Bulan')
        )

# --- BAGIAN 3: AI Rekomendasi Gaya ---
elif menu_selection == "AI Rekomendasi Gaya":
    st.header("💡 AI Recommendation System (Personalisasi Gaya)")
    st.subheader("Temukan 'Harta Karun' Anda Berdasarkan Preferensi")
    st.markdown("""
    AI mencocokkan item langka/unik dengan gaya, ukuran, dan budget Anda. (Sinergi: Analis Bisnis & Tim AI)
    """)
    
    with st.expander("Atur Preferensi Gaya Anda (Input untuk AI)"):
        col_profile_1, col_profile_2, col_profile_3 = st.columns(3)
        
        with col_profile_1:
            st.selectbox("Ukuran Atasan", ["S", "M", "L", "XL"], index=2)
            st.multiselect("Gaya Favorit", ["Minimalis", "Streetwear", "Vintage", "Formal", "Casual"], default=["Vintage", "Casual"])
            
        with col_profile_2:
            st.selectbox("Kondisi Kualitas Minimal", ["Like New", "Good", "Minor Defect"], index=1)
            st.number_input("Budget Maksimum (Rp)", min_value=50000, value=200000, step=50000)
            
        with col_profile_3:
            st.slider("Prioritas Keunikan/Kelangkaan", 0, 10, 7, help="Semakin tinggi, semakin memprioritaskan barang Branded/Unik.")
            
        st.button("Update & Cari Rekomendasi AI", type="primary")
    
    st.subheader("Hasil Rekomendasi Terbaik:")
    
    # Item Rekomendasi (Disimulasikan berdasarkan item teratas di data dummy)
    reco_items = sorted(st.session_state.items_for_sale, key=lambda x: x['dampak'] * 0.4 + x['rating_penjual'] * 0.6, reverse=True)[:3]
    
    col_reco = st.columns(3)
    
    for i, item in enumerate(reco_items):
        with col_reco[i]:
            st.info(f"**⭐ REKOMENDASI UNIK UNTUK ANDA**")
            st.markdown(f"""
            ##### {item['nama']}
            - **Harga:** {format_rupiah(item['harga'])}
            - **Kualitas:** {item['kualitas']}
            - **Dampak Poin:** {item['dampak']} 🍃
            """)
            st.caption(f"*Alasan AI: Cocok dengan gaya **Vintage** & kualitas **{item['kualitas']}**.*")
            st.button("Lihat Detail & Foto Cacat", key=f"reco{item['id']}")
            

# --- BAGIAN 4: Sistem Kepercayaan & C2C ---
elif menu_selection == "Sistem Kepercayaan & C2C":
    st.header("🤝 Sistem Kepercayaan & Logistik C2C")
    st.subheader("Menjamin Kualitas, Keamanan Transaksi, dan Pengembalian")
    st.markdown("""
    Fitur ini adalah inti dari kolaborasi UI/UX, Teknologi, dan Operasional untuk mengatasi tantangan Kualitas & Kepercayaan.
    """)
    
    st.info("💡 **Jaminan Kepercayaan:** RE-WEAR menggunakan sistem **Rekening Bersama (Rekber)**. Dana pembeli ditahan hingga barang diterima dan dikonfirmasi sesuai deskripsi.")
    
    st.subheader("1. Simulasi Proses Listing (Kejujuran Penjual)")
    st.markdown("""
    Setiap penjual harus mematuhi **Standarisasi Kualitas** dan wajib mengunggah **Foto Detail Cacat** (jika ada) saat listing.
    """)
    
    sample_item = st.session_state.items_for_sale[2]
    
    st.warning(f"**Item Contoh: {sample_item['nama']}**")
    st.markdown(f"""
    - **Kualitas Dilaporkan:** `{sample_item['kualitas']}`
    - **Deskripsi Penjual:** `{sample_item['deskripsi']}`
    - **Simulasi Bukti Foto:**  - *Wajib diupload*
    """)
    
    st.subheader("2. Simulasi Transaksi (Jaminan Pengembalian)")
    
    status_transaksi = st.selectbox("Status Logistik C2C (Simulasi Alur):",
                                   ["Menunggu Pembayaran", "Dana Ditahan (Rekber Aktif)", "Barang Dikirim", "Barang Diterima Pembeli", "Komplain Diajukan"])
    
    if status_transaksi == "Barang Diterima Pembeli":
        st.success("Pembeli menerima barang. Dana ditahan Rekber. Pembeli memiliki 2x24 jam untuk 'Konfirmasi Sesuai' atau 'Ajukan Komplain'.")
        col_rekber_1, col_rekber_2 = st.columns(2)
        with col_rekber_1:
            st.button("✅ Konfirmasi Barang Sesuai (Dana Dilepas ke Penjual)", type="primary")
        with col_rekber_2:
            st.button("🚨 Ajukan Komplain / Pengembalian", type="secondary")
            
    elif status_transaksi == "Komplain Diajukan":
        st.error("🚨 Komplain Aktif! Tim Operasional (Customer Service) akan memediasi berdasarkan bukti foto dan deskripsi awal.")
        st.markdown("**(Sinergi Tim Operasional & Manajemen Risiko)**")
    
    st.subheader("3. Verifikasi Penjual & Rating")
    st.markdown("Setiap penjual melewati proses verifikasi, dan rating menjadi metrik utama kepercayaan.")
    st.metric("Verifikasi Penjual A", "Terverifikasi ✅", "Rating: 4.8 / 5.0")


# --- FOOTER ---
st.divider()
st.caption(f"Demo Aplikasi RE-WEAR | Pengguna ID Saat Ini: {user_impact['nama'].split(': ')[1]}")
st.caption("Fokus: Membangun Kepercayaan, Mengukur Dampak, dan Personalisasi Gaya.")
