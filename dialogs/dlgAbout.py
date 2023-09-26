import webbrowser
from tkinter import ttk, Toplevel

from dialogs import helper


class DlgAbout(Toplevel):

    def __init__(self, version):
        Toplevel.__init__(self)
        self.title("About")
        self.iconbitmap("")

        width = 400
        height = 150

        self.geometry(helper.get_center_coords(self, width, height))

        self.app_name = "AssetClassification"
        self.app_version = f"Vers.: {version}"
        self.app_url = "https://github.com/gus484/AssetClassification"
        self.init_page()

    def init_page(self):
        ttk.Label(self, text=self.app_name).pack()
        ttk.Label(self, text=self.app_version).pack()
        ttk.Label(self, text=self.app_url).pack()

        link = ttk.Label(self, text="Images:")
        link.pack()

        link1 = ttk.Label(self, text="Loschen Icons erstellt von Pixel perfect - Flaticon", foreground="blue",
                          cursor="hand2")
        link1.pack()
        link1.bind("<Button-1>", lambda e: self.callback("https://www.flaticon.com/de/kostenlose-icons/loschen"))

        link2 = ttk.Label(self, text="Plus Icons erstellt von Pixel perfect - Flaticon", foreground="blue",
                          cursor="hand2")
        link2.pack()
        link2.bind("<Button-1>", lambda e: self.callback("ttps://www.flaticon.com/de/kostenlose-icons/plus"))

        link3 = ttk.Label(self, text="Datei Icons erstellt von DinosoftLabs - Flaticon", foreground="blue",
                          cursor="hand2")
        link3.pack()
        link3.bind("<Button-1>", lambda e: self.callback("https://www.flaticon.com/de/kostenlose-icons/datei"))

        link4 = ttk.Label(self, text="Graph Icons erstellt von Freepik - Flaticon", foreground="blue",
                          cursor="hand2")
        link4.pack()
        link4.bind("<Button-1>", lambda e: self.callback("https://www.flaticon.com/de/kostenlose-icons/graph"))

    def callback(self, url):
        webbrowser.open_new(url)


if __name__ == "__main__":
    app_about_dlg = DlgAbout()
    app_about_dlg.mainloop()
