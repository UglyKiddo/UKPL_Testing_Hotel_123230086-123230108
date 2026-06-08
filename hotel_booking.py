"""
HOTEL NUSANTARA - BOOKING SYSTEM v2.0
Role:
- Admin   : Lihat Daftar Kamar, Laporan Booking, Laporan Kamar
- Customer: Lihat Daftar Kamar, Booking Kamar, Checkout/Riwayat Booking
"""

import os
import datetime

USERS = {
    "admin": "admin123",
    "budi": "budi456",
    "sari": "sari789",
}

rooms = {
    "1": {"tipe": "Standard", "harga": 300_000, "kapasitas": 2, "stok": 5, "fasilitas": "AC, TV, WiFi"},
    "2": {"tipe": "Deluxe", "harga": 600_000, "kapasitas": 3, "stok": 3, "fasilitas": "AC, TV 42, WiFi, Bathtub, Minibar"},
    "3": {"tipe": "Suite", "harga": 1_200_000, "kapasitas": 4, "stok": 2, "fasilitas": "AC, TV 55, WiFi, Jacuzzi, Minibar, Ruang Tamu"},
}

booking_history = []
booking_counter = 1

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def garis(char="═", panjang=62):
    print(char * panjang)

def header(judul):
    clear_screen()
    garis()
    print(f"🏨 HOTEL NUSANTARA | {judul}")
    garis()
    print()

def tekan_enter():
    input("\nTekan ENTER untuk melanjutkan...")

def format_rupiah(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

def is_admin(username):
    return username.lower() == "admin"

def input_angka(prompt, min_val=None, max_val=None):
    while True:
        try:
            nilai = int(input(prompt))
            if min_val is not None and nilai < min_val:
                print("Nilai terlalu kecil.")
                continue
            if max_val is not None and nilai > max_val:
                print("Nilai terlalu besar.")
                continue
            return nilai
        except ValueError:
            print("Masukkan angka yang valid.")

def input_pilihan_menu(prompt, pilihan_valid):
    while True:
        x = input(prompt).strip()
        if x in pilihan_valid:
            return x
        print("Pilihan tidak valid.")

def login():
    attempts = 0
    while attempts < 3:
        header("LOGIN")
        username = input("Username : ").strip()
        password = input("Password : ").strip()

        if username in USERS and USERS[username] == password:
            print("Login berhasil.")
            tekan_enter()
            return username

        attempts += 1
        print("Login gagal.")
        tekan_enter()

    print("Terlalu banyak percobaan.")
    raise SystemExit

def lihat_daftar_kamar():
    header("DAFTAR KAMAR")
    for kode, kamar in rooms.items():
        print(f"[{kode}] {kamar['tipe']}")
        print(f" Harga      : {format_rupiah(kamar['harga'])}")
        print(f" Kapasitas  : {kamar['kapasitas']}")
        print(f" Stok       : {kamar['stok']}")
        print(f" Fasilitas  : {kamar['fasilitas']}")
        print("-"*40)
    tekan_enter()

def booking_kamar(username):
    global booking_counter

    header("BOOKING KAMAR")
    for kode, kamar in rooms.items():
        print(f"[{kode}] {kamar['tipe']} ({kamar['stok']} tersedia)")

    pilihan = input_pilihan_menu("Pilih kamar: ", ["1","2","3"])
    kamar = rooms[pilihan]

    if kamar["stok"] <= 0:
        print("Kamar habis.")
        tekan_enter()
        return

    malam = input_angka("Jumlah malam: ",1,30)
    tamu = input_angka("Jumlah tamu: ",1,kamar["kapasitas"])

    total = kamar["harga"] * malam

    lanjut = input_pilihan_menu("Lanjut pembayaran? (y/n): ",["y","n","Y","N"])
    if lanjut.lower() == "n":
        return

    while True:
        bayar = input_angka("Nominal bayar: ",1)
        if bayar >= total:
            break
        print("Pembayaran kurang.")

    kamar["stok"] -= 1

    booking_history.append({
        "kode": f"HTL-{booking_counter:04d}",
        "username": username,
        "tipe": kamar["tipe"],
        "malam": malam,
        "tamu": tamu,
        "total": total,
        "bayar": bayar,
        "kembalian": bayar-total,
        "status": "Aktif",
        "check_in": str(datetime.date.today()),
        "check_out": str(datetime.date.today()+datetime.timedelta(days=malam))
    })

    booking_counter += 1

    print("Booking berhasil.")
    tekan_enter()

def checkout(username):
    header("CHECKOUT")

    my = [b for b in booking_history if b["username"] == username]

    if not my:
        print("Belum ada booking.")
        tekan_enter()
        return

    for i,b in enumerate(my,1):
        print(f"{i}. {b['kode']} | {b['tipe']} | {b['status']}")

    pilihan = input_pilihan_menu("Pilih nomor / 0 kembali: ",
                                 [str(i) for i in range(len(my)+1)])

    if pilihan == "0":
        return

    booking = my[int(pilihan)-1]

    if booking["status"] == "Aktif":
        konfirmasi = input_pilihan_menu(
            "Checkout sekarang? (y/n): ",
            ["y","n","Y","N"]
        )

        if konfirmasi.lower() == "y":
            booking["status"] = "Selesai"

            for kamar in rooms.values():
                if kamar["tipe"] == booking["tipe"]:
                    kamar["stok"] += 1
                    break

            print("Checkout berhasil.")

    tekan_enter()

def laporan_booking():
    header("LAPORAN BOOKING")

    if not booking_history:
        print("Belum ada data booking.")
    else:
        for b in booking_history:
            print(
                f"{b['kode']} | "
                f"{b['username']} | "
                f"{b['tipe']} | "
                f"{format_rupiah(b['total'])} | "
                f"{b['status']}"
            )

    tekan_enter()

def harga_kamar():
    header("Harga KAMAR")

    for kamar in rooms.values():
        print(
            f"{kamar['tipe']} | "
            f"Stok: {kamar['stok']} | "
            f"Harga: {format_rupiah(kamar['harga'])}"
        )

    tekan_enter()

def menu_customer(username):
    while True:
        header(f"MENU CUSTOMER - {username}")
        print("[1] Lihat Daftar Kamar")
        print("[2] Booking Kamar")
        print("[3] Checkout / Riwayat Booking")
        print("[0] Logout")

        p = input_pilihan_menu("Pilihan: ",["0","1","2","3"])

        if p == "1":
            lihat_daftar_kamar()
        elif p == "2":
            booking_kamar(username)
        elif p == "3":
            checkout(username)
        else:
            break

def menu_admin(username):
    while True:
        header(f"MENU ADMIN - {username}")
        print("[1] Lihat Daftar Kamar")
        print("[2] Laporan Booking")
        print("[3] Harga Kamar")
        print("[0] Logout")

        p = input_pilihan_menu("Pilihan: ",["0","1","2","3"])

        if p == "1":
            lihat_daftar_kamar()
        elif p == "2":
            laporan_booking()
        elif p == "3":
            harga_kamar()
        else:
            break

def main():
    while True:
        user = login()

        if is_admin(user):
            menu_admin(user)
        else:
            menu_customer(user)

        lagi = input_pilihan_menu(
            "Login lagi? (y/n): ",
            ["y","n","Y","N"]
        )

        if lagi.lower() == "n":
            break

if __name__ == "__main__":
    main()
