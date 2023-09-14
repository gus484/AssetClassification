from tkinter import Listbox, Frame, SINGLE, END, Entry, Toplevel

from reader.etf_reader import EtfReader


class DlgEtfLib(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self)
        self.lb_issuers = None

        self.etf_data = {}
        self.title("ETF-Lib")

        self.get_etfs()
        self.create_issuer_listbox()
        self.grid_frame = Frame(self)

        if master:
            self.focus()
            self.grab_set()

    def get_etfs(self):
        self.etf_data = EtfReader.get_isin_and_names()

    def create_issuer_listbox(self):
        r1 = Frame(master=self, padx=5)
        self.lb_issuers = Listbox(r1, selectmode=SINGLE, height=4, width=25)
        self.lb_issuers.grid(row=0, column=0)
        self.lb_issuers.bind('<<ListboxSelect>>', self.create_table)

        for issuer in self.etf_data:
            self.lb_issuers.insert(END, issuer)
        r1.grid()

    def create_table(self, event):
        idx = event.widget.curselection()[0]
        issuer = self.lb_issuers.get(idx)
        Table(self.grid_frame, self.etf_data[issuer])


class Table:

    def __init__(self, tbl_frame, data):

        for widget in tbl_frame.winfo_children():
            widget.destroy()

        idx = 0
        for isin, name in data.items():
            self.e = Entry(tbl_frame, width=15, fg='black',
                           font=('Arial', 12, 'bold'))

            self.e.grid(row=idx, column=0)
            self.e.insert(END, isin)
            self.e.config(state="disabled")

            self.e = Entry(tbl_frame, width=50, fg='black',
                           font=('Arial', 12, 'normal'))

            self.e.grid(row=idx, column=1)
            self.e.insert(END, name)
            self.e.config(state="disabled")
            idx += 1

        tbl_frame.grid()


if __name__ == "__main__":
    app_eft_dlg = DlgEtfLib()
    app_eft_dlg.mainloop()
