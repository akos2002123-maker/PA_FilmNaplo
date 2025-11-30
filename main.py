import tkinter as tk
from pá_modul import PÁApp

def main():
    root = tk.Tk()
    root.title("app")
    app = PÁApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
