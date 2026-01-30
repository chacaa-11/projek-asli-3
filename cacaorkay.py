from datetime import datetime
"""
Program To-Do List - Aplikasi manajemen tugas dengan antarmuka berbasis terminal
Modul ini menyediakan fungsi-fungsi untuk mengelola daftar tugas (to-do list) dengan
fitur-fitur lengkap seperti menambah, mengedit, menghapus, dan memfilter tugas.
Fungsi-fungsi utama:
- load_data(): Memuat data tugas dari file penyimpanan
- save_data(data): Menyimpan data tugas ke file
- display_tasks(data): Menampilkan semua tugas dalam format tabel
- add_task(data): Menambahkan tugas baru dengan deskripsi detail yang ditampilkan
- mark_complete(data): Mengubah status tugas antara selesai dan belum selesai
- edit_task(data): Mengedit nama, deskripsi, atau jenis tugas yang ada
- delete_task(data): Menghapus tugas dengan konfirmasi pengguna
- view_task_details(data): Menampilkan detail lengkap sebuah tugas
- show_statistics(data): Menampilkan statistik kemajuan tugas
- filter_by_jenis(data): Memfilter dan menampilkan tugas berdasarkan jenis
- main_menu(): Menampilkan menu utama dan mengontrol alur program
Struktur data tugas:
- kegiatan: Nama/judul tugas
- jenis: Kategori tugas (Kegiatan, Acara, Lainnya)
- deskripsi: Penjelasan detail mengenai tugas
- selesai: Status penyelesaian tugas (Boolean)
- tanggal: Waktu pembuatan tugas dalam format DD-MM-YYYY HH:MM
Format penyimpanan file: kegiatan|jenis|deskripsi|status|tanggal
"""

DATA_FILE = "todo_data.txt"

def load_data():
    """Memuat data dari file"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = []
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split('|')
                    if len(parts) >= 5:
                        data.append({
                            'kegiatan': parts[0],
                            'jenis': parts[1],
                            'deskripsi': parts[2],
                            'selesai': parts[3] == 'Selesai',
                            'tanggal': parts[4]
                        })
            return data
    except FileNotFoundError:
        return []

def save_data(data):
    """Menyimpan data ke file"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        for task in data:
            status = 'Selesai' if task['selesai'] else 'Belum'
            line = f"{task['kegiatan']}|{task['jenis']}|{task['deskripsi']}|{status}|{task['tanggal']}\n"
            f.write(line)
    print("✓ Data berhasil disimpan!\n")

def display_tasks(data):
    """Menampilkan semua tugas"""
    if not data:
        print("\n📭 Daftar tugas kosong!\n")
        return
    
    print("\n" + "="*90)
    print(f"{'No':<4} {'Status':<10} {'Jenis':<10} {'Kegiatan':<30} {'Tanggal':<15}")
    print("="*90)
    
    for idx, task in enumerate(data, 1):
        status = "✓ Selesai" if task['selesai'] else "⏳ Belum"
        jenis = task['jenis']
        kegiatan = task['kegiatan'][:27] + "..." if len(task['kegiatan']) > 27 else task['kegiatan']
        tanggal = task['tanggal']
        
        print(f"{idx:<4} {status:<10} {jenis:<10} {kegiatan:<30} {tanggal:<15}")
    
    print("="*90 + "\n")

def add_task(data):
    """Menambah tugas baru"""
    print("\n--- Tambah Tugas Baru ---")
    
    print("\nPilih jenis tugas:")
    print("1. Kegiatan")
    print("2. Acara")
    print("3. Lainnya")
    jenis_input = input("Masukkan pilihan (1-3): ").strip()
    
    jenis_map = {'1': 'Kegiatan', '2': 'Acara', '3': 'Lainnya'}
    jenis = jenis_map.get(jenis_input, 'Kegiatan')
    
    kegiatan = input(f"Masukkan nama {jenis.lower()}: ").strip()
    if not kegiatan:
        print("❌ Nama tidak boleh kosong!\n")
        return
    
    deskripsi = input("Masukkan deskripsi (opsional): ").strip()
    
    task = {
        'kegiatan': kegiatan,
        'jenis': jenis,
        'deskripsi': deskripsi,
        'selesai': False,
        'tanggal': datetime.now().strftime("%d-%m-%Y %H:%M")
    }
    
    data.append(task)
    save_data(data)
    print(f"✓ Tugas '{kegiatan}' berhasil ditambahkan!\n")

