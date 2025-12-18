import os
import sys
from datetime import datetime

# Variabel tambahan untuk offset plin depan
X_plindepan_60 = 14
X_plindepan_40 = 10

# When set to a dict, run_form will auto-fill prompts from this template.
AUTO_FILL_TEMPLATE = None

# Konstanta untuk ukuran plin dan pintu standar
PLIN_SIZES = {
    '40': {'tinggi': 40, 'x_offset': 10},
    '60': {'tinggi': 60, 'x_offset': 14}
}

# Default template values
DEFAULT_VALUES = {
    'tebal_min': 16,
    'tebal_max': 25,
    'plin_min': 40,
    'plin_max': 60
}

# Example test templates for each bagian. Adjust values as you like.
TEST_TEMPLATES = {
    'DSKI': {
        'panjang': 600.0,
        'lebar': 443.0,
        'tebal': 18.0,
        'has_plin': 'y',
        'plin_choices': [2],
        'Lebar_plin': 361.0,
        'Jumlah_plin_depan': 2,
        'Tinggi_plindepan': 60.0,
        'Tinggi_plindepan2': 40.0,
        'Tebal_ambalan_bawah': 25.0,
        'jarak_lantai': 20.0,
        'pintu_count': 3,
        'Lebar_pintu': 394.0,
        'Tinggi_pintu_1': 114.0,
        'Tinggi_pintu_2': 114.0,
        'Tinggi_pintu_3': 325.0,
    },
    'DB': {
        'panjang': 800.0,
        'lebar': 300.0,
        'kedalaman': 16.0,
        'jarak_lantai': 76.0,
    },
    'AMB': {
        'panjang': 600.0,
        'lebar': 200.0,
        'kedalaman': 16.0,
    },
    'DSKA': {
        'panjang': 800.0,
        'lebar': 200.0,
        'tebal': 16.0,
    },
    'TOP': {
        'panjang': 800.0,
        'lebar': 400.0,
        'tebal': 18.0,
    }
}


def clear_screen():
    # Gunakan 'cls' untuk Windows, 'clear' untuk sistem lain
    os.system('cls' if os.name == 'nt' else 'clear')


bagian = ["DSKA", "DSKI", "DB", "TOP", "AMB"]

# Bersihkan layar dan tampilkan header singkat tiap run
clear_screen()
print("========================\nProgram mesin pengeboran\n========================")


# Utility: centralized hole output formatting
def print_hole(idx, x, y, diameter, qty, xoffset, yoffset, hole_type="", mirror: str = None):
    """Print a hole's parameters in the standard format.

    mirror: optional string to print a 'Mirror' line immediately after Yoffset.
    """
    type_text = f" ({hole_type})" if hole_type else ""
    # Build base lines
    out = f"""
Lubang {idx}{type_text} memiliki:
X        : {x} mm
Y        : {y} mm
Diameter : {diameter} mm
QTY      : {qty}
Xoffset  : {xoffset} mm
Yoffset  : {yoffset} mm
"""
    # Append mirror line inside the same block when provided
    if mirror:
        out += f"Mirror   : {mirror}\n"
    print(out)

# Helper: input that supports 'x' to go back one step with validation
def input_with_back(prompt, cast=None, allow_empty=False, min_val=None, max_val=None, options=None):
    while True:
        s = input(prompt).strip()
        if not s and allow_empty:
            return (s, False)
        if s.lower() == 'x':
            return (None, True)
        if cast is None:
            if options and s not in options:
                print(f"Input harus salah satu dari: {', '.join(options)}")
                continue
            return (s, False)
        try:
            val = cast(s)
            if min_val is not None and val < min_val:
                print(f"Nilai minimal adalah {min_val}")
                continue
            if max_val is not None and val > max_val:
                print(f"Nilai maksimal adalah {max_val}")
                continue
            return (val, False)
        except ValueError:
            print("Input tidak valid. Ketik 'x' untuk kembali atau masukkan nilai yang benar.")

