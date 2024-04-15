import yaml
from bang_pytm.core.control import Control, ControlCatalog, Part

class OSCALParser:
    
    # CREATE CONTROL CATALOG

    # get metadata for control catalog
    def parse_metadata(data):
        return ControlCatalog.Metadata(
            title=data['title'],
            published=data['published'],
            last_modified=data['last_modified'],
            version=data['version'],
            oscal_version=['oscal_version']
        )
    
    def parse_part(self, part_data):
        part = Part(id = part_data['id'],
                    prose = part_data.get('prose', "")
                    )
        part.part_name = part_data['name']
        return part
    
    def parse_control(self, control_data):

        # account for parts within the controls
        part = None
        part_list = []
        for part_data in control_data.get('parts', []):
            part = self.parse_part(part_data)
            part_list.append(part)
        
        control = Control(
            id = control_data['id'],
            title = control_data['title'],
            parts = part_list,
        )

        # set the property dict. hopefully this is the right way to do it
        if 'props' in control_data:
            for prop in control_data['props']:
                control.prop[prop['name']] = prop['value']
        
        return control
    
    def parse_group(self, group_data):
        
        subgroup = None
        subgroup_list = []
        control_list = []
        part_list = []

        if 'groups' in group_data:
            for subgroup_data in group_data['groups']:
                subgroup = self.parse_group(subgroup_data)
                subgroup_list.append(subgroup)
        
        if 'controls' in group_data:
            for control_data in group_data['controls']:
                control = self.parse_control(control_data)
                control_list.append(control)

        if 'parts' in group_data:
            for part_data in control_data.get('parts', []):
                part = self.parse_part(part_data)
                part_list.append(part)
        
        return ControlCatalog.Group(
            id = group_data['id'],
            title = group_data['title'],
            subgroups = subgroup_list,
            controls = control_list
        )
    
    # tie it all together!

    



  