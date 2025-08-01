import ttkbootstrap as ttk
from adaptor.gui import TimeKeeperApp

if __name__ == "__main__":
    root = ttk.Window(themename="litera")
    app = TimeKeeperApp(root)
    root.mainloop()