# Simple form runner that supports conditional prompts and 'x' to go back
def run_form(prompts):
    answers = {}
    i = 0

    def clear_previous_lines(n: int):
        try:
            for _ in range(n):
                sys.stdout.write('\x1b[1A')
                sys.stdout.write('\x1b[2K')
            sys.stdout.flush()
        except Exception:
            pass

    while i < len(prompts):
        p = prompts[i]
        when = p.get('when')
        if when is not None and not when(answers):
            i += 1
            continue
        key = p['key']
        cast = p.get('cast')
        allow_empty = p.get('allow_empty', False)
        prompt = p['prompt']
        # If AUTO_FILL_TEMPLATE is set and contains this key, use it (testing convenience)
        if AUTO_FILL_TEMPLATE and key in AUTO_FILL_TEMPLATE:
            preset = AUTO_FILL_TEMPLATE[key]
            # show what would have been input, but don't wait
            print(f"{prompt} (auto) {preset}")
            val = preset
            back = False
            # Only auto-cast for built-in types (int, float, str, bool)
            if cast in (int, float, str, bool) and not isinstance(val, cast):
                try:
                    val = cast(val)
                except Exception:
                    pass
        else:
            val, back = input_with_back(prompt, cast=cast, allow_empty=allow_empty)
        if back:
            if i == 0:
                clear_previous_lines(1)
                return None
            prev = i - 1
            keys_to_remove = [q.get('key') for q in prompts[prev:] if q.get('key') in answers]
            total_lines_to_clear = 1 + len(keys_to_remove)
            clear_previous_lines(total_lines_to_clear)
            for q in prompts[prev:]:
                k = q.get('key')
                if k and k in answers:
                    del answers[k]
            i = prev
            continue
        answers[key] = val
        i += 1
    return answers

# Top-level selection using input_with_back (top-level 'x' will re-prompt)
while True:
    val, went_back = input_with_back("Pilih bagian kayu [DSKA / DSKI / DB / TOP / AMB] : ")
    if went_back:
        print("Tidak ada langkah sebelumnya. Silakan pilih bagian.")
        continue
    s = str(val).strip()
    if s.lower() == 'test':
        # let user pick which bagian to run the test template for
        pilihan_template = input("Masukkan bagian untuk testing [DSKA/DSKI/DB/TOP/AMB]: ").strip().upper()
        if pilihan_template in TEST_TEMPLATES:
            AUTO_FILL_TEMPLATE = TEST_TEMPLATES[pilihan_template]
            pilihan_bagian = pilihan_template
            print(f"Auto-fill template aktif untuk {pilihan_bagian}.")
            break
        else:
            print("Template tidak ditemukan untuk pilihan itu. Coba lagi.")
            continue
    pilihan_bagian = s.upper()
    break

