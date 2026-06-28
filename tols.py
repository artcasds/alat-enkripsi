import os
import sys
import time
import base64
import zlib
import marshal
import re

# Konfigurasi Kode Warna ANSI
R = '\033[1;31m'  # Merah
G = '\033[1;32m'  # Hijau
C = '\033[1;36m'  # Cyan
W = '\033[1;37m'  # Putih
Y = '\033[1;33m'  # Kuning
NC = '\033[0m'    # Reset Warna

# Path folder Download di Android/Termux
DOWNLOAD_DIR = "/sdcard/Download/"

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner():
    clear_screen()
    # Tulisan besar ENCRYPT TOOLS tetap dipertahankan
    print(f"{C}")
    print("  ███████╗███╗   ██╗██████╗ ██████╗ ██╗   ██╗██████╗ ████████╗")
    print("  ██╔════╝████╗  ██║██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝")
    print("  █████╗  ██╔██╗ ██║██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ")
    print("  ██╔══╝  ██║╚██╗██║██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ")
    print("  ███████╗██║ ╚████║╚██████╗██║  ██║   ██║   ██║        ██║   ")
    print("  ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   ")
    print("              ████████╗██████╗ ██████╗ ██╗     ███████╗       ")
    print("              ╚══██╔══╝██╔══██╗██╔══██╗██║     ██╔════╝       ")
    print("                 ██║   ██║  ██║██║  ██║██║     ███████╗       ")
    print("                 ██║   ██║  ██║██║  ██║██║     ╚════██║       ")
    print("                 ██║   ██████╔╝██████╔╝███████╗███████║       ")
    print("                 ╚═╝   ╚═════╝ ╚═════╝ ╚══════╝╚══════╝       ")
    
    # Author ditaruh di atas Info
    print(f"                 {C}AUTHOR: YOGSSS{NC}")
    print(f"{R}[INFO]{W} DONT USE TOOLS FOR ENC MALICIOUS TOOLS{NC}\n")

def get_file_content(prompt_msg):
    while True:
        file_target = input(f"{C}{prompt_msg}: {W}")
        if os.path.exists(file_target):
            with open(file_target, 'r', encoding='utf-8', errors='ignore') as f:
                return file_target, f.read()
        else:
            print(f"{R}[!] File '{file_target}' tidak ditemukan di folder ini! Coba lagi.{NC}")

def save_file(filename, content, is_bytes=False, prefix="enc_"):
    if not os.path.exists(DOWNLOAD_DIR):
        print(f"\n{R}[!] Akses ke folder Download gagal!{NC}")
        print(f"{Y}[*] Pastikan kamu sudah menjalankan perintah: termux-setup-storage{NC}")
        time.sleep(3)
        return

    output_name = prefix + filename
    output_path = os.path.join(DOWNLOAD_DIR, output_name)
    mode = 'wb' if is_bytes else 'w'
    
    try:
        with open(output_path, mode, encoding=None if is_bytes else 'utf-8') as f:
            f.write(content)
        print(f"\n{G}[√] Berhasil! File tersimpan di Download: {Y}{output_name}{NC}")
    except PermissionError:
        print(f"\n{R}[!] Izin ditolak! Kamu belum memberi izin penyimpanan ke Termux.{NC}")
        print(f"{Y}[*] Jalankan perintah: termux-setup-storage{NC}")
    time.sleep(2)

