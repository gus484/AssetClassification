import glob
import json
import os
import queue
import threading
import time
import tkinter
from json import JSONDecodeError
from tkinter import *
from tkinter import filedialog, ttk
from tkinter.ttk import Combobox, Progressbar

from ttkthemes import ThemedTk

from ac import AssetAllocation
from dialogs.dlgAbout import DlgAbout
from dialogs.dlgAddIsin import DlgAddIsin
from dialogs.dlgEtfLib import DlgEtfLib
from report.translation import Translation


class App:
    CONFIG_FILE_PATH = 'config.json'

    def __init__(self):
        self.app_path = None
        self.version = "0.2"
        self.w = None
        self.language_code = None
        self.d_region_mappings = None

        self.btn_set_gpo_path = None
        self.btn_set_out_path = None
        self.btn_set_csv_path = None
        self.btn_run_script = None

        self.cb_mapping = None

        self.img_add = None
        self.img_folder = None
        self.img_remove = None

        self.lb_isin_filter = None
        self.lb_language = None
        self.lb_log = None
        self.lb_source_path = None
        self.lb_target_path = None

        self.inp_isin = None
        self.inp_mapping = None
        self.inp_pp_path = None

        self.menubar = None
        self.settings_menu = None
        self.pb_progress = None
        self.progress_step_size = 25

        self.tv_isin = None
        self.tv_log = None

        self.mapping_path = None
        self.source_path = None
        self.target_path = None
        self.pp_path = None

        self.config = {}
        self.log_queue = None
        self.log_thread = None
        self.script_thread = None

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
            self.tv_isin.insert('', 'end', values=(isin, ""))

        self.change_language(self.config.get('language', 'en'))

        if os.path.exists(self.config.get("mapping", "")):
            mapping_path = self.config.get("mapping")
            mapping_name = os.path.basename(mapping_path).replace('.json', '').upper()
            if mapping_name in self.d_region_mappings:
                self.cb_mapping.set(mapping_name)
        if os.path.exists(self.config.get("input", "")):
            self.source_path.set(self.config.get("input", ""))
        if os.path.exists(self.config.get("report", "")):
            self.target_path.set(self.config.get("report", ""))

    def write_config(self):
        self.config['mapping'] = self.d_region_mappings[self.cb_mapping.get()]
        self.config['input'] = self.source_path.get()
        self.config['report'] = self.target_path.get()
        self.config['language'] = self.language_code
        self.config['isin'] = self.get_isin_filter()
        json_object = json.dumps(self.config, indent=4, ensure_ascii=False)

        with open(App.CONFIG_FILE_PATH, "w", encoding="utf8") as outfile:
            outfile.write(json_object)

    def run(self):
        self.load_config()

        Translation.set_language(self.config.get('language', 'en'))

        self.w = ThemedTk(theme="arc")
        self.w.title(f"AssetAllocation (Ver. {self.version})")
        self.create_menu_bar()

        self.app_path = os.getcwd()
        img_path = os.path.join(self.app_path, "images")

        self.img_folder = PhotoImage(file=os.path.join(img_path, "folder.png"))
        self.img_remove = PhotoImage(file=os.path.join(img_path, "remove.png"))
        self.img_add = PhotoImage(file=os.path.join(img_path, "add.png"))
        if os.name == 'nt':
            self.w.iconbitmap(os.path.join(img_path, "pie.ico"))
        else:
            self.w.iconphoto(False, os.path.join(img_path, "pie.png"))

        fm = Frame(master=self.w, pady=5)

        ft = Frame(master=fm, pady=5)
        self.create_source_path_selector(ft)
        self.create_target_path_selector(ft)
        self.create_pp_file_selector(ft)
        ft.pack(side='top')

        fl = Frame(master=fm, padx=5)

        fl1 = Frame(master=fl, padx=5)
        self.create_isin_filter(fl1)
        fl1.pack(side='top')

        fl2 = Frame(master=fl, padx=5, pady=15)
        self.create_mapping_file_selector(fl2)
        fl2.pack()
        fl.pack(side='left', fill='y')

        fr = Frame(master=fm, padx=5)
        self.create_log_view(fr)
        fr.pack(side='right', fill='y')

        fm.pack(side='top')

        fb = Frame(master=self.w)
        self.create_run_button(fb)
        self.create_progress_bar(fb)
        fb.pack(side='bottom')

        self.set_config()
        self.w.mainloop()

    def show_about(self):
        dlg_about = DlgAbout(self.version, AssetAllocation.VERSION)
        dlg_about.mainloop()

    def show_etf_lib(self):
        dlg_etf_lib = DlgEtfLib(self.w)
        dlg_etf_lib.mainloop()

    def create_isin_filter(self, parent_frame: Frame):
        r1 = Frame(parent_frame)
        r2 = Frame(parent_frame, pady=17)

        self.lb_isin_filter = ttk.Label(r1, text=Translation.get_name('isin_filter'))

        columns = ('isin', 'name')
        self.tv_isin = ttk.Treeview(r1, height=4, columns=columns, show='headings')
        self.tv_isin.column("isin", anchor=CENTER, stretch=NO, width=80)
        self.tv_isin.heading('isin', text='ISIN')
        self.tv_isin.heading('name', text='Name')

        self.lb_isin_filter.pack(side=TOP)
        self.tv_isin.pack()

        r1.pack(side='left')

        btn_delete_isin = ttk.Button(r2, command=self.delete_isin, image=self.img_remove, width=5, padding=0)
        btn_delete_isin.pack(side=TOP)
        btn_add_isin = ttk.Button(r2, command=self.show_add_isin, image=self.img_add, width=5, padding=0)
        btn_add_isin.pack(side=TOP)
        r2.pack(side="left", fill="y")

    def create_log_view(self, parent_frame: Frame):
        f = Frame(master=parent_frame)

        self.lb_log = ttk.Label(f, text="Logs")
        self.lb_log.pack(side=TOP)

        columns = ('type', 'message')
        self.tv_log = ttk.Treeview(f, selectmode='none', columns=columns, show='headings', height=7)
        self.tv_log.column("type", anchor=CENTER, stretch=NO, width=80)
        self.tv_log.column("message", anchor=W, stretch=YES)
        self.tv_log.heading('type', text='Type')
        self.tv_log.heading('message', text='Message')

        # Constructing vertical scrollbar
        vsb = ttk.Scrollbar(f, orient="vertical", command=self.tv_log.yview)
        vsb.pack(side='right', fill='y')
        self.tv_log.configure(yscrollcommand=vsb.set)
        self.tv_log.pack()
        f.pack(fill='y')

    def create_mapping_file_selector(self, parent_frame: Frame):
        self.lb_language = ttk.Label(parent_frame, text="Region mapping:", width=20, anchor='e')
        self.lb_language.pack(side=LEFT, padx=5)

        mappings = list(self.get_available_mappings().keys())

        self.cb_mapping = Combobox(parent_frame, values=mappings, state="readonly")
        self.cb_mapping.set(mappings[0])
        self.cb_mapping.pack(side=LEFT)

    def create_menu_bar(self):
        self.menubar = Menu()
        self.w.config(menu=self.menubar)

        self.settings_menu = Menu(self.menubar, tearoff=0)
        sub_menu = Menu(self.settings_menu, tearoff=0)
        sub_menu.add_command(label='de', command=lambda: self.change_language('de'))
        sub_menu.add_command(label='en', command=lambda: self.change_language('en'))
        self.settings_menu.add_cascade(
            label="Language",
            menu=sub_menu
        )

        self.menubar.add_cascade(
            label="Preferences",
            menu=self.settings_menu,
            underline=0
        )

        self.menubar.add_command(label="ETFLib", command=self.show_etf_lib)
        self.menubar.add_command(label="About", command=self.show_about, compound=tkinter.RIGHT)

    def create_progress_bar(self, parent_frame: Frame):
        f = Frame(master=parent_frame, pady=5)
        self.pb_progress = Progressbar(f, value=0, length=400)
        self.pb_progress.pack()
        f.pack()

    def create_pp_file_selector(self, parent_frame: Frame):
        f = Frame(master=parent_frame, pady=5)

        lb_pp_path = ttk.Label(f, text="PP-File:", width=15, anchor="e")
        lb_pp_path.pack(side=LEFT)

        self.pp_path = StringVar()
        self.inp_pp_path = ttk.Entry(f, textvariable=self.pp_path, state=DISABLED, width=50)
        btn_pp_path = ttk.Button(f, image=self.img_folder, width=5, command=self.open_pp_path, padding=0)

        self.inp_pp_path.pack(side="left")
        btn_pp_path.pack(side="left")
        f.pack()

    def create_run_button(self, parent_frame: Frame):
        f = Frame(master=parent_frame, pady=5)

        self.btn_run_script = ttk.Button(f, text=Translation.get_name('run_script'), width=25,
                                         command=self.run_script)
        self.btn_run_script.pack()
        f.pack()

    def create_source_path_selector(self, parent_frame: Frame):
        f = Frame(master=parent_frame, pady=5, padx=10)

        self.lb_source_path = ttk.Label(f, text="Source path:", width=15, anchor="e")
        self.lb_source_path.pack(side=LEFT)

        self.source_path = StringVar()
        inp_csv = ttk.Entry(f, textvariable=self.source_path, state=DISABLED, width=50)
        self.btn_set_csv_path = ttk.Button(f, command=self.open_input_path, image=self.img_folder, width=5, padding=0)

        inp_csv.pack(side="left")
        self.btn_set_csv_path.pack(side="left")
        f.pack()

    def create_target_path_selector(self, parent_frame: Frame):
        f = Frame(master=parent_frame, pady=5, padx=10)

        self.lb_target_path = ttk.Label(f, text="Target path:", width=15, anchor="e")
        self.lb_target_path.pack(side=LEFT)

        self.target_path = StringVar()
        inp_csv = ttk.Entry(f, textvariable=self.target_path, state=DISABLED, width=50)
        self.btn_set_out_path = ttk.Button(f, image=self.img_folder, width=5, command=self.open_report_path, padding=0)

        inp_csv.pack(side="left")
        self.btn_set_out_path.pack(side="left")
        f.pack()

    def get_available_mappings(self) -> dict[str: str]:
        self.d_region_mappings = {}
        json_files = glob.glob(os.path.join('mappings/region/', f'*.json'))
        for jfile in json_files:
            file_name = os.path.basename(jfile).replace('.json', '').upper()
            self.d_region_mappings[file_name] = jfile
        return self.d_region_mappings

    def change_language(self, language: str):
        Translation.set_language(language)
        self.language_code = language
        self.btn_run_script.config(text=Translation.get_name('run_script'))
        self.lb_target_path.config(text=Translation.get_name('report_path'))
        self.lb_source_path.config(text=Translation.get_name('input_path'))
        self.lb_language.config(text=Translation.get_name('region_mapping'))
        self.lb_log.config(text=Translation.get_name('log_messages'))
        self.lb_isin_filter.config(text=Translation.get_name('isin_filter'))
        self.menubar.entryconfig(1, label=Translation.get_name('preferences'))
        self.settings_menu.entryconfig(1, label=Translation.get_name('language'))
        self.menubar.entryconfig(3, label=Translation.get_name('about'))

    def show_add_isin(self):
        isin = tkinter.StringVar()
        dlg_isin = DlgAddIsin(isin)
        dlg_isin.wait_window()
        self.tv_isin.insert('', 'end', values=(isin.get(), ""))

    def delete_isin(self):
        selected_items = self.tv_isin.selection()
        for selected_item in selected_items:
            self.tv_isin.delete(selected_item)

    def open_input_path(self):
        input_path = filedialog.askdirectory()
        if input_path != "":
            self.source_path.set(input_path)

    def open_pp_path(self):
        pp_path = filedialog.askopenfilename(filetypes=[('PP File', '*.xml')])
        if pp_path != "":
            self.pp_path.set(pp_path)

    def open_report_path(self):
        report_path = filedialog.askdirectory()
        if report_path != "":
            self.target_path.set(report_path)

    def get_isin_filter(self) -> list:
        isin_list = []
        for line in self.tv_isin.get_children():
            isin_list.append(self.tv_isin.item(line)['values'][0])
        return isin_list

    def run_ac(self, log_queue: queue):
        self.pb_progress.stop()

        if self.inp_pp_path.get() != "":
            self.progress_step_size = 20
        else:
            self.progress_step_size = 25

        ac = AssetAllocation(log_queue)
        ac.set_parameters(self.source_path.get(), self.target_path.get(), self.get_isin_filter(),
                          self.d_region_mappings[self.cb_mapping.get()], self.language_code, '')
        ac.run()

        self.btn_run_script['state'] = tkinter.NORMAL

    def format_log_message(self, message) -> list:
        lvl_idx = message.find(":")
        return [message[:lvl_idx], message[lvl_idx + 1:].lstrip(' ')]

    def update_progress(self, message: str):
        if message.startswith("Stage"):
            self.pb_progress.step(self.progress_step_size)
        if message.startswith('finished'):
            # progressbar will jump to 0 if it is set to 100
            self.pb_progress.step(self.progress_step_size - 0.01)

    def log_message(self):
        """
        writes messages from the queue to the text widget as long the script thread runs
        """
        run = True
        while run:
            time.sleep(0.1)

            while not self.log_queue.empty():
                ele = self.log_queue.get()
                msg_type, message = self.format_log_message(ele.getMessage())
                self.update_progress(message)
                self.tv_log.insert('', 'end', values=(msg_type, message))

            if not self.script_thread.is_alive():
                run = False

    def run_script(self):
        self.btn_run_script['state'] = tkinter.DISABLED

        self.write_config()

        # clear log view
        for line in self.tv_log.get_children():
            self.tv_log.delete(line)

        # configure and start the log and ac script threads
        self.log_queue = queue.Queue()
        self.script_thread = threading.Thread(target=self.run_ac, args=(self.log_queue,))
        self.log_thread = threading.Thread(target=self.log_message)

        self.log_thread.start()
        self.script_thread.start()


if __name__ == '__main__':
    app = App()
    app.run()
