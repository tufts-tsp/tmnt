import json
import re
from bang_pytm.core.asset import Asset, Lambda, ExternalEntity, Datastore, Process
from bang_pytm.core.control import Control
from bang_pytm.util import sources
from bang_pytm.core.tm import TM

capec = sources.load_capec()

with open('./bang_pytm/util/pytm_threatlib.json', 'r', encoding='utf8') as f:
    data = json.load(f)

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
    and_controls = d["condition"]
    controls_list = re.findall('target\.controls\.(\w*) is (True|False)', d["condition"])
    # "(target.hasDataLeaks() or any(d.isCredentials or d.isPII for d in target.data)) and (not target.controls.isEncrypted or (not target.isResponse and any(d.isStored and d.isDestEncryptedAtRest for d in target.data)) or (target.isResponse and any(d.isStored and d.isSourceEncryptedAtRest for d in target.data)))"
    
    # create separate rules object for each target
    for t in d['target']:
        if t in ["Lambda", "Process", "Datastore", "ExternalEntity"]:
            pytm_rules.append({
                'component': globals()[t],
                'threat': threat,
                'controls': controls_list})
        elif t in ["Server", "Dataflow"]:
            print("warning ", t)
            pytm_rules.append({
                'component': t,
                'threat': threat,
                'controls': controls_list})
        else:
            print(t)
