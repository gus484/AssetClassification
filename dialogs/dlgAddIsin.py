import tkinter
from tkinter import Frame, Toplevel, ttk

from dialogs import helper


class DlgAddIsin(Toplevel):

    def __init__(self, isin: tkinter.StringVar):
        Toplevel.__init__(self)
        self.label_isin = None
        self.inp_isin = None
        self.btn_add = None
        self.isin = isin

        width = 350
        height = 100

        self.geometry(helper.get_center_coords(self, width, height))
        self.title("Add ISIN")

        self.create_isin_entry()

        self.focus()
        self.grab_set()
        # self.overrideredirect(True)

    def create_isin_entry(self):
        window = Frame(master=self, padx=5)
        self.label_isin = ttk.Label(window, text="ISIN")
        self.inp_isin = ttk.Entry(window)
        self.btn_add = ttk.Button(window, text="Add ISIN", command=self.add_isin)

        self.label_isin.pack()
        self.inp_isin.pack()
        self.btn_add.pack()
        window.pack()

    def add_isin(self):
        self.isin.set(self.inp_isin.get())
        self.destroy()
        self.update()


if __name__ == "__main__":
    app_isin_dlg = DlgAddIsin()
    app_isin_dlg.mainloop()