def show_menu():
    while True:
        show_banner()
        print(f"{C}[01] {G}ENCRYPT BASE64 zlib [python]{NC}")
        print(f"{C}[02] {G}ENCRYPT MARSHAL [python]{NC}")
        print(f"{C}[03] {G}DECRYPT BASE64 zlib [python]{NC}")
        print(f"{C}[04] {G}ENC MARSHAL INCLUDE [python]{NC}")
        print(f"{C}[05] {G}JAVASCRIPT ENCRYPT [javascript]{NC}")
        print(f"{C}[06] {G}BASH ENCRYPT [bash only]{NC}")
        print(f"{C}[07] {G}XOR ENCRYPT [python only]{NC}")
        print(f"{C}[08] {G}HTML ENCODE{NC}")
        print(f"{C}[09] {G}OBFUSCATE EYE{NC}")
        print(f"{C}[10] {G}EXIT{NC}\n")

        try:
            # Menggunakan teks prompt yang baru
            pilihan = input(f"{C}PILIH SESUAI KEBUTUHAN: {W}").strip()
            
            # [01] ENCRYPT BASE64 zlib
            if pilihan in ['01', '1']:
                print(f"\n{Y}[*] Memproses Base64 Zlib Encryption...{NC}")
                fname, source = get_file_content("Masukkan nama file Python")
                compressed = zlib.compress(source.encode('utf-8'))
                encoded = base64.b64encode(compressed).decode('utf-8')
                payload = f"import zlib,base64\nexec(zlib.decompress(base64.b64decode('{encoded}')).decode('utf-8'))"
                save_file(fname, payload)

            # [02] ENCRYPT MARSHAL
            elif pilihan in ['02', '2']:
                print(f"\n{Y}[*] Memproses Marshal Encryption...{NC}")
                fname, source = get_file_content("Masukkan nama file Python")
                try:
                    compiled = compile(source, '', 'exec')
                    marshaled = marshal.dumps(compiled)
                    payload = f"import marshal\nexec(marshal.loads({repr(marshaled)}))"
                    save_file(fname, payload)
                except Exception as e:
                    print(f"{R}[!] Gagal compile script: {e}{NC}"); time.sleep(2)

            # [03] DECRYPT BASE64 zlib
            elif pilihan in ['03', '3']:
                print(f"\n{Y}[*] Memproses Decrypt Base64 Zlib...{NC}")
                fname, source = get_file_content("Masukkan nama file terenkripsi (Menu 01)")
                match = re.search(r"b64decode\(['\"](.*?)['\"]\)", source)
                if match:
                    try:
                        b64_str = match.group(1)
                        decoded = zlib.decompress(base64.b64decode(b64_str)).decode('utf-8')
                        save_file(fname, decoded, prefix="dec_")
                    except Exception:
                        print(f"{R}[!] Gagal mendecrypt. Format file rusak atau salah.{NC}"); time.sleep(2)
                else:
                    print(f"{R}[!] Pola enkripsi Base64/Zlib tidak ditemukan dalam file.{NC}"); time.sleep(2)

            # [04] ENC MARSHAL INCLUDE
            elif pilihan in ['04', '4']:
                print(f"\n{Y}[*] Memproses Marshal Include (Multi-Layer)...{NC}")
                fname, source = get_file_content("Masukkan nama file Python")
                try:
                    compiled = compile(source, '', 'exec')
                    marshaled = marshal.dumps(compiled)
                    compressed = zlib.compress(marshaled)
                    encoded = base64.b64encode(compressed).decode('utf-8')
                    payload = f"import marshal,zlib,base64\nexec(marshal.loads(zlib.decompress(base64.b64decode('{encoded}'))))"
                    save_file(fname, payload)
                except Exception as e:
                    print(f"{R}[!] Gagal memproses: {e}{NC}"); time.sleep(2)

            # [05] JAVASCRIPT ENCRYPT
            elif pilihan in ['05', '5']:
                print(f"\n{Y}[*] Memproses JavaScript Encryption...{NC}")
                fname, source = get_file_content("Masukkan nama file JS (misal: script.js)")
                char_codes = [str(ord(c)) for c in source]
                encoded = ",".join(char_codes)
                payload = f"eval(String.fromCharCode({encoded}))"
                save_file(fname, payload)

            # [06] BASH ENCRYPT
            elif pilihan in ['06', '6']:
                print(f"\n{Y}[*] Memproses Bash Encryption...{NC}")
                fname, source = get_file_content("Masukkan nama file Bash (misal: script.sh)")
                encoded = base64.b64encode(source.encode('utf-8')).decode('utf-8')
                payload = f"eval \"$(echo '{encoded}' | base64 -d)\""
                save_file(fname, payload)

            # [07] XOR ENCRYPT
            elif pilihan in ['07', '7']:
                print(f"\n{Y}[*] Memproses XOR Encryption...{NC}")
                fname, source = get_file_content("Masukkan nama file Python")
                key_input = input(f"{C}Masukkan kunci angka (1-255): {W}")
                key = int(key_input) if key_input.isdigit() else 155
                xor_bytes = [ord(c) ^ key for c in source]
                payload = f"key = {key}\ndata = {str(xor_bytes)}\nexec(''.join([chr(b ^ key) for b in data]))"
                save_file(fname, payload)

            # [08] HTML ENCODE
            elif pilihan in ['08', '8']:
                print(f"\n{Y}[*] Memproses HTML Encode...{NC}")
                fname, source = get_file_content("Masukkan nama file HTML (misal: index.html)")
                encoded = "".join([f"&#{ord(c)};" for c in source])
                save_file(fname, encoded)

            # [09] OBFUSCATE EYE
            elif pilihan in ['09', '9']:
                print(f"\n{Y}[*] Memproses Obfuscate Eye...{NC}")
                fname, source = get_file_content("Masukkan nama file Python")
                hex_data = source.encode('utf-8').hex()
                b64_data = base64.b64encode(hex_data.encode('utf-8')).decode('utf-8')
                payload = f"import base64\nexec(bytes.fromhex(base64.b64decode('{b64_data}').decode('utf-8')).decode('utf-8'))"
                save_file(fname, payload)

            # [13] EXIT
            elif pilihan == '10':
                print(f"\n{G}[!] Keluar dari program. Terima kasih!{NC}")
                sys.exit()

            else:
                print(f"\n{R}[!] Pilihan tidak valid!{NC}")
                time.sleep(1.5)

        except KeyboardInterrupt:
            print(f"\n\n{R}[!] Program dihentikan paksa.{NC}")
            sys.exit()

if __name__ == "__main__":
    show_menu()

