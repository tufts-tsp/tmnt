import yaml
from tmnt.dsl import *


class TMNTParser:

    def __init__(self):
        tm = TM()


    def parse_finding(self, finding_data):


        return Finding(
            affected_components = #union
            issues = #union
            controls = #union
            relevance = finding_data["relevance"],
            likelihood = finding_data["likelihood"],
            likelihood_event_occurence = finding_data["likelihood_event_occurence"],
            likelihood_adverse_event = finding_data["likelihood_adverse_event"],
            impact = finding_data["impact"],
            technical_impact = #security property 
        
            business_impact = #list
            safety_impact = #safety impact
            predispositions = finding_data["predispositions"],
            severity = finding_data["severity"],
            pervasiveness = finding_data["pervasiveness"],
            risk = finding_data["risk"],
            residual_risk = finding_data["residual_risk"],
        )


    def parse_stride(self, stride_data):
        return STRIDE(
            spoofing = stride_data["spoofing"],
            tampering = stride_data["tampering"],
            repudiation = stride_data["repudiation"],
            information_disclosure = stride_data["information_disclosure"],
            denial_of_service = stride_data["denial_of_service"],
            elevation_of_privilege = stride_data["elevation_of_privilege"],
        )


    def parse_security_property(self, sp_data):
        return SecurityProperty(
            confidentiality = sp_data["confidentiality"],
            integrity = sp_data["integrity"],
            availability = sp_data["availability"],
        )


    def parse_safetyimpact(self, safetyimpact_data):
        return SafetyImpact(
            harm = safetyimpact_data["harm"],
            exploitability = safetyimpact_data["exploitability"],
        )


    def parse_element(self, element_data):
        return Element(
            name = element_data["name"],
            desc = element_data["desc"],
        )


    def parse_boundary(self, boundary_data):
    return Boundary(
        name = boundary_data["name"],
        boundary_owner = self.tm.get_actor_by_name(boundary_data["boundary_owner"]),
    )


    def parse_actor(self, actor_data):
        return Actor(
            name = actor_data["name"],
            security_property = parse_security_property(actor_data["security_property"]),
            actor_type = actor_data["actor_type"],
            physical_access = actor_data["physical_access"],
        )


    def parse_component(self, component_data):
        data = None
        d_list = []
        for d in component_data.get("data_list", []):
            part = self.parse_data(d)
            d_list.append(data)

        return Component(
            name = component_data["name"],
            desc = component_data["desc"],
            data_list = d_list, 
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


    def parse_issue(self, issue_data):
        return Issue(
            name = issue_data["name"],
            desc = issue_data["desc"],
            prerequisites = issue_data["prerequisites"],
            mitigations = issue_data["mitigations"],
            ref_id = issue_data["ref_id"],
            long_desc = issue_data["long_desc"],
            likelihood = issue_data["likelihood"],
            severity = issue_data["severity"],
            related = issue_data["related"],
            references = issue_data["references"],
            consequences = issue_data["consequences"],
        )


    def parse_threat(self, threat_data):
    return Threat(
        name = threat_data["name"],
        desc = threat_data["desc"],
        examples = threat_data["examples"],
        threat_source_desc = threat_data["threat_source_desc"],
        required_skills = threat_data["required_skills"],
        required_resources = threat_data["required_resources"],
        avenue = threat_data["avenue"],
        attack_steps = threat_data["attack_steps"],
    )
    

    def parse_vulnerability(self, vulnerability_data):
        return Vulnerability(
            name = vulnerability_data["name"],
        )


    def parse_weakness(self, weakness_data):
        return Weakness(
            name = weakness_data["name"],
            alt_name = weakness_data["alt_name"],
            desc = weakness_data["desc"],
            mode_introduction = weakness_data["mode_introduction"],
            detection_methods = weakness_data["detection_methods"],
        )


    def parse_asset(self, asset_data):

        open_port = None
        open_port_list = []
        for open_port_data in asset_data.get("open_ports", []):
            open_port = self.#parse_boundary(open_port_data)
            open_port_list.append(open_port)

        #part list[int] for open ports

        boundary = None
        boundary_list = []
        for boundary_data in asset_data.get("trust_boundaries", []):
            boundary = self.parse_boundary(boundary_data)
            boundary_list.append(boundary)
        
        
        return Asset(
            name = asset_data["name"],
            open_ports = open_port_list,
            trust_boundaries = boundary_list,
            machine = asset_data["machine"],
            security_property = parse_security_property(asset_data["security_property"]),
            data = parse_data(asset_data["data"]),
        )


    def parse_external_entities(self, ee_data):
        return ExternalEntity (
            name = ee_data["name"],
            machine = ee_data["machine"],
            security_property = parse_security_property(ee_data["security_property"]),
            data = parse_data(ee_data["data"]),
            physical_access = ee_data["physical_access"],
        )


    def parse_datastore(self, datastore_data):
        return Datastore(
            name = datastore_data["name"],
            ds_type = datastore_data["ds_type"], 
        )


    def parse_process(self, process_data):
        return Process(
            name = process_data["name"],
        )

    
    def parse_flow(self, flow_data):
        return Flow (
            name = flow_data["name"],
            src = self.tm.get_component_by_name(flow_data["src"]),
            dst = self.tm.get_component_by_name(flow_data["dst"]),
            path = self.tm.get_component_by_name(flow_data["path"]),
            authentication = flow_data["authentication"],
            multifactor_authentication = flow_data["multifactor_authentication"],
        )


    def parse_dataflow(self, dataflow_data):
        return DataFlow(
            name = flow_data["name"],
            protocol = flow_data["protocol"],
            port = int(flow_data["port"]),
        )

    
    def parse_workflow(self, workflow_data):
        element = None
        element_list = []
        for element_data in workflow_data.get("path", []):
            element = self.parse_element(element_data)
            element_list.append(element)

        return WorkFlow(
            name = workflow_data["name"],
            path = element_list,
        )


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