# tkinter adalah standar library untuk pengenalan GUI (Graphical User Interface)

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

# Init
window = tk.Tk()
window.configure(bg="white") # warna layar
window.geometry("300x200") # mengatur ukuran, tapi masih bisa resize
window.resizable(False, False) # Ukuran layar tidak dapat diubah
window.title("IKN Design City") # Membuat judul pada layar

# Variabel dan Fungsi
NAMA_DEPAN = tk.StringVar()
NAMA_BELAKANG = tk.StringVar()

def tombol_click():
    '''fungsi ini akan dipanggil oleh tombol'''
    pesan = f"Halo {NAMA_DEPAN.get()} {NAMA_BELAKANG.get()}, Cantik!"
    showinfo(title="Ada apa?", message=pesan)

# frame input
input_frame = ttk.Frame(window)

# Penempatan Grid, Pack, dan Place
input_frame.pack(padx=10, pady=10, fill="x", expand=True)

# Komponen-Komponen
# 1. Label nama depan
nama_depan_label = ttk.Label(input_frame, text="Nama Depan: ")
nama_depan_label.pack(padx=10, fill="x", expand=True)
# 2. Entry nama depan
nama_depan_entry = ttk.Entry(input_frame, textvariable=NAMA_DEPAN)
nama_depan_entry.pack(padx=10, fill="x", expand=True)
# 3. Label nama belakang
nama_belakang_label = ttk.Label(input_frame, text="Nama Belakang: ")
nama_belakang_label.pack(padx=10, fill="x", expand=True)
# 4. Entry nama belakang
nama_belakang_entry = ttk.Entry(input_frame, textvariable=NAMA_BELAKANG)
nama_belakang_entry.pack(padx=10, fill="x", expand=True)
# 5. Tombol
tombol_sapa = ttk.Button(input_frame, text = "Redesign the map", command=tombol_click)
tombol_sapa.pack(padx=10, pady=10, fill='x', expand=True)


# Main loop window, Supaya layar GUI nya muncul
window.mainloop() 