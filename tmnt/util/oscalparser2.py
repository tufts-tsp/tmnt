import yaml
from tmnt.dsl import *


class OSCALParser2:

    def __init__(self):
        tm = TM()

    def parse_security_property(self, sp_data):
        return SecurityProperty(
            confidentiality = sp_data["confidentiality"],
            integrity = sp_data["integrity"],
            availability = sp_data["availability"],
        )
    

    def parse_data(self, data):
        return Data (
            name = data["name"],
            is_pii = data["is_pii"],
            is_phi = data["is_phi"],
            format = data["format"],
            is_credentials = data["is_credentials"],
            lifetime = data["lifetime"],
        )


    def parse_asset(self, asset_data):
        return Asset(
            name = asset_data["name"],
            machine = asset_data["machine"],
            security_property = parse_security_property(asset_data["security_property"]),
            data = parse_data(asset_data["data"])
        )

    def parse_boundary(self, boundary_data):
        return Boundary(
            name = boundary_data["name"],
            boundary_owner = parse_actor(boundary_data["boundary_owner"]),
        )

    def parse_actor(self, actor_data):
        return Actor(
            name = actor_data["name"],
            actor_type = actor_data["actor_type"],
            physical_access = actor_data["physical_access"],
            security_property = parse_security_property(actor_data["security_property"]),
        )

    
    def parse_flow(self, flow_data):
        return Flow (
            name = flow_data["name"],

            #src = get_assest_by_name(flow_data["src"]),
            #dst = flow_data["dst"],
            #path = flow_data["path"],
            
            authentication = flow_data["authentication"],
            multifactor_authentication = flow_data["multifactor_authentication"],
        )





    def parse_dataflow(self, dataflow_data):
        # only for DATAFLOW 
            # port = flow_data["port"] #convert to int
            # protocol = flow_data["protocol"]

    
    def parse_workflow(self, workflow_data):


    def parse_external_entities(self, ee_data):
        return ExternalEntity (
            name = ee_data["name"],
            physical_access = ee_data["physical_access"],
            machine = ee_data["machine"],
        )

        #security_property = 
        #data = 


    def load_yaml(self, file_path):
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
            return data
            # return self.parse_catalog(data["catalog"]) 



    def parse(self, file_path, tm):
        self.tm = tm
        data = load_yaml(file_path)

        #parse all elements/components 
        for actor in data["actor"]:
            if actor["type"] = "Actor":
                act = parse_actor(actor)
                tm.addActor(act)

        
        return self.tm