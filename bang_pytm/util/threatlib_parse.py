import json
import re
from bang_pytm.core.asset import Asset, ExternalEntity, Datastore, Process
from bang_pytm.core.finding import Finding
from bang_pytm.engine.rules import Rule
from bang_pytm.core.control import Control
from bang_pytm.core.flow import DataFlow
from bang_pytm.util import sources
from bang_pytm.core.tm import TM

# Parses the rules found in the threats.json file of pytm, stores it as a list of Rules
def parse_pytm_threatlib():
    with open('./bang_pytm/util/pytm_threatlib.json', 'r', encoding='utf8') as f:
        data = json.load(f)
    capec = sources.load_capec()
    pytm_rules = []
    
    for d in data:
        # get CAPEC ID
        capec_ref = re.search('capec\.mitre\.org\/data\/definitions\/(\d*)\.html', d["references"])
        if capec_ref:
            capec_id = capec_ref.group(1)
            for c in capec:
                if c.meta["ref_id"] == "CAPEC-" + capec_id:
                    threat = c
        else:
            threat = None

        # get controls
        controls_list = re.findall('target\.controls\.(\w*) is (True|False)', d["condition"])
        controls_list_2 = re.findall('target\.controls\.(\w*)', d["condition"])
        
        # EXAMPLE EXPRESSION: s = "(target.hasDataLeaks() or any(d.isCredentials or d.isPII for d in target.data)) and (not target.controls.isEncrypted or (not target.isResponse and any(d.isStored and d.isDestEncryptedAtRest for d in target.data)) or (target.isResponse and any(d.isStored and d.isSourceEncryptedAtRest for d in target.data)))"
        # "condition": "target.usesEnvironmentVariables is True and target.controls.sanitizesInput is False and target.controls.checksInputBounds is False"
        control_conditions = re.findall('(and|or)', d["condition"])
        filtered_control_conditions = []
        for i in range(len(controls_list) - 1):
            if control_conditions[i] in ['and', 'or']:
                filtered_control_conditions.append(control_conditions[i])
        
        # create separate rules object for each target
        for t in d['target']:
            if t in ["Process", "Datastore", "ExternalEntity"]:
                pytm_rules.append(Rule(globals()[t], threat, controls_list))
            elif t == "Dataflow":
                pytm_rules.append(Rule(DataFlow, threat, controls_list))
            elif t in ["Server", "Lambda"]:
                pytm_rules.append(Rule(Asset, threat, controls_list))
            else:
                raise Exception("Unknown Asset type")
    return pytm_rules

# Given a Component and a list of Rules, return the unmitigated and mitigated threats for that component 
def component_threats(component, threat_map):
    mitigated_threats = []
    unmitigated_threats = []
    applicable_rules = [t for t in threat_map if type(component) == t.component]
    for r in applicable_rules:
        result = r.mitigated_threat(component)
        if result['is_mitigated']:
            mitigated_threats.append(result['threat'])
        else:
            unmitigated_threats.append(result['threat'])
    return mitigated_threats, unmitigated_threats 

# Given the list of Components in a TM, return Findings for each Component
def get_findings(tm_components, threat_map):
    findings = []
    for component in tm_components:
        mt, umt = component_threats(component, threat_map)
        finding = Finding(affected_components=component, issues=umt)
        findings.append(finding)
    return findings