def mark_complete(data):
    """Tandai tugas sebagai selesai/belum selesai"""
    display_tasks(data)
    
    if not data:
        return
    
    try:
        no = int(input("Masukkan nomor tugas untuk mengubah status: ").strip())
        if 1 <= no <= len(data):
            task = data[no - 1]
            task['selesai'] = not task['selesai']
            status_baru = "Selesai" if task['selesai'] else "Belum Selesai"
            save_data(data)
            print(f"✓ Status '{task['kegiatan']}' diubah menjadi {status_baru}!\n")
        else:
            print("❌ Nomor tidak valid!\n")
    except ValueError:
        print("❌ Masukkan angka yang valid!\n")

def edit_task(data):
    """Edit tugas yang sudah ada"""
    display_tasks(data)
    
    if not data:
        return
    
    try:
        no = int(input("Masukkan nomor tugas untuk diedit: ").strip())
        if 1 <= no <= len(data):
            task = data[no - 1]
            
            print(f"\nMengedit: {task['kegiatan']}")
            print("1. Edit nama")
            print("2. Edit deskripsi")
            print("3. Edit jenis")
            print("0. Batal")
            
            pilihan = input("Pilih opsi: ").strip()
            
            if pilihan == '1':
                nama_baru = input("Masukkan nama baru: ").strip()
                if nama_baru:
                    task['kegiatan'] = nama_baru
                    save_data(data)
                    print(f"✓ Nama tugas berhasil diubah!\n")
                    
            elif pilihan == '2':
                deskripsi_baru = input("Masukkan deskripsi baru: ").strip()
                task['deskripsi'] = deskripsi_baru
                save_data(data)
                print(f"✓ Deskripsi tugas berhasil diubah!\n")
                
            elif pilihan == '3':
                print("Pilih jenis baru:")
                print("1. Kegiatan")
                print("2. Acara")
                print("3. Lainnya")
                jenis_input = input("Masukkan pilihan (1-3): ").strip()
                jenis_map = {'1': 'Kegiatan', '2': 'Acara', '3': 'Lainnya'}
                if jenis_input in jenis_map:
                    task['jenis'] = jenis_map[jenis_input]
                    save_data(data)
                    print(f"✓ Jenis tugas berhasil diubah!\n")
                else:
                    print("❌ Pilihan tidak valid!\n")
            else:
                print("Dibatalkan.\n")
        else:
            print("❌ Nomor tidak valid!\n")
    except ValueError:
        print("❌ Masukkan angka yang valid!\n")

def delete_task(data):
    """Hapus tugas"""
    display_tasks(data)
    
    if not data:
        return
    
    try:
        no = int(input("Masukkan nomor tugas untuk dihapus: ").strip())
        if 1 <= no <= len(data):
            task = data[no - 1]
            konfirmasi = input(f"Yakin hapus '{task['kegiatan']}'? (y/n): ").strip().lower()
            if konfirmasi == 'y':
                data.pop(no - 1)
                save_data(data)
                print(f"✓ Tugas berhasil dihapus!\n")
            else:
                print("Dibatalkan.\n")
        else:
            print("❌ Nomor tidak valid!\n")
    except ValueError:
        print("❌ Masukkan angka yang valid!\n")

def view_task_details(data):
    """Lihat detail tugas"""
    display_tasks(data)
    
    if not data:
        return
    
    try:
        no = int(input("Masukkan nomor tugas untuk melihat detail: ").strip())
        if 1 <= no <= len(data):
            task = data[no - 1]
            print("\n" + "="*50)
            print(f"Nama       : {task['kegiatan']}")
            print(f"Jenis      : {task['jenis']}")
            print(f"Deskripsi  : {task['deskripsi'] if task['deskripsi'] else '-'}")
            print(f"Status     : {'✓ Selesai' if task['selesai'] else '⏳ Belum Selesai'}")
            print(f"Tanggal    : {task['tanggal']}")
            print("="*50 + "\n")
        else:
            print("❌ Nomor tidak valid!\n")
    except ValueError:
        print("❌ Masukkan angka yang valid!\n")

