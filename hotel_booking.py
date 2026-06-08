import os
import datetime

USERS = {
    "budi":  "budi123",
    "sari":  "sari789",
    "andi":  "andi321",
}

rooms = {
    "1": {
        "tipe":      "Standard",
        "harga":     300_000,
        "kapasitas": 2,
        "stok":      5,
        "fasilitas": "AC, TV, WiFi",
    },
    "2": {
        "tipe":      "Deluxe",
        "harga":     600_000,
        "kapasitas": 3,
        "stok":      3,
        "fasilitas": 'AC, TV 42", WiFi, Bathtub, Minibar',
    },
    "3": {
        "tipe":      "Suite",
        "harga":     1_200_000,
        "kapasitas": 4,
        "stok":      2,
        "fasilitas": 'AC, TV 55", WiFi, Jacuzzi, Minibar, Ruang Tamu',
    },
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
    print(f"  HOTEL NUSANTARA  │  {judul}")
    garis()
    print()


def tekan_enter():
    print()
    input("  Tekan [ENTER] untuk melanjutkan...")


def format_rupiah(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")


def input_angka(prompt, min_val=None, max_val=None):
    while True:
        try:
            raw = input(prompt).strip()
            if raw == "":
                print("  Input tidak boleh kosong.\n")
                continue
            nilai = int(raw)
            if min_val is not None and nilai < min_val:
                print(f"  Nilai minimum adalah {min_val}.\n")
                continue
            if max_val is not None and nilai > max_val:
                print(f"  Nilai maksimum adalah {max_val}.\n")
                continue
            return nilai
        except ValueError:
            print("  Masukkan angka yang valid.\n")


def input_pilihan_menu(prompt, pilihan_valid):
    while True:
        raw = input(prompt).strip()
        if raw == "":
            print("  Input tidak boleh kosong.\n")
            continue
        if raw not in pilihan_valid:
            print(f"  Pilihan tidak tersedia. Masukkan: {', '.join(pilihan_valid)}\n")
            continue
        return raw


def login():
    header("LOGIN")
    print("  Masukkan username dan password Anda.\n")
    garis("─")
    print()

    attempts = 0

    while attempts < 3:
        username = input("  Username : ").strip()
        if username == "":
            print("Username tidak boleh kosong.\n")
            continue

        password = input("  Password : ").strip()
        if password == "":
            print("Password tidak boleh kosong.\n")
            continue

        if username in USERS and USERS[username] == password:
            print()
            print(f"Selamat datang, {username.capitalize()}!")
            tekan_enter()
            return username

        attempts += 1
        sisa = 3 - attempts
        print(f"\n  Username atau password salah. Sisa percobaan: {sisa}\n")

    print("\n  Terlalu banyak percobaan gagal. Program dihentikan.")
    exit()


def lihat_daftar_kamar():
    header("DAFTAR KAMAR")

    for kode, kamar in rooms.items():
        status = "TERSEDIA" if kamar["stok"] > 0 else "❌ HABIS"
        print(f"  [{kode}] {kamar['tipe']}")
        garis("─", 50)
        print(f"      Harga       : {format_rupiah(kamar['harga'])} / malam")
        print(f"      Kapasitas   : {kamar['kapasitas']} tamu")
        print(f"      Stok        : {kamar['stok']} kamar  ({status})")
        print(f"      Fasilitas   : {kamar['fasilitas']}")
        print()

    tekan_enter()


def booking_kamar(username):
    global booking_counter
    header("BOOKING KAMAR")

    print("  Pilih tipe kamar:\n")
    for kode, kamar in rooms.items():
        stok_info = f"({kamar['stok']} tersisa)" if kamar["stok"] > 0 else "(HABIS)"
        print(f"    [{kode}] {kamar['tipe']:10s}  {format_rupiah(kamar['harga'])}/malam  {stok_info}")
    print()

    pilihan = input_pilihan_menu("  Pilihan kamar [1/2/3] : ", ["1", "2", "3"])
    kamar = rooms[pilihan]

    if kamar["stok"] == 0:
        print(f"\n  Maaf, kamar {kamar['tipe']} sedang tidak tersedia.\n")
        tekan_enter()
        return

    print(f"\n  Kamar dipilih: {kamar['tipe']} — {format_rupiah(kamar['harga'])}/malam\n")

    malam = input_angka("  Jumlah malam menginap : ", min_val=1, max_val=30)
    tamu  = input_angka(
        f"  Jumlah tamu (maks {kamar['kapasitas']}) : ",
        min_val=1,
        max_val=kamar["kapasitas"],
    )

    total          = kamar["harga"] * malam
    tanggal_masuk  = datetime.date.today()
    tanggal_keluar = tanggal_masuk + datetime.timedelta(days=malam)

    print()
    garis("─", 50)
    print("  RINGKASAN PEMESANAN")
    garis("─", 50)
    print(f"  Tipe kamar     : {kamar['tipe']}")
    print(f"  Check-in       : {tanggal_masuk}")
    print(f"  Check-out      : {tanggal_keluar}")
    print(f"  Jumlah malam   : {malam} malam")
    print(f"  Jumlah tamu    : {tamu} orang")
    print(f"  Harga/malam    : {format_rupiah(kamar['harga'])}")
    print(f"  Total biaya    : {format_rupiah(total)}")
    garis("─", 50)
    print()

    konfirmasi = input_pilihan_menu(
        "  Lanjutkan ke pembayaran? [y/n] : ", ["y", "Y", "n", "N"]
    )

    if konfirmasi.lower() == "n":
        print("\n  ℹ  Pemesanan dibatalkan.\n")
        tekan_enter()
        return

    print()
    print("  ── PEMBAYARAN ──────────────────────────────")
    print(f"  Total yang harus dibayar: {format_rupiah(total)}")
    print()

    while True:
        bayar = input_angka("  Masukkan nominal pembayaran (Rp) : ", min_val=1)
        if bayar < total:
            kurang = total - bayar
            print(f"\n Pembayaran kurang {format_rupiah(kurang)}. Coba lagi.\n")
        else:
            break

    kembalian = bayar - total
    rooms[pilihan]["stok"] -= 1

    kode_booking = f"HTL-{booking_counter:04d}"
    booking_counter += 1

    booking_history.append({
        "kode":      kode_booking,
        "username":  username,
        "tipe":      kamar["tipe"],
        "check_in":  str(tanggal_masuk),
        "check_out": str(tanggal_keluar),
        "malam":     malam,
        "tamu":      tamu,
        "total":     total,
        "bayar":     bayar,
        "kembalian": kembalian,
        "status":    "Aktif",
    })

    print()
    garis("═")
    print("                  PEMBAYARAN BERHASIL")
    garis("═")
    print(f"  No. Booking    : {kode_booking}")
    print(f"  Nama Tamu      : {username.capitalize()}")
    print(f"  Tipe Kamar     : {kamar['tipe']}")
    print(f"  Fasilitas      : {kamar['fasilitas']}")
    print(f"  Check-in       : {tanggal_masuk}")
    print(f"  Check-out      : {tanggal_keluar}")
    print(f"  Durasi         : {malam} malam")
    print(f"  Jumlah Tamu    : {tamu} orang")
    garis("─", 62)
    print(f"  Subtotal       : {format_rupiah(total)}")
    print(f"  Dibayar        : {format_rupiah(bayar)}")
    print(f"  Kembalian      : {format_rupiah(kembalian)}")
    garis("═")
    print("        Terima kasih telah memilih Hotel Nusantara!")
    garis("═")

    tekan_enter()


def checkout(username):
    header("CHECKOUT & RIWAYAT BOOKING")

    my_bookings = [b for b in booking_history if b["username"] == username]

    if not my_bookings:
        print("  ℹ  Anda belum memiliki riwayat pemesanan.\n")
        tekan_enter()
        return

    print(f"  Booking atas nama: {username.capitalize()}\n")
    garis("─", 62)
    print(f"  {'No':>3}  {'Kode Booking':15s}  {'Tipe':10s}  {'Check-in':12s}  {'Status':8s}")
    garis("─", 62)

    for idx, b in enumerate(my_bookings, start=1):
        print(f"  {idx:>3}  {b['kode']:15s}  {b['tipe']:10s}  {b['check_in']:12s}  {b['status']}")

    print()
    pilihan_str = [str(i) for i in range(1, len(my_bookings) + 1)] + ["0"]

    print("  Pilih nomor untuk melihat detail / checkout.")
    print("  [0] Kembali ke menu utama\n")

    nomor = input_pilihan_menu(f"  Pilihan [0-{len(my_bookings)}] : ", pilihan_str)

    if nomor == "0":
        return

    booking = my_bookings[int(nomor) - 1]

    print()
    garis("═")
    print("                  DETAIL BOOKING")
    garis("═")
    print(f"  No. Booking    : {booking['kode']}")
    print(f"  Nama Tamu      : {booking['username'].capitalize()}")
    print(f"  Tipe Kamar     : {booking['tipe']}")
    print(f"  Check-in       : {booking['check_in']}")
    print(f"  Check-out      : {booking['check_out']}")
    print(f"  Durasi         : {booking['malam']} malam")
    print(f"  Jumlah Tamu    : {booking['tamu']} orang")
    print(f"  Total Biaya    : {format_rupiah(booking['total'])}")
    print(f"  Dibayar        : {format_rupiah(booking['bayar'])}")
    print(f"  Kembalian      : {format_rupiah(booking['kembalian'])}")
    print(f"  Status         : {booking['status']}")
    garis("═")

    if booking["status"] == "Aktif":
        print()
        aksi = input_pilihan_menu(
            "  Lakukan checkout sekarang? [y/n] : ", ["y", "Y", "n", "N"]
        )
        if aksi.lower() == "y":
            booking["status"] = "Selesai"
            for kode, kamar in rooms.items():
                if kamar["tipe"] == booking["tipe"]:
                    rooms[kode]["stok"] += 1
                    break
            print("\n  Checkout berhasil! Terima kasih, sampai jumpa lagi. 👋\n")
    else:
        print("\n  ℹ  Booking ini sudah selesai.\n")

    tekan_enter()


def menu_utama(username):
    while True:
        header(f"MENU UTAMA  │  {username.capitalize()}")
        print("    [1]  Lihat Daftar Kamar")
        print("    [2]  Booking Kamar")
        print("    [3]  Checkout / Riwayat Booking")
        print("    [0]  Logout")
        print()
        garis("─")

        pilihan = input_pilihan_menu("\n  Pilihan menu [0/1/2/3] : ", ["0", "1", "2", "3"])

        if pilihan == "1":
            lihat_daftar_kamar()
        elif pilihan == "2":
            booking_kamar(username)
        elif pilihan == "3":
            checkout(username)
        elif pilihan == "0":
            header("LOGOUT")
            print(f"  Sampai jumpa, {username.capitalize()}! 👋\n")
            break


def main():
    while True:
        user = login()
        menu_utama(user)

        clear_screen()
        garis()
        print("  Login dengan akun lain?")
        garis("─")
        lagi = input_pilihan_menu("\n  [y] Login lagi  |  [n] Keluar  → ", ["y", "Y", "n", "N"])
        if lagi.lower() == "n":
            clear_screen()
            garis()
            print("  Terima kasih telah menggunakan Hotel Nusantara Booking System.")
            print("  © 2025 Hotel Nusantara. All rights reserved.")
            garis()
            print()
            break


if __name__ == "__main__":
    main()