def handle_db():
    print("\n=== Program Dinding Belakang (DB) ===")
    prompts = [
        {'key': 'panjang', 'prompt': "Masukkan Panjang Kayu (mm): ", 'cast': float},
        {'key': 'lebar', 'prompt': "Masukkan Lebar Kayu (mm): ", 'cast': float},
        {'key': 'kedalaman', 'prompt': "Masukkan Ketebalan Kayu (mm): ", 'cast': float},
        {'key': 'jarak_lantai', 'prompt': "Masukkan jarak dari lantai ke drawernya (mm): ", 'cast': float},
    ]
    answers = run_form(prompts)
    if answers is None:
        return
    panjang = answers['panjang']
    lebar = answers['lebar']
    kedalaman = answers['kedalaman']
    jarak_lantai = answers.get('jarak_lantai', 0)

    Kelipatan = (int(panjang) // 32) * 32 - 64
    Kelipatan2 = (int(lebar) // 32) * 32 - 64

    L4_X = -(76 - jarak_lantai)
    L4_Y = (lebar - (Kelipatan2 - 32)) / 2
    L4_Diameter = 5
    L4_QTY = 2
    L4_Xoffset = 0
    # Dempetkan mirror: set Y offset to 0 supaya tidak ada jarak antara mirror dan y offset
    L4_Yoffset = 0

    L5_X = -(76 - jarak_lantai)
    L5_Y = L4_Y + 64
    L5_Diameter = 8
    L5_QTY = 2
    L5_Xoffset = 0
    # Dempetkan mirror: set Y offset to 0 supaya mirror sejajar tanpa jarak
    L5_Yoffset = 0

    L6_X = panjang / 2
    L6_Y = -(kedalaman / 2)
    L6_Diameter = 8
    L6_QTY = 1
    L6_Xoffset = 0
    L6_Yoffset = 0

    print_hole(1, L4_X, L4_Y, L4_Diameter, L4_QTY, L4_Xoffset, L4_Yoffset, "DB", mirror="Kiri dan Kanan")

    print_hole(2, L5_X, L5_Y, L5_Diameter, L5_QTY, L5_Xoffset, L5_Yoffset, "DB", mirror="Kiri dan Kanan")

    # Lubang tengah DB - sertakan keterangan mirror di dalam blok output juga
    print_hole(3, L6_X, L6_Y, L6_Diameter, L6_QTY, L6_Xoffset, L6_Yoffset, "DB", mirror="Kiri dan Kanan")
    
    print("\n========================")
    print("Program Selesai")
    print("========================")

def handle_amb():
    print("\n=== Program Ambalan Bawah (AMB) ===")
    prompts = [
        {'key': 'panjang', 'prompt': "Masukkan Panjang Kayu (mm): ", 'cast': float},
        {'key': 'lebar', 'prompt': "Masukkan Lebar Kayu (mm): ", 'cast': float},
        {'key': 'kedalaman', 'prompt': "Masukkan Ketebalan Kayu (mm): ", 'cast': float},
    ]
    answers = run_form(prompts)
    if answers is None:
        return
    panjang = answers['panjang']
    lebar = answers['lebar']
    kedalaman = answers['kedalaman']

    Kelipatan = (int(panjang) // 32) * 32 - 64
    XLubang1 = (panjang - Kelipatan) / 2
    YLubang1 = 0
    quantity = [1, 2]

    # Lubang 1
    diameter_lubang1 = 8
    XoffsetLubang1 = Kelipatan
    YoffsetLubang1 = 0
    print_hole(1, XLubang1, YLubang1, diameter_lubang1, quantity[1], XoffsetLubang1, YoffsetLubang1, "AMB")

    # Lubang 2
    XLubang2 = XLubang1 + 64
    YLubang2 = 0
    diameter_lubang2 = 8
    XoffsetLubang2 = XoffsetLubang1 - 128
    YoffsetLubang2 = YoffsetLubang1
    print_hole(2, XLubang2, YLubang2, diameter_lubang2, quantity[1], XoffsetLubang2, YoffsetLubang2, "AMB")

    # Lubang 3
    XLubang3 = XLubang1
    YLubang3 = 25
    diameter_lubang3 = 25
    XoffsetLubang3 = Kelipatan
    YoffsetLubang3 = 0
    print_hole(3, XLubang3, YLubang3, diameter_lubang3, quantity[1], XoffsetLubang3, YoffsetLubang3, "AMB")

    # Lubang 4
    XLubang4 = panjang / 2
    YLubang4 = 0
    diameter_lubang4 = 8
    XoffsetLubang4 = 0
    YoffsetLubang4 = 0
    print_hole(4, XLubang4, YLubang4, diameter_lubang4, quantity[0], XoffsetLubang4, YoffsetLubang4, "AMB")
    
    print("\n========================")
    print("Program Selesai")
    print("========================")

def handle_dski():
    print("\n=== Program Dinding Samping Kiri (DSKI) ===")
    # collect inputs via run_form so 'x' goes back one step
    prompts_basic = [
        {'key': 'panjang', 'prompt': "Masukkan Panjang Kayu (mm): ", 'cast': float},
        {'key': 'lebar', 'prompt': "Masukkan Lebar Kayu (mm): ", 'cast': float},
        {'key': 'tebal', 'prompt': "Masukkan Tebal Kayu (mm): ", 'cast': float},
    ]
    basic = run_form(prompts_basic)
    if basic is None:
        return
    panjang = basic['panjang']
    lebar = basic['lebar']
    tebal = basic['tebal']

    Kelipatan = (int(panjang) // 32) * 32 - 64
    Kelipatan2 = (int(lebar) // 32) * 32 - 64
    quantity = [1, 2]

    def parse_plin_choices(s: str):
        s = s.strip()
        if not s:
            return []
        parts = [p.strip() for p in s.replace(';', ',').replace('/', ',').split(',') if p.strip()]
        try:
            vals = sorted({int(p) for p in parts})
        except ValueError:
            raise ValueError("Gunakan angka 1,2,3 dipisah koma jika memilih lebih dari satu.")
        if not all(c in (1, 2, 3) for c in vals):
            raise ValueError("Pilihan hanya boleh 1, 2, dan/atau 3.")
        return vals

    prompts = [
        {'key': 'has_plin', 'prompt': "Apakah terdapat plin pada meja? [y/n]: ", 'cast': str},
        {'key': 'plin_choices', 'prompt': "Pilih plin yang terdapat pada meja (pisahkan dengan koma, contoh: 1,3) [1=atas,2=depan,3=bawah] : ", 'cast': parse_plin_choices, 'when': lambda a: a.get('has_plin', '').lower() == 'y'},
        {'key': 'Lebar_plin', 'prompt': "Masukkan Lebar Plin (mm) [Berlaku untuk semua plin]: ", 'cast': float, 'when': lambda a: a.get('has_plin', '').lower() == 'y'},
        {'key': 'Tinggi_plinatas', 'prompt': "Masukkan Tinggi Plin Atas (mm): ", 'cast': float, 'when': lambda a: ('plin_choices' in a and 1 in a['plin_choices'])},
        {'key': 'Jumlah_plin_depan', 'prompt': "Berapa jumlah plin depan? (1/2): ", 'cast': int, 'when': lambda a: ('plin_choices' in a and 2 in a['plin_choices'])},
        {'key': 'Tinggi_plindepan', 'prompt': "Masukkan Tinggi Plin Depan 1 (mm): ", 'cast': float, 'when': lambda a: ('plin_choices' in a and 2 in a['plin_choices'])},
        {'key': 'Tinggi_plindepan2', 'prompt': "Masukkan Tinggi Plin Depan 2 (mm): ", 'cast': float, 'when': lambda a: (a.get('Jumlah_plin_depan') == 2)},
        {'key': 'Tinggi_plinbawah', 'prompt': "Masukkan Tinggi Plin Bawah (mm): ", 'cast': float, 'when': lambda a: ('plin_choices' in a and 3 in a['plin_choices'])},
        {'key': 'Tebal_ambalan_bawah', 'prompt': "Masukkan Tebal Ambalan Bawah (mm): ", 'cast': float},
        {'key': 'jarak_lantai', 'prompt': "Masukkan jarak dari lantai ke drawernya (mm): ", 'cast': float},
        {'key': 'pintu_count', 'prompt': "Berapa pintu yang dimiliki drawernya? (2/3): ", 'cast': int},
        {'key': 'Lebar_pintu', 'prompt': "Masukkan Lebar pintu (mm) [Berlaku untuk semua pintu]: ", 'cast': float, 'when': lambda a: ('pintu_count' in a)},
        {'key': 'Tinggi_pintu_1', 'prompt': "Masukkan Tinggi pintu 1 (mm): ", 'cast': float, 'when': lambda a: ('pintu_count' in a and a['pintu_count'] >= 1)},
        {'key': 'Tinggi_pintu_2', 'prompt': "Masukkan Tinggi pintu 2 (mm): ", 'cast': float, 'when': lambda a: ('pintu_count' in a and a['pintu_count'] >= 2)},
        {'key': 'Tinggi_pintu_3', 'prompt': "Masukkan Tinggi pintu 3 (mm): ", 'cast': float, 'when': lambda a: ('pintu_count' in a and a['pintu_count'] >= 3)},
    ]

    while True:
        res = run_form(prompts)
        if res is None:
            return
        pintu_count = res.get('pintu_count')
        if pintu_count not in (2, 3):
            print("Jumlah pintu hanya boleh 2 atau 3. Silakan masukkan ulang.")
            continue
        break

    # map results back to variable names used later in function
    has_plin = res.get('has_plin', '').lower()
    plin_choices = res.get('plin_choices', []) if has_plin == 'y' else []
    if not plin_choices or has_plin != 'y':
        Lebar_plin = 0
        Tinggi_plinatas = 0
        Jumlah_plin_depan = 0
        Tinggi_plindepan = 0
        Tinggi_plindepan2 = 0
        Tinggi_plinbawah = 0
        Tebal_ambalan_bawah = 0
    else:
        Lebar_plin = res.get('Lebar_plin')
        Tinggi_plinatas = res.get('Tinggi_plinatas')
        Jumlah_plin_depan = res.get('Jumlah_plin_depan')
        Tinggi_plindepan = res.get('Tinggi_plindepan')
        Tinggi_plindepan2 = res.get('Tinggi_plindepan2')
        Tinggi_plinbawah = res.get('Tinggi_plinbawah')

    # Gunakan Lebar_plin untuk semua lebar plin
    Lebar_plinatas = Lebar_plin
    Lebar_plindepan = Lebar_plin
    Lebar_plindepan2 = Lebar_plin
    Lebar_plinbawah = Lebar_plin

    Tebal_ambalan_bawah = res.get('Tebal_ambalan_bawah', 0)
    jarak_lantai = res.get('jarak_lantai')
    pintu_count = res.get('pintu_count')
    
    # Gunakan Lebar_pintu untuk semua pintu
    Lebar_pintu = res.get('Lebar_pintu', 0)
    Lebar_pintu_1 = Lebar_pintu
    Lebar_pintu_2 = Lebar_pintu
    Lebar_pintu_3 = Lebar_pintu
    
    # Tinggi pintu tetap individual
    Tinggi_pintu_1 = res.get('Tinggi_pintu_1')
    Tinggi_pintu_2 = res.get('Tinggi_pintu_2')
    Tinggi_pintu_3 = res.get('Tinggi_pintu_3')

    # Tampilkan ringkasan singkat: hanya Panjang x Lebar x Tebal kayu
    print("\n--- Ringkasan dimensi kayu ---")
    try:
        print(f"{panjang} x {lebar} x {tebal} mm (P x L x T)")
    except Exception:
        # Fallback in case variables are missing
        print("Dimensi kayu tidak lengkap.")

    # Collect holes into a list so we can renumber if some are omitted
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

    # Lubang DB 1 (mapped)
    DKI_Lubang4_X = -(76 - jarak_lantai)
    DKI_Lubang4_Y = (lebar - (Kelipatan2 - 32)) / 2
    holes.append({'x': DKI_Lubang4_X, 'y': DKI_Lubang4_Y, 'diameter': 5, 'qty': quantity[1], 'xoffset': 0, 'yoffset': Kelipatan2 - 32})

    # Lubang DB 2 (mapped)
    DKI_Lubang5_X = -(76 - jarak_lantai)
    DKI_Lubang5_Y = DKI_Lubang1_Y + 64
    holes.append({'x': DKI_Lubang5_X, 'y': DKI_Lubang5_Y, 'diameter': 8, 'qty': quantity[1], 'xoffset': 0, 'yoffset': DKI_Lubang1_Yoffset - 128})

    # Lubang DB 3 (mapped from DSKI Lubang 7)
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

    # LUBANG 10 - 12 ADALAH PLIN (tampil hanya jika plin depan dipilih)
    print("\nDEBUG - Nilai variabel plin:")
    print(f"plin_choices: {plin_choices}")
    print(f"Jumlah_plin_depan: {Jumlah_plin_depan}")
    
    if 2 in plin_choices:
        # Lubang 10 plin depan 1a
        DKI_Lubang10_X = Tinggi_pintu_1
        DKI_Lubang10_Y = (tebal / 2) + 1
        holes.append({'x': DKI_Lubang10_X, 'y': DKI_Lubang10_Y, 'diameter': 5, 'qty': quantity[0], 'xoffset': 0, 'yoffset': 0})

        # Lubang 11 plin depan 1b - Different X offset based on Tinggi_plindepan
        if Tinggi_plindepan == 60:
            DKI_Lubang11_X = DKI_Lubang10_X + 32  # Offset for 60mm height
        elif Tinggi_plindepan == 40:
            DKI_Lubang11_X = DKI_Lubang10_X + 20  # Offset for 40mm height
        else:
            DKI_Lubang11_X = DKI_Lubang10_X + 32  # Default to 32mm offset for other heights
        DKI_Lubang11_Y = DKI_Lubang10_Y
        holes.append({'x': DKI_Lubang11_X, 'y': DKI_Lubang11_Y, 'diameter': 8, 'qty': quantity[0], 'xoffset': 0, 'yoffset': 0})

    # Lubang 12 (opsional) plin depan 2
    if 2 in plin_choices and Jumlah_plin_depan == 2:
        DKI_Lubang12_X = (Tinggi_pintu_1 + 20 + Tinggi_pintu_2) + 10
        DKI_Lubang12_Y = (tebal / 2) + 1
        holes.append({'x': DKI_Lubang12_X, 'y': DKI_Lubang12_Y, 'diameter': 8, 'qty': quantity[1], 'xoffset': 20, 'yoffset': 0})

    # LUBANG 13 - 15 ADALAH RAIL
    # Lubang 13 Rail 1
    if Tinggi_plindepan == 60:
        if Tinggi_plinatas is not None:
            DKI_Lubang13_X = Tinggi_pintu_1 - 25 - 7 - Tinggi_plinatas
        else:
            DKI_Lubang13_X = Tinggi_pintu_1 - 25 - 7
    elif Tinggi_plindepan == 40:
        if Tinggi_plinatas is not None:
            DKI_Lubang13_X = Tinggi_pintu_1 - 31 - 7 - Tinggi_plinatas
        else:
            DKI_Lubang13_X = Tinggi_pintu_1 - 31 - 7
    else:
        # Nilai default jika tinggi plin depan bukan 40 atau 60
        DKI_Lubang13_X = Tinggi_pintu_1 - 25 - 7
    DKI_Lubang13_Y = 54
    holes.append({'x': DKI_Lubang13_X, 'y': DKI_Lubang13_Y, 'diameter': 5, 'qty': quantity[1], 'xoffset': 0, 'yoffset': 276, 'label': 'RAIL 1'})

    # Lubang 14 Rail 2
    DKI_Lubang14_X = Tinggi_pintu_1 + 20 + Tinggi_pintu_2 - 9 - 12
    DKI_Lubang14_Y = 54
    holes.append({'x': DKI_Lubang14_X, 'y': DKI_Lubang14_Y, 'diameter': 5, 'qty': quantity[1], 'xoffset': 0, 'yoffset': 276, 'label': 'RAIL 2'})

    # Lubang 15 (hanya jika 3 pintu) Rail 3
    if pintu_count == 3:
        # Calculate X position based on ambalan thickness
        if Tebal_ambalan_bawah == 18:
            DKI_Lubang15_X = DKI_Lubang4_X - 9 - 6 - 21
        else:
            DKI_Lubang15_X = DKI_Lubang4_X - 15 - 6 - 21
        DKI_Lubang15_Y = 54
        holes.append({'x': DKI_Lubang15_X, 'y': DKI_Lubang15_Y, 'diameter': 5, 'qty': quantity[1], 'xoffset': 0, 'yoffset': 288, 'label': 'RAIL 3'})

    # Lubang 16: only if plin bawah (3) is selected and Tinggi_plinbawah is valid
    if 3 in plin_choices and Tinggi_plinbawah is not None:
        L16_X = - ((Tinggi_plinbawah - 32) / 10)
        L16_Y = (tebal / 2) + 1
        L16_Diameter = 5
        L16_QTY = 2
        L16_Xoffset = 32
        L16_Yoffset = 0
        holes.append({'x': L16_X, 'y': L16_Y, 'diameter': L16_Diameter, 'qty': L16_QTY, 'xoffset': L16_Xoffset, 'yoffset': L16_Yoffset})

    # Lubang 19: only if plin atas (1) is selected and Tinggi_plinatas is valid
    if 1 in plin_choices and Tinggi_plinatas is not None:
        # Different X position based on Tinggi_plinatas
        if Tinggi_plinatas == 40:
            L19_X = 10  # Position for 40mm height
        elif Tinggi_plinatas == 60:
            L19_X = 14  # Position for 60mm height
        else:
            L19_X = None
            
        if L19_X is not None:
            L19_Y = (tebal / 2) + 1
            L19_Diameter = 5
            L19_QTY = 2
            L19_Xoffset = 32
            L19_Yoffset = 0
            holes.append({'x': L19_X, 'y': L19_Y, 'diameter': L19_Diameter, 'qty': L19_QTY, 'xoffset': L19_Xoffset, 'yoffset': L19_Yoffset})

    # Map hole indices to their types for output
    hole_types = {
        1: "TOP 1",    # Lubang TOP 1
        2: "TOP 2",    # Lubang TOP 2
        3: "TOP 3",    # Lubang TOP 3
        4: "AMB 1",    # Lubang AMB 1
        5: "AMB 2",    # Lubang AMB 2
        6: "DB 1",     # Lubang DB 1 (sebelumnya DB 3)
        7: "DB 2",     # Lubang DB 2 (sebelumnya DB 1)
        8: "DB 3",     # Lubang DB 3 (sebelumnya DB 2)
        9: "PLIN DEPAN 1a",  # sebelumnya DB 3
        10: "PLIN DEPAN 1b", # sebelumnya PLIN DEPAN 1a
        11: "PLIN DEPAN 2",  # sebelumnya PLIN DEPAN 1b
        12: "PLIN DEPAN 3",  # sebelumnya PLIN DEPAN 2
        13: "RAIL 1",
        14: "RAIL 2",
        15: "RAIL 3",
        16: "PLIN BAWAH",
        17: "PLIN ATAS",
    }
    
    # Print all collected holes in order, renumbering as needed
    for idx, h in enumerate(holes, start=1):
        # prefer explicit label stored on hole if present, else fall back to hole_types mapping
        label = h.get('label') if isinstance(h, dict) else None
        if not label:
            label = hole_types.get(idx, "")
        print_hole(idx, h['x'], h['y'], h['diameter'], h['qty'], h['xoffset'], h['yoffset'], label)
    
    print("\n========================")
    print("Program Selesai")
    print("========================")

def handle_dska():
    print("\n=== Program Dinding Samping Atas (DSKA) ===")
    print("Fungsi untuk DSKA belum diimplementasikan. Jika mau, saya bisa tambahkan logika lubang serupa DSKI/DB.")
    print("\n========================")
    print("Program Selesai")
    print("========================")

def handle_top():
    print("\n=== Program TOP ===")
    prompts = [
        {'key': 'panjang', 'prompt': "Masukkan Panjang Kayu (mm): ", 'cast': float},
        {'key': 'lebar', 'prompt': "Masukkan Lebar Kayu (mm): ", 'cast': float},
        {'key': 'tebal', 'prompt': "Masukkan Tebal Kayu (mm): ", 'cast': float},
        {'key': 'lebar_dski', 'prompt': "Masukkan Lebar DSKI (mm): ", 'cast': float},
        {'key': 'lebar_db', 'prompt': "Masukkan Lebar DB (mm): ", 'cast': float},
        {'key': 'tebal_dski', 'prompt': "Masukkan Tebal DSKI (mm): ", 'cast': float},
        {'key': 'sela', 'prompt': "Masukkan Sela: ", 'cast': float},
    ]
    answers = run_form(prompts)
    if answers is None:
        return
    panjang = answers['panjang']
    lebar = answers['lebar']
    tebal = answers['tebal']
    lebar_dski = answers['lebar_dski']
    lebar_db = answers['lebar_db']
    tebal_dski = answers['tebal_dski']
    sela = answers.get('sela', 100)  # Default 100 jika tidak diinput

    # Hitung Kelipatan jika diperlukan
    Kelipatan = (int(panjang) // 32) * 32 - 64
    Kelipatan2 = (int(lebar) // 32) * 32 - 64
    Kelipatan2_dski = (int(lebar_dski) // 32) * 32 - 64  # Kelipatan untuk DSKI
    quantity = [1, 2]

    holes = []
    # 2 lubang berdasarkan rumus DSKI Lubang 1 (TOP 1), dengan X ditambah sela
    # Rumus DSKI: X = 0, Y = (lebar_dski - (Kelipatan2_dski - 32)) / 2
    top1_x = ((lebar - (lebar_db + (tebal_dski * 2))) / 2) + (tebal_dski / 2)  
    top1_y = ((lebar_dski - (Kelipatan2_dski - 32)) / 2) + sela
    holes.append({'x': top1_x, 'y': top1_y, 'diameter': 5, 'qty': quantity[1], 'xoffset': 0, 'yoffset': 256, 'label': 'Lubang 1'})

    top2_x = top1_x 
    top2_y = top1_y + 64
    holes.append({'x': top2_x, 'y': top2_y, 'diameter': 8, 'qty': quantity[1], 'xoffset': 0, 'yoffset': 128, 'label': 'Lubang 2'})

    # Print holes
    for idx, h in enumerate(holes, start=1):
        label = h.get('label', '')
        print_hole(idx, h['x'], h['y'], h['diameter'], h['qty'], h['xoffset'], h['yoffset'], label)
    
    print("\n========================")
    print("Program Selesai")
    print("========================")

if pilihan_bagian == "DB" or pilihan_bagian == bagian[2]:
    handle_db()
    AUTO_FILL_TEMPLATE = None
elif pilihan_bagian == "DSKA" or pilihan_bagian == bagian[0]:
    handle_dska()
    AUTO_FILL_TEMPLATE = None
elif pilihan_bagian == "AMB" or pilihan_bagian == bagian[4]:
    handle_amb()
    AUTO_FILL_TEMPLATE = None
elif pilihan_bagian == "DSKI" or pilihan_bagian == bagian[1]:
    handle_dski()
    AUTO_FILL_TEMPLATE = None
elif pilihan_bagian == "TOP" or pilihan_bagian == bagian[3]:
    handle_top()
    AUTO_FILL_TEMPLATE = None
else:
    print("Pilihan bagian tidak valid. Silakan jalankan ulang dan pilih salah satu opsi yang tersedia.")

