import shutil
import uuid
import xml.dom.minidom
import xml.etree.ElementTree
import xml.etree.ElementTree as EleTree
from dataclasses import dataclass

from pp.pp_colors import PPColor


@dataclass
class Security:
    name: str
    isin: str
    idx: int


class PPUpdater:

    def __init__(self, src_filepath: str, target_filepath: str):
        self.pp_file = src_filepath
        self.pp_file_backup = src_filepath + ".bck"
        self.pp_file_out = target_filepath
        self.tree = EleTree.parse(src_filepath)
        self.securities = {}
        self.COLOR_COUNTER = -1
        self.COLOR_SUB_COUNTER = 0
        self.colors = PPColor()

    def run(self, data, tax_name="ETFClassification"):
        self.create_backup()
        self.read_pp_securities()

        if self.exist_taxonomy(tax_name):
            self.remove_taxonomy(tax_name)

        prepared_data = self.prepare_data(data)
        taxonomy, children = self.create_a_taxonomy(tax_name)

        for d in prepared_data:
            self.create_classification(children, d, prepared_data[d])

        self.write_to_file()

    def prepare_data(self, data):
        prepared_data = {}
        for isin in data:
            if not self.exist_security(isin):
                continue
            r = extract_data(data[isin], self.securities[isin].idx)
            prepared_data = merge_data(r, prepared_data)
        return prepared_data

    def create_backup(self) -> None:
        shutil.copyfile(self.pp_file, self.pp_file_backup)

    def exist_security(self, security_isin: str) -> bool:
        if security_isin in self.securities:
            return True
        return False

    def exist_taxonomy(self, name: str) -> bool:
        tag = self.tree.getroot().find('taxonomies')
        taxonomies = tag.findall('taxonomy')
        for tax in taxonomies:
            if tax.find('name').text == name:
                return True
        return False

    def remove_taxonomy(self, name: str) -> bool:
        tag = self.tree.getroot().find('taxonomies')
        taxonomies = tag.findall('taxonomy')
        for tax in taxonomies:
            if tax.find('name').text == name:
                self.tree.getroot().remove(tax)
                return True
        return False

    def read_pp_securities(self):
        root = self.tree.getroot()

        tag = root.find('securities')
        if tag is None:
            return

        securities = tag.findall('security')
        idx = 0
        for security in securities:
            name_tag = security.find('name').text
            isin_tag = security.find('isin').text
            idx += 1
            self.securities[isin_tag] = Security(name_tag, isin_tag, idx)

    def create_a_taxonomy(self, tax_name: str):
        parent = self.tree.getroot().find('taxonomies')

        tax = xml.etree.ElementTree.SubElement(parent, "taxonomy")
        id_tag = xml.etree.ElementTree.SubElement(tax, "id")
        id_tag.text = str(uuid.uuid4())
        name = xml.etree.ElementTree.SubElement(tax, "name")
        name.text = tax_name

        children = self.create_root_element(tax, tax_name)
        return [tax, children]

    def create_root_element(self, parent, tax_name):
        root = xml.etree.ElementTree.SubElement(parent, "root")

        id_tag = xml.etree.ElementTree.SubElement(root, "id")
        id_tag.text = str(uuid.uuid4())
        name = xml.etree.ElementTree.SubElement(root, "name")
        name.text = tax_name
        color = xml.etree.ElementTree.SubElement(root, "color")
        color.text = "#83969e"
        self.create_assignments(root)
        children = xml.etree.ElementTree.SubElement(root, "children")
        return children

    def create_classification(self, parent, name, data, lvl=0):
        classification = xml.etree.ElementTree.SubElement(parent, "classification")
        self.create_base_taxonomy_data(classification, name, lvl)
        children = xml.etree.ElementTree.SubElement(classification, "children")
        if type(data) == dict:
            for d in data:
                self.create_classification(children, d, data[d], lvl + 1)
            self.create_assignments(classification)
        else:
            self.create_assignments(classification, data)

    def create_base_taxonomy_data(self, parent, tax_name, lvl):
        id_tag = xml.etree.ElementTree.SubElement(parent, "id")
        id_tag.text = str(uuid.uuid4())
        name = xml.etree.ElementTree.SubElement(parent, "name")
        name.text = tax_name
        color = xml.etree.ElementTree.SubElement(parent, "color")
        # color.text = "#83969e"
        if lvl == 0:
            self.COLOR_COUNTER += 1
            color.text = self.colors.get_top_color(self.COLOR_COUNTER)
            self.COLOR_SUB_COUNTER = 0
        else:
            color.text = self.colors.get_color(self.COLOR_COUNTER, self.COLOR_SUB_COUNTER)
            self.COLOR_SUB_COUNTER += 1
        return [name, id_tag, color]

    def write_to_file(self):
        with open("pp.xml", "wb") as f:
            self.tree.write(f)

    def create_assignments(self, parent, data=None):
        assignments = xml.etree.ElementTree.SubElement(parent, "assignments")
        if data is not None:
            for d in data:
                self.create_assignment(assignments, d)

    def create_assignment(self, parent, data: tuple):
        idx = ''
        if data[1] > 2:
            idx = f"[{data[1]}]"
        weight_val = round(float(data[0]) * 100)

        assignment = xml.etree.ElementTree.SubElement(parent, "assignment")

        investment_vehicle = xml.etree.ElementTree.SubElement(assignment, "investmentVehicle")
        investment_vehicle.set("class", "security")
        investment_vehicle.set("reference", "../../../../../../../../../../securities/security" + idx)

        weight = xml.etree.ElementTree.SubElement(assignment, "weight")
        weight.text = str(weight_val)

        rank = xml.etree.ElementTree.SubElement(assignment, "rank")
        rank.text = str(0)


def extract_data(data, security):
    r = {}
    d = list(data.values())

    for region in d:
        top_lvl = region[0][0]
        r[top_lvl] = {}
        for e in region[1]:
            sub_lvl, weight, _ = e
            r[top_lvl][sub_lvl] = [(weight, security)]

    return r


def merge_data(r, data):
    if len(data) == 0:
        return r

    for top_lvl in r:
        if top_lvl in data:
            for sub_lvl in r[top_lvl]:
                if sub_lvl in data[top_lvl]:
                    data[top_lvl][sub_lvl].append(r[top_lvl][sub_lvl][0])
                    print(data[top_lvl][sub_lvl], r[top_lvl][sub_lvl])
                else:
                    data[top_lvl][sub_lvl] = r[top_lvl][sub_lvl]
        else:
            data[top_lvl] = r[top_lvl]

    return data