def show_statistics(data):
    """Tampilkan statistik tugas"""
    if not data:
        print("\n📭 Tidak ada tugas!\n")
        return
    
    total = len(data)
    selesai = sum(1 for task in data if task['selesai'])
    belum = total - selesai
    
    print("\n" + "="*50)
    print("📊 STATISTIK TUGAS")
    print("="*50)
    print(f"Total Tugas    : {total}")
    print(f"Selesai        : {selesai} (✓)")
    print(f"Belum Selesai  : {belum} (⏳)")
    if total > 0:
        print(f"Progress       : {(selesai/total)*100:.1f}%")
    print("="*50 + "\n")

def filter_by_jenis(data):
    """Filter tugas berdasarkan jenis"""
    jenis_list = list(set(task['jenis'] for task in data))
    
    if not jenis_list:
        print("\n📭 Tidak ada tugas!\n")
        return
    
    print("\nJenis yang tersedia:")
    for idx, jenis in enumerate(jenis_list, 1):
        print(f"{idx}. {jenis}")
    
    try:
        pilihan = int(input("Pilih jenis (nomor): ").strip())
        if 1 <= pilihan <= len(jenis_list):
            jenis_terpilih = jenis_list[pilihan - 1]
            filtered = [task for task in data if task['jenis'] == jenis_terpilih]
            
            print(f"\n--- Tugas dengan jenis: {jenis_terpilih} ---")
            if filtered:
                print("\n" + "="*90)
                print(f"{'No':<4} {'Status':<10} {'Kegiatan':<40} {'Tanggal':<15}")
                print("="*90)
                for idx, task in enumerate(filtered, 1):
                    status = "✓ Selesai" if task['selesai'] else "⏳ Belum"
                    kegiatan = task['kegiatan'][:37] + "..." if len(task['kegiatan']) > 37 else task['kegiatan']
                    print(f"{idx:<4} {status:<10} {kegiatan:<40} {task['tanggal']:<15}")
                print("="*90 + "\n")
        else:
            print("❌ Pilihan tidak valid!\n")
    except ValueError:
        print("❌ Masukkan angka yang valid!\n")

def main_menu():
    """Menu utama program"""
    while True:
        print("\n" + "="*50)
        print("📝 PROGRAM TO-DO LIST")
        print("="*50)
        print("1. Lihat semua tugas")
        print("2. Tambah tugas baru")
        print("3. Tandai tugas selesai/belum")
        print("4. Edit tugas")
        print("5. Hapus tugas")
        print("6. Lihat detail tugas")
        print("7. Filter berdasarkan jenis")
        print("8. Lihat statistik")
        print("0. Keluar")
        print("="*50)
        
        pilihan = input("Masukkan pilihan (0-8): ").strip()
        data = load_data()
        
        if pilihan == '1':
            display_tasks(data)
        elif pilihan == '2':
            add_task(data)
        elif pilihan == '3':
            mark_complete(data)
        elif pilihan == '4':
            edit_task(data)
        elif pilihan == '5':
            delete_task(data)
        elif pilihan == '6':
            view_task_details(data)
        elif pilihan == '7':
            if data:
                filter_by_jenis(data)
            else:
                print("\n📭 Tidak ada tugas!\n")
        elif pilihan == '8':
            show_statistics(data)
        elif pilihan == '0':
            print("\n👋 Terima kasih! Sampai jumpa lagi!\n")
            break
        else:
            print("\n❌ Pilihan tidak valid! Silakan coba lagi.\n")
            def select_task_status(data):
                """Pilih tugas dan ubah statusnya dengan opsi langsung"""
                display_tasks(data)
                
                if not data:
                    return
                
                try:
                    no = int(input("Masukkan nomor tugas: ").strip())
                    if 1 <= no <= len(data):
                        task = data[no - 1]
                        
                        print(f"\nUbah status '{task['kegiatan']}':")
                        print("1. ✓ Selesai")
                        print("2. ⏳ Belum Selesai")
                        
                        pilihan = input("Pilih status (1-2): ").strip()
                        
                        if pilihan == '1':
                            task['selesai'] = True
                            save_data(data)
                            print(f"✓ Status diubah menjadi Selesai!\n")
                        elif pilihan == '2':
                            task['selesai'] = False
                            save_data(data)
                            print(f"✓ Status diubah menjadi Belum Selesai!\n")
                        else:
                            print("❌ Pilihan tidak valid!\n")
                    else:
                        print("❌ Nomor tidak valid!\n")
                except ValueError:
                    print("❌ Masukkan angka yang valid!\n")

if __name__ == "__main__":
    print("\n🚀 Selamat datang di Program To-Do List!")
    print("=" * 50)
    main_menu()
