import yaml
from tmnt_dsl.core.control import Control, ControlCatalog, Part, Metadata


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
