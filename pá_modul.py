import tkinter as tk
from tkinter import messagebox
import datetime
import random

class PÁFilm:
    def __init__(self, cim, ertekeles, datum):
        self.cim = cim
        self.ertekeles = ertekeles
        self.datum = datum

    def szoveg(self):
        return f"{self.cim} ({self.ertekeles}/10, {self.datum})"


def pá_atlag_ertekeles(filmek):
    if not filmek:
        return 0
    osszeg = 0
    for film in filmek:
        osszeg += film.ertekeles
    return osszeg / len(filmek)


class PÁApp:
    def __init__(self, root):
        self.root = root
        self.filmek = []

        self.keret_felso = tk.Frame(root)
        self.keret_felso.pack(padx=10, pady=10)

        self.cim_label = tk.Label(self.keret_felso, text="Cím:")
        self.cim_label.grid(row=0, column=0)
        self.cim_entry = tk.Entry(self.keret_felso, width=30)
        self.cim_entry.grid(row=0, column=1)

        self.ertekeles_label = tk.Label(self.keret_felso, text="Értékelés (1-10):")
        self.ertekeles_label.grid(row=1, column=0)
        self.ertekeles_entry = tk.Entry(self.keret_felso, width=10)
        self.ertekeles_entry.grid(row=1, column=1, sticky="w")

        self.datum_label = tk.Label(self.keret_felso, text="Dátum (ÉÉÉÉ-HH-NN):")
        self.datum_label.grid(row=2, column=0)
        self.datum_entry = tk.Entry(self.keret_felso, width=15)
        self.datum_entry.grid(row=2, column=1, sticky="w")

        self.hozzaad_button = tk.Button(self.keret_felso, text="Hozzáadás", command=self.hozzaad_film)
        self.hozzaad_button.grid(row=3, column=0, pady=5)

        self.torol_button = tk.Button(self.keret_felso, text="Törlés", command=self.torol_kijelolt)
        self.torol_button.grid(row=3, column=1, pady=5, sticky="w")

        self.random_button = tk.Button(self.keret_felso, text="Random ajánlás", command=self.random_ajanlas)
        self.random_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.atlag_label = tk.Label(self.keret_felso, text="Átlagos értékelés: -")
        self.atlag_label.grid(row=5, column=0, columnspan=2, pady=5)

        self.mentes_button = tk.Button(self.keret_felso, text="Mentés fájlba", command=self.mentes_fajlba)
        self.mentes_button.grid(row=6, column=0, pady=5)

        self.betoltes_button = tk.Button(self.keret_felso, text="Betöltés fájlból", command=self.betoltes_fajlbol)
        self.betoltes_button.grid(row=6, column=1, pady=5, sticky="w")

        self.lista = tk.Listbox(root, width=50, height=10)
        self.lista.pack(padx=10, pady=10)
        self.lista.bind("<Double-Button-1>", self.dupla_kattintas)

        self.alapertelmezett_datum()

    def alapertelmezett_datum(self):
        ma = datetime.date.today()
        self.datum_entry.delete(0, tk.END)
        self.datum_entry.insert(0, ma.strftime("%Y-%m-%d"))

    def hozzaad_film(self):
        cim = self.cim_entry.get().strip()
        ertekeles_szoveg = self.ertekeles_entry.get().strip()
        datum_szoveg = self.datum_entry.get().strip()

        if not cim or not ertekeles_szoveg or not datum_szoveg:
            messagebox.showerror("Hiba", "Minden mezőt ki kell tölteni.")
            return

        try:
            ertekeles = int(ertekeles_szoveg)
        except ValueError:
            messagebox.showerror("Hiba", "Az értékelésnek egész számnak kell lennie.")
            return

        if ertekeles < 1 or ertekeles > 10:
            messagebox.showerror("Hiba", "Az értékelés 1 és 10 között legyen.")
            return

        try:
            datum_obj = datetime.datetime.strptime(datum_szoveg, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Hiba", "A dátum formátuma: ÉÉÉÉ-HH-NN.")
            return

        film = PÁFilm(cim, ertekeles, datum_obj.strftime("%Y-%m-%d"))
        self.filmek.append(film)
        self.lista.insert(tk.END, film.szoveg())
        self.frissit_atlag()
        self.cim_entry.delete(0, tk.END)
        self.ertekeles_entry.delete(0, tk.END)
        self.alapertelmezett_datum()

    def torol_kijelolt(self):
        indexek = self.lista.curselection()
        if not indexek:
            return
        i = indexek[0]
        self.lista.delete(i)
        del self.filmek[i]
        self.frissit_atlag()

    def frissit_atlag(self):
        atlag = pá_atlag_ertekeles(self.filmek)
        if self.filmek:
            self.atlag_label.config(text=f"Átlagos értékelés: {atlag:.2f}")
        else:
            self.atlag_label.config(text="Átlagos értékelés: -")

    def random_ajanlas(self):
        if not self.filmek:
            messagebox.showinfo("Info", "Nincs még film a listában.")
            return
        film = random.choice(self.filmek)
        messagebox.showinfo("Ajánlott film", film.szoveg())

    def dupla_kattintas(self, event):
        indexek = self.lista.curselection()
        if not indexek:
            return
        film = self.filmek[indexek[0]]
        messagebox.showinfo("Film részletei", film.szoveg())

    def mentes_fajlba(self):
        if not self.filmek:
            messagebox.showinfo("Info", "Nincs menthető film.")
            return
        try:
            with open("filmek.txt", "w", encoding="utf-8") as f:
                for film in self.filmek:
                    sor = f"{film.cim};{film.ertekeles};{film.datum}\n"
                    f.write(sor)
            messagebox.showinfo("Info", "Mentés kész.")
        except OSError:
            messagebox.showerror("Hiba", "A mentés nem sikerült.")

    def betoltes_fajlbol(self):
        try:
            with open("filmek.txt", "r", encoding="utf-8") as f:
                sorok = f.readlines()
        except FileNotFoundError:
            messagebox.showerror("Hiba", "A filmek.txt fájl nem található.")
            return
        except OSError:
            messagebox.showerror("Hiba", "A betöltés nem sikerült.")
            return
        self.filmek.clear()
        self.lista.delete(0, tk.END)
        for sor in sorok:
            sor = sor.strip()
            if not sor:
                continue
            darabok = sor.split(";")
            if len(darabok) != 3:
                continue
            cim = darabok[0]
            try:
                ertekeles = int(darabok[1])
            except ValueError:
                continue
            datum = darabok[2]
            film = PÁFilm(cim, ertekeles, datum)
            self.filmek.append(film)
            self.lista.insert(tk.END, film.szoveg())
        self.frissit_atlag()
