import webbrowser
from tkinter import ttk, Toplevel

from dialogs import helper
from report.translation import Translation


class DlgAbout(Toplevel):

    def __init__(self, app_version, script_version):
        Toplevel.__init__(self)
        self.title(Translation.get_name('about'))
        self.iconbitmap("")

        width = 400
        height = 210

        self.geometry(helper.get_center_coords(self, width, height))

        self.app_name = "AssetClassification"
        self.app_version = f"App.-Vers.: {app_version}"
        self.script_version = f"Script-Vers.: {script_version}"
        self.app_url = "https://github.com/gus484/AssetClassification"
        self.init_page()

    def init_page(self):
        ttk.Label(self, text=self.app_name).pack()
        ttk.Label(self, text=self.app_version).pack()
        ttk.Label(self, text=self.script_version).pack()
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

        link5 = ttk.Label(self, text="Info Squared icon by Icons8", foreground="blue",
                          cursor="hand2")
        link5.pack()
        link5.bind("<Button-1>", lambda e: self.callback("https://icons8.com/icon/IIoAou6tSNjt/info-squared"))

        link6 = ttk.Label(self, text="Medium Risk icon by Icons8", foreground="blue",
                          cursor="hand2")
        link6.pack()
        link6.bind("<Button-1>", lambda e: self.callback("https://icons8.com/icon/CTr8yPJXyPcs/medium-risk"))

        link7 = ttk.Label(self, text="High Priority icon by Icons8", foreground="blue",
                          cursor="hand2")
        link7.pack()
        link7.bind("<Button-1>", lambda e: self.callback("https://icons8.com/icon/51w77eaukGoV/high-priority"))

    def callback(self, url):
        webbrowser.open_new(url)


if __name__ == "__main__":
    app_about_dlg = DlgAbout()
    app_about_dlg.mainloop()
