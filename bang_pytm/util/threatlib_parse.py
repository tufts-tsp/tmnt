import json
import re
from bang_pytm.core.asset import Asset, Lambda, ExternalEntity, Datastore, Process
from bang_pytm.core.control import Control
from bang_pytm.core.flow import Flow
from bang_pytm.util import sources
from bang_pytm.core.tm import TM


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
        # control_conditions = re.findall('(and|or)', d["condition"])
        # filtered_control_conditions = []
        # for i in range(len(controls_list) - 1):
        #     if control_conditions[i] in ['and', 'or']:
        #     filtered_control_conditions.append(control_conditions[i])
        
        # create separate rules object for each target
        for t in d['target']:
            if t in ["Lambda", "Process", "Datastore", "ExternalEntity"]:
                pytm_rules.append({
                    'component': globals()[t],
                    'threat': threat,
                    'controls': controls_list})
            elif t == "Dataflow":
                pytm_rules.append({
                    'component': Flow,
                    'threat': threat,
                    'controls': controls_list})
            elif t == "Server":
                pytm_rules.append({
                    'component': Asset,
                    'threat': threat,
                    'controls': controls_list})
            else:
                raise Exception("Unknown Asset type")
    return pytm_rules

# Given a rule (containing a threat and the controls needed to mitigate that threat), and an Asset with some controls, use the rule to determine whether the threat applies on this Asset. Return the threat, whether it was mitigated, and the controls that were found to apply/not apply.
def mitigated_threat(component:Asset, rule:dict):
    applied_controls = []
    not_applied_controls = []
    for control in rule['controls']:
        if control[0] in [c.name for c in component.controls]:
            applied_controls.append(control)
        else:
            not_applied_controls.append(control)
    # TODO
    is_mitigated = True if len(applied_controls) > 0 else False
    return {
        'threat':rule, 
        'is_mitigated': is_mitigated, 
        'applied_controls': applied_controls,
        'not_applied_controls': not_applied_controls
    }

# Given a set of rules and a component, return the unmitigated and mitigated threats for that component 
def component_threats(component, threat_map):
    mitigated_threats = []
    unmitigated_threats = []
    applicable_rules = [t for t in pytm_rules if type(component) == t['component']]
    for r in applicable_rules:
        result = mitigated_threat(component, r)
        if result['is_mitigated']:
            mitigated_threats.append(result['threat'])
        else:
            unmitigated_threats.append(result['threat'])
    return mitigated_threats, unmitigated_threats 

pytm_rules = parse_pytm_threatlib()
tm_components = [Asset(), Asset(), Process()]
findings = []
for component in tm_components:
    mt, ut = component_threats(component, pytm_rules)
    finding = {'component':component,'mitigated_threats':mt, 'unmitigated_threats':ut}
    findings.append(finding)
