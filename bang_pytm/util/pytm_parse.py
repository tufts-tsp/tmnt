import json
from bang_pytm.core.asset import Asset, Process, Lambda
from bang_pytm.core.control import Control
from bang_pytm.util import sources
from bang_pytm.core.tm import TM

capec = sources.load_capec()

with open('test_threatlib.json', 'r') as f:
    data = json.load(f)

obj_mapping = {
    "Asset":Asset,
    "Process":Process,
    "Lambda":Lambda
}

pytm_threats = []

for d in data:
    controls = []
    for control in d['controls']:
        controls.append(Control(name=control))
    threat = None
    for c in capec:
        if c.ref_id == "CAPEC-" + d['capec']:
            threat = c
    for component in d['component']:
        obj = obj_mapping[component]
        pytm_threats.append({
            'component':obj,
            'threat':threat,
            'controls':controls
        })
        
        
# tm = TM()
# tm.add_component(Asset())
# tm.add_component(Asset())
# tm.add_component(Process())
# tm_components = tm.components

tm_components = [Asset(), Asset(), Process()]

mitigated_threats = []
unmitigated_threats = []


def of_type(component, threat_map):
    threats = [threat for threat in threat_map if type(component) == type(threat['component'])]
    if len(threat) > 0:
        return threats
    return None

def mitigated_threat(component, threat):
    applied_controls = []
    not_applied_controls = []
    for control in threat['control']:
        if control.name in [c.name for c in component.controls]:
            applied_controls.append(control)
        else:
            not_applied_controls.append(control)
    mitigated = True if len(applied_controls) > 0 else False
    return {
        'threat':threat, 
        'mitigated':mitigated, 
        'applied_controls':applied_controls,
        'not_applied_controls':not_applied_controls
    }

findings = []

for component in tm_components:
    finding = {'component':component,'mitigated_threats':[], 'unmitigated_threats':[]}
    threats = of_type(component, pytm_threats)
    for threat in threats:
        result = mitigated_threat(component, threat)
        if result['mitigated']:
            finding['mitigated_threats'].append(result)
        else:
            finding['unmitigated_threats'].append(result)
        
