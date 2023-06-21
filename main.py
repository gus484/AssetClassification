import json
import os
from ac import AssetAllocation
from json import JSONDecodeError
from tkinter import *
from tkinter import filedialog


class App:
    CONFIG_FILE_PATH = 'config.json'

    def __init__(self):
        self.version = "0.01"
        self.w = None
        self.input_path = None
        self.inp_mapping = None
        self.inp_isin = None
        self.lb_isin = None
        self.mapping_path = None
        self.input_path = None
        self.txt_log = None
        self.report_path = None
        self.config = {}

        self.path_to_script = ''

    def load_config(self):
        if not os.path.exists(App.CONFIG_FILE_PATH):
            return

        with open(App.CONFIG_FILE_PATH, encoding="utf8") as f:
            try:
                self.config = json.load(f)
            except JSONDecodeError:
                print("could not load config file!")

    def set_config(self):
        isin_filter = self.config.get('isin', [])

        for isin in isin_filter:
            self.lb_isin.insert(END, isin)

        if os.path.exists(self.config.get("mapping")):
            self.mapping_path.set(self.config.get("mapping"))
        if os.path.exists(self.config.get("input", "")):
            self.input_path.set(self.config.get("input", ""))
        if os.path.exists(self.config.get("report", "")):
            self.report_path.set(self.config.get("report", ""))

    def write_config(self):
        self.config['isin'] = self.lb_isin.get(0, END)
        self.config['mapping'] = self.mapping_path.get()
        self.config['input'] = self.input_path.get()
        self.config['report'] = self.report_path.get()
        json_object = json.dumps(self.config, indent=4, ensure_ascii=False)

        with open(App.CONFIG_FILE_PATH, "w", encoding="utf8") as outfile:
            outfile.write(json_object)

    def run(self):
        self.load_config()
        self.w = Tk()
        self.w.title(f"AssetAllocation (Ver. {self.version})")

        self.create_isin_filter()
        self.create_mapping_file_selector()
        self.create_csv_file_selector()
        self.create_out_file_selector()

        f = Frame(master=self.w, pady=5)
        btn_run_script = Button(f, text=self.config.get('run_script', 'run script'), width=25, command=self.run_script)
        btn_run_script.pack()
        f.pack()

        self.create_log_view()

        self.set_config()
        self.w.mainloop()

    def make_invisible(self, widget):
        widget.pack_forget()

    def create_log_view(self):
        self.txt_log = Text(self.w)
        self.make_invisible(self.txt_log)

    def create_csv_file_selector(self):
        f = Frame(master=self.w, pady=5, padx=10)
        self.input_path = StringVar()
        inp_csv = Entry(f, textvariable=self.input_path, state=DISABLED, width=25)
        btn_set_csv_path = Button(f, text=self.config.get("input_path", "input path"),
                                  command=self.open_input_path, width=15)

        inp_csv.pack(side="left")
        btn_set_csv_path.pack(side="left")
        f.pack()

    def create_out_file_selector(self):
        f = Frame(master=self.w, pady=5, padx=10)
        self.report_path = StringVar()
        inp_csv = Entry(f, textvariable=self.report_path, state=DISABLED, width=25)
        btn_set_out_path = Button(f, text=self.config.get("report_path", "report path"),
                                  command=self.open_report_path, width=15)

        inp_csv.pack(side="left")
        btn_set_out_path.pack(side="left")
        f.pack()

    def create_mapping_file_selector(self):
        f = Frame(master=self.w, pady=10)
        self.mapping_path = StringVar()
        self.inp_mapping = Entry(f, textvariable=self.mapping_path, state=DISABLED, width=25)
        btn_set_gpo_path = Button(f, text=self.config.get("region_mapping", "region mapping"),
                                  command=self.open_mapping_path, width=15)

        self.inp_mapping.pack(side="left")
        btn_set_gpo_path.pack(side="left")
        f.pack()

    def create_isin_filter(self):
        rt = Frame(master=self.w)
        r1 = Frame(rt, padx=5)
        r2 = Frame(rt)

        isin_label = Label(r1, text="ISIN-Filter")
        self.lb_isin = Listbox(r1, selectmode=SINGLE, height=4, width=25)

        isin_label.pack()
        self.lb_isin.pack()

        btn_delete_isin = Button(r2, text="🗙", command=self.delete_isin)
        btn_delete_isin.place(relx=0.0)
        btn_delete_isin.pack(side=TOP)

        rt2 = Frame(master=self.w)
        r3 = Frame(rt2, padx=5)
        r4 = Frame(rt2)

        self.inp_isin = Entry(r3, width=25)
        self.inp_isin.pack(side='left')

        btn_add_isin = Button(r4, text="➕", command=self.add_isin)
        btn_add_isin.pack(side=TOP)

        r1.pack(side='left')
        r2.pack(side="left", expand=True)
        r3.pack(side='left')
        r4.pack(side="left")
        rt.pack()
        rt2.pack()

    def add_isin(self):
        self.lb_isin.insert(0, [self.inp_isin.get()])

    def delete_isin(self):
        if self.lb_isin.curselection() != ():
            self.lb_isin.delete(self.lb_isin.curselection())

    def open_report_path(self):
        report_path = filedialog.askdirectory()
        if report_path != "":
            self.report_path.set(report_path)

    def open_input_path(self):
        input_path = filedialog.askdirectory()
        if input_path != "":
            self.input_path.set(input_path)

    def open_mapping_path(self):
        mapping_path = filedialog.askopenfilename(filetypes=[('JSON File', '*.json')])
        if mapping_path != "":
            self.mapping_path.set(mapping_path)

    def get_isin_filter(self):
        isin_list = []
        for isin in self.lb_isin.get(0, END):
            isin_list.append(isin[0])
        return isin_list

    def run_script(self):
        self.write_config()
        ac = AssetAllocation()
        ac.set_parameters(self.input_path.get(), self.report_path.get(), self.get_isin_filter(), self.mapping_path.get(), 'de')
        ac.run()


if __name__ == '__main__':
    app = App()
    app.run()
