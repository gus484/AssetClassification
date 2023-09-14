from tkinter import Tk, Label


class DlgAbout(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title("About")

        self.geometry("400x100")
        self.eval('tk::PlaceWindow . center')

        self.app_name = "AssetClassification"
        self.app_version = "Vers.: 0.1"
        self.app_url = "https://github.com/gus484/AssetClassification"
        self.init_page()

    def init_page(self):
        Label(self, text=self.app_name).pack()
        Label(self, text=self.app_version).pack()
        Label(self, text=self.app_url).pack()


if __name__ == "__main__":
    app_about_dlg = DlgAbout()
    app_about_dlg.mainloop()
