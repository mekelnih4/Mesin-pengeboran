import streamlit as st
import os
import sys
from datetime import datetime

# Import fungsi dari file asli (import os.py)
# Asumsikan file asli bernama import_os.py atau sesuaikan
# Untuk demo, kita buat versi sederhana

st.title("Aplikasi Penghitung Lubang Kayu - Streamlit")

st.sidebar.header("Pilih Bagian Kayu")
bagian = st.sidebar.selectbox("Bagian", ["DSKA", "DSKI", "DB", "TOP", "AMB"])

st.header(f"Program untuk {bagian}")

# Contoh input sederhana untuk DB
if bagian == "DB":
    st.subheader("Dinding Belakang (DB)")
    panjang = st.number_input("Panjang Kayu (mm)", min_value=0.0, value=800.0)
    lebar = st.number_input("Lebar Kayu (mm)", min_value=0.0, value=300.0)
    kedalaman = st.number_input("Ketebalan Kayu (mm)", min_value=0.0, value=16.0)
    jarak_lantai = st.number_input("Jarak dari lantai ke drawernya (mm)", min_value=0.0, value=76.0)

    if st.button("Hitung Lubang"):
        # Logika sederhana dari handle_db
        Kelipatan = (int(panjang) // 32) * 32 - 64
        Kelipatan2 = (int(lebar) // 32) * 32 - 64

        L4_X = -(76 - jarak_lantai)
        L4_Y = (lebar - (Kelipatan2 - 32)) / 2
        L4_Diameter = 5
        L4_QTY = 2

        L5_X = -(76 - jarak_lantai)
        L5_Y = L4_Y + 64
        L5_Diameter = 8
        L5_QTY = 2

        L6_X = panjang / 2
        L6_Y = -(kedalaman / 2)
        L6_Diameter = 8
        L6_QTY = 1

        st.write("### Hasil Lubang:")
        st.write(f"Lubang 1: X={L4_X}, Y={L4_Y}, Diameter={L4_Diameter}, QTY={L4_QTY}")
        st.write(f"Lubang 2: X={L5_X}, Y={L5_Y}, Diameter={L5_Diameter}, QTY={L5_QTY}")
        st.write(f"Lubang 3: X={L6_X}, Y={L6_Y}, Diameter={L6_Diameter}, QTY={L6_QTY}")

elif bagian == "DSKI":
    st.subheader("Dinding Samping Kiri (DSKI)")
    panjang = st.number_input("Panjang Kayu (mm)", min_value=0.0, value=600.0)
    lebar = st.number_input("Lebar Kayu (mm)", min_value=0.0, value=443.0)
    tebal = st.number_input("Tebal Kayu (mm)", min_value=0.0, value=18.0)
    has_plin = st.selectbox("Apakah terdapat plin pada meja?", ["y", "n"])
    
    # Default values
    plin_choices = []
    Lebar_plin = 0.0
    Tinggi_plinatas = 0.0
    Jumlah_plin_depan = 0
    Tinggi_plindepan = 0.0
    Tinggi_plindepan2 = 0.0
    Tinggi_plinbawah = 0.0
    
    if has_plin == "y":
        plin_choices = st.multiselect("Pilih plin (1=atas,2=depan,3=bawah)", [1,2,3], default=[2])
        Lebar_plin = st.number_input("Lebar Plin (mm)", min_value=0.0, value=361.0)
        if 1 in plin_choices:
            Tinggi_plinatas = st.number_input("Tinggi Plin Atas (mm)", min_value=0.0, value=60.0)
        if 2 in plin_choices:
            Jumlah_plin_depan = st.selectbox("Jumlah plin depan", [1,2])
            Tinggi_plindepan = st.number_input("Tinggi Plin Depan 1 (mm)", min_value=0.0, value=60.0)
            if Jumlah_plin_depan == 2:
                Tinggi_plindepan2 = st.number_input("Tinggi Plin Depan 2 (mm)", min_value=0.0, value=40.0)
        if 3 in plin_choices:
            Tinggi_plinbawah = st.number_input("Tinggi Plin Bawah (mm)", min_value=0.0, value=40.0)
    Tebal_ambalan_bawah = st.number_input("Tebal Ambalan Bawah (mm)", min_value=0.0, value=25.0)
    jarak_lantai = st.number_input("Jarak dari lantai ke drawernya (mm)", min_value=0.0, value=20.0)
    pintu_count = st.selectbox("Berapa pintu yang dimiliki drawernya?", [2,3])
    Lebar_pintu = st.number_input("Lebar pintu (mm)", min_value=0.0, value=394.0)
    Tinggi_pintu_1 = st.number_input("Tinggi pintu 1 (mm)", min_value=0.0, value=114.0)
    Tinggi_pintu_2 = st.number_input("Tinggi pintu 2 (mm)", min_value=0.0, value=114.0)
    Tinggi_pintu_3 = 0.0
    if pintu_count == 3:
        Tinggi_pintu_3 = st.number_input("Tinggi pintu 3 (mm)", min_value=0.0, value=325.0)

    if st.button("Hitung Lubang"):
        # Logika lengkap dari handle_dski
        Kelipatan = (int(panjang) // 32) * 32 - 64
        Kelipatan2 = (int(lebar) // 32) * 32 - 64
        quantity = [1, 2]

        # Map inputs
        has_plin_val = 'y' if has_plin == 'y' else 'n'
        plin_choices_val = plin_choices if has_plin_val == 'y' else []
        if not plin_choices_val or has_plin_val != 'y':
            Lebar_plin = 0
            Tinggi_plinatas = 0
            Jumlah_plin_depan = 0
            Tinggi_plindepan = 0
            Tinggi_plindepan2 = 0
            Tinggi_plinbawah = 0
            Tebal_ambalan_bawah = 0
        else:
            Tinggi_plinatas = Tinggi_plinatas if 1 in plin_choices_val else 0
            Jumlah_plin_depan = Jumlah_plin_depan if 2 in plin_choices_val else 0
            Tinggi_plindepan = Tinggi_plindepan if 2 in plin_choices_val else 0
            Tinggi_plindepan2 = Tinggi_plindepan2 if Jumlah_plin_depan == 2 else 0
            Tinggi_plinbawah = Tinggi_plinbawah if 3 in plin_choices_val else 0

        # Collect holes
        holes = []

        # Lubang TOP 1
        DKI_Lubang1_X = 0
        DKI_Lubang1_Y = (lebar - (Kelipatan2 - 32)) / 2
        DKI_Lubang1_Yoffset = Kelipatan2 - 32
        holes.append({'x': DKI_Lubang1_X, 'y': DKI_Lubang1_Y, 'diameter': 8, 'qty': quantity[1], 'xoffset': 0, 'yoffset': DKI_Lubang1_Yoffset})

        # Lubang TOP 2
        DKI_Lubang2_X = 0
        DKI_Lubang2_Y = DKI_Lubang1_Y + 64
        holes.append({'x': DKI_Lubang2_X, 'y': DKI_Lubang2_Y, 'diameter': 8, 'qty': quantity[1], 'xoffset': 0, 'yoffset': DKI_Lubang1_Yoffset - 128})

        # Lubang TOP 3
        DKI_Lubang3_X = 25
        DKI_Lubang3_Y = (lebar - (Kelipatan2 - 32)) / 2
        holes.append({'x': DKI_Lubang3_X, 'y': DKI_Lubang3_Y, 'diameter': 15, 'qty': quantity[0], 'xoffset': 0, 'yoffset': Kelipatan2 - 32})

        # Lubang DB 1
        DKI_Lubang4_X = -(76 - jarak_lantai)
        DKI_Lubang4_Y = (lebar - (Kelipatan2 - 32)) / 2
        holes.append({'x': DKI_Lubang4_X, 'y': DKI_Lubang4_Y, 'diameter': 5, 'qty': quantity[1], 'xoffset': 0, 'yoffset': Kelipatan2 - 32})

        # Lubang DB 2
        DKI_Lubang5_X = -(76 - jarak_lantai)
        DKI_Lubang5_Y = DKI_Lubang1_Y + 64
        holes.append({'x': DKI_Lubang5_X, 'y': DKI_Lubang5_Y, 'diameter': 8, 'qty': quantity[1], 'xoffset': 0, 'yoffset': DKI_Lubang1_Yoffset - 128})

        # Lubang DB 3
        DKI_Lubang7_X = panjang / 2 
        DKI_Lubang7_Y = -(tebal / 2)
        holes.append({'x': DKI_Lubang7_X, 'y': DKI_Lubang7_Y, 'diameter': 8, 'qty': quantity[0], 'xoffset': 0, 'yoffset': 0})

        # Lubang AMB 1
        mid = (panjang - Kelipatan) / 2
        diff = DKI_Lubang4_X - mid
        if diff > 28:
            DKI_Lubang8_X = mid
        else:
            SELISIH = (mid - DKI_Lubang4_X)
            PENGISI = 28 - SELISIH
            DKI_Lubang8_X = mid + PENGISI
        DKI_Lubang8_Y = -(tebal / 2)
        holes.append({'x': DKI_Lubang8_X, 'y': DKI_Lubang8_Y, 'diameter': 5, 'qty': quantity[1], 'xoffset': -(Kelipatan), 'yoffset': 0})

        # Lubang AMB 2
        DKI_Lubang9_X = DKI_Lubang8_X - 64
        DKI_Lubang9_Y = -(tebal / 2)
        holes.append({'x': DKI_Lubang9_X, 'y': DKI_Lubang9_Y, 'diameter': 8, 'qty': quantity[1], 'xoffset': -(Kelipatan - 128), 'yoffset': 0})

        # Plin holes
        if 2 in plin_choices:
            DKI_Lubang10_X = Tinggi_pintu_1
            DKI_Lubang10_Y = (tebal / 2) + 1
            holes.append({'x': DKI_Lubang10_X, 'y': DKI_Lubang10_Y, 'diameter': 5, 'qty': quantity[0], 'xoffset': 0, 'yoffset': 0})

            if Tinggi_plindepan == 60:
                DKI_Lubang11_X = DKI_Lubang10_X + 32
            elif Tinggi_plindepan == 40:
                DKI_Lubang11_X = DKI_Lubang10_X + 20
            else:
                DKI_Lubang11_X = DKI_Lubang10_X + 32
            DKI_Lubang11_Y = DKI_Lubang10_Y
            holes.append({'x': DKI_Lubang11_X, 'y': DKI_Lubang11_Y, 'diameter': 8, 'qty': quantity[0], 'xoffset': 0, 'yoffset': 0})

        if 2 in plin_choices and Jumlah_plin_depan == 2:
            DKI_Lubang12_X = (Tinggi_pintu_1 + 20 + Tinggi_pintu_2) + 10
            DKI_Lubang12_Y = (tebal / 2) + 1
            holes.append({'x': DKI_Lubang12_X, 'y': DKI_Lubang12_Y, 'diameter': 8, 'qty': quantity[1], 'xoffset': 20, 'yoffset': 0})

        # Rail holes
        if Tinggi_plindepan == 60:
            DKI_Lubang13_X = Tinggi_pintu_1 - 25 - 7 - (Tinggi_plinatas if Tinggi_plinatas else 0)
        elif Tinggi_plindepan == 40:
            DKI_Lubang13_X = Tinggi_pintu_1 - 31 - 7 - (Tinggi_plinatas if Tinggi_plinatas else 0)
        else:
            DKI_Lubang13_X = Tinggi_pintu_1 - 25 - 7
        DKI_Lubang13_Y = 54
        holes.append({'x': DKI_Lubang13_X, 'y': DKI_Lubang13_Y, 'diameter': 5, 'qty': quantity[1], 'xoffset': 0, 'yoffset': 276, 'label': 'RAIL 1'})

        DKI_Lubang14_X = Tinggi_pintu_1 + 20 + Tinggi_pintu_2 - 9 - 12
        DKI_Lubang14_Y = 54
        holes.append({'x': DKI_Lubang14_X, 'y': DKI_Lubang14_Y, 'diameter': 5, 'qty': quantity[1], 'xoffset': 0, 'yoffset': 276, 'label': 'RAIL 2'})

        if pintu_count == 3:
            if Tebal_ambalan_bawah == 18:
                DKI_Lubang15_X = DKI_Lubang4_X - 9 - 6 - 21
            else:
                DKI_Lubang15_X = DKI_Lubang4_X - 15 - 6 - 21
            DKI_Lubang15_Y = 54
            holes.append({'x': DKI_Lubang15_X, 'y': DKI_Lubang15_Y, 'diameter': 5, 'qty': quantity[1], 'xoffset': 0, 'yoffset': 288, 'label': 'RAIL 3'})

        if 3 in plin_choices and Tinggi_plinbawah:
            L16_X = - ((Tinggi_plinbawah - 32) / 10)
            L16_Y = (tebal / 2) + 1
            holes.append({'x': L16_X, 'y': L16_Y, 'diameter': 5, 'qty': 2, 'xoffset': 32, 'yoffset': 0})

        if 1 in plin_choices and Tinggi_plinatas:
            if Tinggi_plinatas == 40:
                L19_X = 10
            elif Tinggi_plinatas == 60:
                L19_X = 14
            else:
                L19_X = None
            if L19_X:
                L19_Y = (tebal / 2) + 1
                holes.append({'x': L19_X, 'y': L19_Y, 'diameter': 5, 'qty': 2, 'xoffset': 32, 'yoffset': 0})

        # Output holes
        hole_types = {
            1: "TOP 1", 2: "TOP 2", 3: "TOP 3", 4: "AMB 1", 5: "AMB 2", 6: "DB 1", 7: "DB 2", 8: "DB 3",
            9: "PLIN DEPAN 1a", 10: "PLIN DEPAN 1b", 11: "PLIN DEPAN 2", 12: "PLIN DEPAN 3",
            13: "RAIL 1", 14: "RAIL 2", 15: "RAIL 3", 16: "PLIN BAWAH", 17: "PLIN ATAS",
        }
        st.write("### Hasil Lubang untuk DSKI:")
        for idx, h in enumerate(holes, start=1):
            label = h.get('label') or hole_types.get(idx, "")
            st.write(f"Lubang {idx} ({label}): X={h['x']}, Y={h['y']}, Diameter={h['diameter']}, QTY={h['qty']}, Xoffset={h['xoffset']}, Yoffset={h['yoffset']}")

elif bagian == "AMB":
    st.subheader("Ambalan Bawah (AMB)")
    panjang = st.number_input("Panjang Kayu (mm)", min_value=0.0, value=600.0)
    lebar = st.number_input("Lebar Kayu (mm)", min_value=0.0, value=200.0)
    kedalaman = st.number_input("Ketebalan Kayu (mm)", min_value=0.0, value=16.0)

    if st.button("Hitung Lubang"):
        Kelipatan = (int(panjang) // 32) * 32 - 64
        XLubang1 = (panjang - Kelipatan) / 2
        YLubang1 = 0
        quantity = [1, 2]

        st.write("### Hasil Lubang:")
        st.write(f"Lubang 1: X={XLubang1}, Y={YLubang1}, Diameter=8, QTY={quantity[1]}, Xoffset={Kelipatan}, Yoffset=0")
        
        XLubang2 = XLubang1 + 64
        YLubang2 = 0
        st.write(f"Lubang 2: X={XLubang2}, Y={YLubang2}, Diameter=8, QTY={quantity[1]}, Xoffset={Kelipatan - 128}, Yoffset=0")
        
        XLubang3 = XLubang1
        YLubang3 = 25
        st.write(f"Lubang 3: X={XLubang3}, Y={YLubang3}, Diameter=25, QTY={quantity[1]}, Xoffset={Kelipatan}, Yoffset=0")
        
        XLubang4 = panjang / 2
        YLubang4 = 0
        st.write(f"Lubang 4: X={XLubang4}, Y={YLubang4}, Diameter=8, QTY={quantity[0]}, Xoffset=0, Yoffset=0")

elif bagian == "TOP":
    st.subheader("TOP")
    panjang = st.number_input("Panjang Kayu (mm)", min_value=0.0, value=800.0)
    lebar = st.number_input("Lebar Kayu (mm)", min_value=0.0, value=400.0)
    tebal = st.number_input("Tebal Kayu (mm)", min_value=0.0, value=18.0)
    lebar_dski = st.number_input("Lebar DSKI (mm)", min_value=0.0, value=443.0)
    lebar_db = st.number_input("Lebar DB (mm)", min_value=0.0, value=300.0)
    tebal_dski = st.number_input("Tebal DSKI (mm)", min_value=0.0, value=18.0)
    sela = st.number_input("Sela", min_value=0.0, value=100.0)

    if st.button("Hitung Lubang"):
        Kelipatan = (int(panjang) // 32) * 32 - 64
        Kelipatan2 = (int(lebar) // 32) * 32 - 64
        Kelipatan2_dski = (int(lebar_dski) // 32) * 32 - 64
        quantity = [1, 2]

        top1_x = ((lebar - (lebar_db + (tebal_dski * 2))) / 2) + (tebal_dski / 2)
        top1_y = ((lebar_dski - (Kelipatan2_dski - 32)) / 2) + sela

        st.write("### Hasil Lubang:")
        st.write(f"Lubang 1: X={top1_x}, Y={top1_y}, Diameter=5, QTY={quantity[1]}, Xoffset=0, Yoffset=256")

        top2_x = top1_x
        top2_y = top1_y + 64
        st.write(f"Lubang 2: X={top2_x}, Y={top2_y}, Diameter=8, QTY={quantity[1]}, Xoffset=0, Yoffset=128")

else:
    st.write("Fitur untuk bagian ini belum diimplementasikan.")

# Footer
st.write("---")
st.write("Aplikasi sederhana dengan Streamlit.")
