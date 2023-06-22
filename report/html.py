class Html:
    def __init__(self, title, scripts=None):
        self.html = ""
        self.title = title
        self.write_header(scripts)
        self.script_store = []

    def write_to_file(self, path):
        self.write_scripts_onload()
        self.write_footer()

        with open(path, 'w', encoding="utf-8") as writer:
            writer.write(self.html)

    def write_header(self, scripts):
        self.html += "<!doctype html>"
        self.html += '<html lang="de">'
        self.html += '<head><meta charset="utf-8">'
        self.html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        self.html += f'<title>{self.title}</title>'
        self.html += '<link rel="stylesheet" href="css/style.css">'
        self.html += '<link type="image/png" sizes="96x96" rel="icon" href="img/ring.png">'
        if scripts:
            for script in scripts:
                self.html += f'<script type="text/javascript" src="{script}"></script>'
        self.html += '</head>'
        self.html += '<body>'

    def write_footer(self):
        self.html += '</body></html>'

    def write_infobox(self, data, tag_id=''):
        """
        Creates div info_box from the tuples of the data list
        :param data: list of tuples
        :param tag_id: div tag id attribute
        """
        self.html += f'<div class="info_container" id="{tag_id}">'
        for d in data:
            self.html += f'<div class="info_box"><div>{d[0]}</div><div>{d[1]}</div></div>'
        self.html += '</div>'

    def write_div(self, data, css_class="", tag_id=""):
        self.html += f'<div id="{tag_id}" class="{css_class}">{data}</div>'

    def write_link_bar(self, links, active):
        self.html += "<nav><ul>"
        for link in links:
            c = ""
            if active == link[0]:
                c = "active"
            self.html += f'<li><a class="{c}" href="{link[1]}">{link[0]}</a></li>'
        self.html += "</ul></nav>"

    def write_toc(self, data):
        self.html += '<div id="toc_container">'
        self.html += '<p class="toc_title">Contents</p>'
        self.html += '<ul class="toc_list">'
        for d in data:
            self.html += f'<li><a href="#{d[1]}">{d[0]}</a></li>'
        self.html += '</ul></div>'

    def write_table(self, tbl_caption, col_headlines, data):
        self.html += f'<table><caption>{tbl_caption}</caption><thead><tr>'
        for h in col_headlines:
            self.html += f'<th>{h}</th>'
        self.html += '</tr></thead>'
        for row in data:
            self.html += '<tr>'
            for col in row:
                self.html += f'<td>{str(col)}</td>'
            self.html += '</tr>'
        self.html += '</table>'

    def write_script_tag(self, path):
        self.html += f'<script src="{path}"></script>'

    def write_run_script_after_doc_loaded(self, name, id, *args):
        self.script_store.append(f'{name}("{id}",{",".join(args)});')

    def write_scripts_onload(self):
        self.html += '<script> window.onload = function() {'
        for script in self.script_store:
            self.html += script + '\n'
        self.html += '}</script>'
