import tmnpy.dsl as dsl
from tmnpy.dsl import TM, Control, ControlCatalog, Data
from tmnpy.dsl.control import Part, Metadata
from tmnpy.dsl.threat import SecurityProperty

import yaml


class Parser(object):
    def load_yaml(self, file_path):
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
        return data


class TMNTParser(Parser):
    def __init__(self, tm_name: str, yaml: str):
        self.yaml = self.load_yaml(yaml)
        self.tm = TM(tm_name)
        self.results = []
        if "assets" in self.yaml.keys():
            for asset in self.yaml["assets"]:
                obj, kwargs = self.parse_component(asset)
                self.tm.add_component(obj(**kwargs))
        if "actors" in self.yaml.keys():
            for actor in self.yaml["actors"]:
                obj, kwargs = self.parse_element(actor)
                self.tm.add_actor(obj(**kwargs))
        if "flows" in self.yaml.keys():
            for flow in self.yaml["flows"]:
                obj, kwargs = self.parse_component(flow)
                self.tm.add_component(obj(**kwargs))

    def parse_list_value(self, v):
        nm = v["name"]
        component = [c for c in self.tm.components if c.name == nm]
        if len(component) == 0:
            e = f"Could not find {nm} in the TM Components."
            e += "Have you specified that it should be created?"
            raise SyntaxError(e)
        elif len(component) > 1:
            e = f"Found multiple components named {nm}."
            e += "Please assign an unique name"
            raise SyntaxError(e)
        return component[0]

    def parse_component(self, component):
        component_type, kwargs = self.parse_element(component)
        objs = {
            k: v
            for k, v in kwargs.items()
            if type(v) != str and type(v) != bool
        }
        for k, v in objs.items():
            if k == "security_property":
                v = SecurityProperty(**v)
                # print(v.confidentiality)
            elif k == "data":
                data_elems = []
                for d in v:
                    # print(d)
                    data_elems.append(Data(**d))
                # print(v)
                v = data_elems
            elif k == "path":
                path = []
                for component in v:
                    path.append(self.parse_list_value(component))
                v = path
            elif k in ["src", "dst"]:
                v = self.parse_list_value(v)
            elif k == "port":
                pass
            # print(k, v)
            kwargs[k] = v
        return component_type, kwargs

    def parse_element(self, element):
        if not isinstance(element, dict):
            raise TypeError(f"Issue parsing {element}")
        element_type = getattr(dsl, element["type"])
        kwargs = {k: v for k, v in element.items() if k != "type"}
        return element_type, kwargs


class OSCALParser:
    # CREATE CONTROL CATALOG

    # get metadata for control catalog
    def parse_metadata(self, data):
        return Metadata(
            title=data["title"],
            published=data["published"],
            last_modified=data["last-modified"],
            version=data["version"],
            oscal_version=data["oscal-version"],
        )

    def parse_part(self, part_data):
        part = Part(id=part_data["id"], prose=part_data.get("prose", ""))
        part.part_name = part_data["name"]
        return part

    def parse_control(self, control_data):
        # account for parts within the controls
        part = None
        part_list = []
        for part_data in control_data.get("parts", []):
            part = self.parse_part(part_data)
            part_list.append(part)

        control = Control(
            id=control_data["id"],
            title=control_data["title"],
            parts=part_list,
        )

        # set the property dict. hopefully this is the right way to do it
        if "props" in control_data:
            for prop in control_data["props"]:
                control.prop[prop["name"]] = prop["value"]

        return control

    def parse_group(self, group_data):
        subgroup = None
        subgroup_list = []
        control_list = []
        part_list = []

        if "groups" in group_data:
            for subgroup_data in group_data["groups"]:
                subgroup = self.parse_group(subgroup_data)
                subgroup_list.append(subgroup)

        if "controls" in group_data:
            for control_data in group_data["controls"]:
                control = self.parse_control(control_data)
                control_list.append(control)

        if "parts" in group_data:
            for part_data in control_data.get("parts", []):
                part = self.parse_part(part_data)
                part_list.append(part)

        return ControlCatalog.Group(
            id=group_data["id"],
            title=group_data["title"],
            subgroups=subgroup_list,
            controls=control_list,
        )

    # tie it all together!

    def parse_catalog(self, data):
        group_list = []
        control_list = []

        parsed_metadata = self.parse_metadata(data["metadata"])

        for group_data in data["groups"]:
            group = self.parse_group(group_data)
            group_list.append(group)

        if "controls" in data:
            for control_data in data["controls"]:
                control = self.parse_control(control_data)
                control_list.append(control)

        catalog = ControlCatalog(
            metadata=parsed_metadata, groups=group_list, controls=control_list
        )

        return catalog

    def load_yaml(self, file_path):
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
            return self.parse_catalog(data["catalog"])
