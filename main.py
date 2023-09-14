import json
import os
import queue
import threading
import time
import tkinter
from json import JSONDecodeError
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox

from ac import AssetAllocation
from dialogs.dlgAbout import DlgAbout
from dialogs.dlgEtfLib import DlgEtfLib
from report.translation import Translation


class App:
    CONFIG_FILE_PATH = 'config.json'

    def __init__(self):
        self.version = "0.01"
        self.w = None
        self.cb_language = None
        self.input_path = None
        self.inp_mapping = None
        self.isin_label = None
        self.inp_isin = None
        self.lb_isin = None
        self.mapping_path = None
        self.input_path = None
        self.txt_log = None
        self.report_path = None
        self.pp_path = None
        self.inp_pp_path = None
        self.config = {}
        self.log_queue = None
        self.log_thread = None
        self.script_thread = None
        self.btn_set_gpo_path = None
        self.btn_set_out_path = None
        self.btn_set_csv_path = None
        self.btn_run_script = None

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

        self.cb_language.set(self.config.get('language', 'en'))

        if os.path.exists(self.config.get("mapping", "")):
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
        self.config['language'] = self.cb_language.get()
        json_object = json.dumps(self.config, indent=4, ensure_ascii=False)

        with open(App.CONFIG_FILE_PATH, "w", encoding="utf8") as outfile:
            outfile.write(json_object)

    def run(self):
        self.load_config()

        Translation.set_language(self.config.get('language', 'en'))

        self.w = Tk()
        self.w.title(f"AssetAllocation (Ver. {self.version})")

        self.create_menu_bar()
        self.create_isin_filter()
        self.create_mapping_file_selector()
        self.create_csv_file_selector()
        self.create_out_file_selector()
        self.create_pp_file_selector()
        self.create_language_selector()

        f = Frame(master=self.w, pady=5)
        self.btn_run_script = Button(f, text=Translation.get_name('run_script'), width=25,
                                     command=self.run_script)
        self.btn_run_script.pack()
        f.pack()

        self.create_log_view()

        self.set_config()

        self.w.mainloop()

    def make_invisible(self, widget):
        widget.pack_forget()

    def show_about(self):
        dlg_about = DlgAbout()
        dlg_about.mainloop()

    def show_etflib(self):
        dlg_etflib = DlgEtfLib(self.w)
        dlg_etflib.mainloop()

    def create_menu_bar(self):
        menubar = Menu()
        self.w.config(menu=menubar)
        menubar.add_command(label="ETFLib", command=self.show_etflib)
        menubar.add_command(label="About", command=self.show_about, compound=tkinter.RIGHT)

    def create_log_view(self):
        f = Frame(master=self.w, pady=5)

        self.txt_log = Text(f, width=30, height=10, wrap=tkinter.NONE)
        self.txt_log.grid(column=0, row=1)
        self.txt_log.pack(side="left")

        scrollbar = Scrollbar(f, command=self.txt_log.yview)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.txt_log.config(yscrollcommand=scrollbar.set)

        f.pack()

    def create_csv_file_selector(self):
        f = Frame(master=self.w, pady=5, padx=10)
        self.input_path = StringVar()
        inp_csv = Entry(f, textvariable=self.input_path, state=DISABLED, width=25)
        self.btn_set_csv_path = Button(f, text=Translation.get_name("input_path"),
                                       command=self.open_input_path, width=15)

        inp_csv.pack(side="left")
        self.btn_set_csv_path.pack(side="left")
        f.pack()

    def create_out_file_selector(self):
        f = Frame(master=self.w, pady=5, padx=10)
        self.report_path = StringVar()
        inp_csv = Entry(f, textvariable=self.report_path, state=DISABLED, width=25)
        self.btn_set_out_path = Button(f, text=Translation.get_name("report_path"),
                                       command=self.open_report_path, width=15)

        inp_csv.pack(side="left")
        self.btn_set_out_path.pack(side="left")
        f.pack()

    def create_mapping_file_selector(self):
        f = Frame(master=self.w, pady=10)
        self.mapping_path = StringVar()
        self.inp_mapping = Entry(f, textvariable=self.mapping_path, state=DISABLED, width=25)
        self.btn_set_gpo_path = Button(f, text=Translation.get_name("region_mapping"),
                                       command=self.open_mapping_path, width=15)

        self.inp_mapping.pack(side="left")
        self.btn_set_gpo_path.pack(side="left")
        f.pack()

    def create_language_selector(self):
        f = Frame(master=self.w, pady=5)
        languages = ['de', 'en']

        self.cb_language = Combobox(f, values=languages, state="readonly")
        self.cb_language.set(languages[0])
        self.cb_language.bind("<<ComboboxSelected>>", self.change_language)
        f.pack()
        self.cb_language.pack()

    def change_language(self, event):
        Translation.set_language(event.widget.get())
        self.btn_run_script.config(text=Translation.get_name('run_script'))
        self.btn_set_out_path.config(text=Translation.get_name('report_path'))
        self.btn_set_csv_path.config(text=Translation.get_name('input_path'))
        self.btn_set_gpo_path.config(text=Translation.get_name('region_mapping'))
        self.isin_label.config(text=Translation.get_name('isin_filter'))

    def create_pp_file_selector(self):
        f = Frame(master=self.w, pady=5)

        self.pp_path = StringVar()
        self.inp_pp_path = Entry(f, textvariable=self.pp_path, state=DISABLED, width=25)
        btn_pp_path = Button(f, text=Translation.get_name("pp_file"),
                             command=self.open_pp_path, width=15)

        self.inp_pp_path.pack(side="left")
        btn_pp_path.pack(side="left")
        f.pack()

    def create_isin_filter(self):
        rt = Frame(master=self.w)
        r1 = Frame(rt, padx=5)
        r2 = Frame(rt)

        self.isin_label = Label(r1, text=Translation.get_name('isin_filter'))
        self.lb_isin = Listbox(r1, selectmode=SINGLE, height=4, width=25)

        self.isin_label.pack()
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

    def open_pp_path(self):
        pp_path = filedialog.askopenfilename(filetypes=[('PP File', '*.xml')])
        if pp_path != "":
            self.pp_path.set(pp_path)

    def get_isin_filter(self):
        isin_list = []
        for isin in self.lb_isin.get(0, END):
            isin_list.append(isin[0])
        return isin_list

    def run_ac(self, log_queue: queue):
        ac = AssetAllocation(log_queue)
        ac.set_parameters(self.input_path.get(), self.report_path.get(), self.get_isin_filter(),
                          self.mapping_path.get(), self.cb_language.get())
        ac.run()

        self.btn_run_script['state'] = tkinter.NORMAL

    def format_log_message(self, message) -> str:
        lvl_idx = message.find(":")
        return message[lvl_idx + 1:]

    def log_message(self):
        """
        writes messages from the queue to the text widget as long the script thread runs
        """
        run = True
        while run:
            time.sleep(0.1)

            while not self.log_queue.empty():
                ele = self.log_queue.get()
                self.txt_log.insert(END, self.format_log_message(ele.getMessage()) + '\n')

            if not self.script_thread.is_alive():
                run = False

    def run_script(self):
        self.btn_run_script['state'] = tkinter.DISABLED

        self.write_config()

        self.txt_log.delete("1.0", tkinter.END)

        # configure and start the log and ac script threads
        self.log_queue = queue.Queue()
        self.script_thread = threading.Thread(target=self.run_ac, args=(self.log_queue,))
        self.log_thread = threading.Thread(target=self.log_message)

        self.log_thread.start()
        self.script_thread.start()


if __name__ == '__main__':
    app = App()
    app.run()
