"""
Data Sources used to pre-populate TM recomendations
"""

from bs4 import BeautifulSoup as bs
from bs4.element import NavigableString
import os
import json

from bang_pytm.core.threat import Weakness, Threat


def load_owasp_asvs() -> list:
    """
    OWASP Application Security Verification Standard

    Download URL https://github.com/OWASP/ASVS/releases
    """
    results = []
    data = load_xml("asvs.xml")
    ref = load_json("asvs_ref.json")
    # TO DO
    return results


def load_capec() -> list:
    """
    CAPEC Data from MITRE. Ignore Deprecated CAPEC.

    Download URL https://capec.mitre.org/data/xml/capec_latest.xml
    """
    results = []
    data = load_xml("capec.xml")
    ref = data.find("external_references").find_all("external_reference")
    data = data.find_all("attack_patterns")
    for pattern in data:
        if pattern.attrs["status"] == "Deprecated":
            continue
        results.append(
            Threat(
                name=pattern.attrs["name"],
                desc=pattern.find("description"),
                prerequisites=[
                    val.text for val in pattern.find_all("prerequisite")
                ],
                mitigations=[
                    val.text for val in pattern.find_all("mitigations")
                ],
                ref_id="CAPEC-" + pattern.attrs["id"],
                long_desc=pattern.find("extended_description"),
                likelihood=__get_text_val(
                    pattern.find("likelihood_of_attack")
                ),
                severity=__get_text_val(pattern.find("typical_severity")),
                related=[__get_related_capec(related) for related in pattern.find_all("related_attack_pattern")] + [__get_related_cwes(related) for related in pattern.find_all("related_weakness")]
                references=__get_references(pattern.find("references"), ref)
                consequences=__get_consequences(pattern.find("consequences")),
                required_skills=[
                    {"level": val.attrs["level"], "info": val.text}
                    for val in pattern.find_all("skill")
                ],
                required_resources=[
                    val.text for val in pattern.find_all("resource")
                ],
                
                examples=[val.text for val in pattern.find_all("example")],
                steps=__get_attack(pattern.find("execution_flow")),
                relationships=,
                related_weaknesses=,
                ,
            )
        )
    return results


def load_cwes() -> list:
    """
    CWE Data from MITRE. Ignore Deprecated CWEs.

    Download URL https://cwe.mitre.org/data/xml/cwec_latest.xml.zip
    """
    results = []
    data = load_xml("cwe.xml")
    ref = data.find("external_references").find_all("external_reference")
    data = data.find_all("weakness")
    for weakness in data:
        if weakness.attrs["status"] == "Deprecated":
            continue
        results.append(
            Weakness(
                name=weakness.attrs["name"],
                ref_id="CWE-" + weakness.attrs["id"],
                alt_name=[
                    term.text for term in weakness.find_all("alternate_term")
                ],
                desc=weakness.find("description"),
                long_desc=weakness.find("extended_description"),
                mode_introduction=[
                    intro.find("phase").text
                    for intro in weakness.find_all("introduction")
                ],
                exploitable=__get_text_val(
                    weakness.find("likelihood_of_exploit")
                ),
                consequences=__get_consequences(
                    weakness.find("common_consequences")
                ),
                relationships=[
                    __get_related_cwes(related)
                    for related in weakness.find_all("related_weakness")
                ],
                conditions=__get_conditions(
                    weakness.find("applicable_platforms")
                ),
                mitigations=__get_mitigations(
                    weakness.find("potential_mitigations")
                ),
                detection_methods=__get_detection(
                    weakness.find("detection_methods")
                ),
                related_cves=__get_cves(weakness.find("observed_examples")),
                related_threats=__get_capec(
                    weakness.find("related_attack_patterns")
                ),
                references=__get_references(weakness.find("references"), ref),
            )
        )
    return results


def load_xml(fn: str, fpath: str = None) -> bs:
    if fpath == None:
        fpath = os.path.dirname(__file__) + "/reference_data/"
    with open(fpath + fn, "r") as f:
        data = f.read()
    return bs(data, "lxml")


def load_json(fn: str, fpath: str = None) -> list:
    if fpath == None:
        fpath = os.path.dirname(__file__) + "/reference_data/"
    with open(fpath + fn, "r") as f:
        data = json.load(f)
    return data


############################## CAPEC/CWE HELPERS ##############################


def __get_references(references, ref):
    if references == None:
        return None
    references = references.find_all("Reference")
    return [__find_reference(r, ref) for r in references]


def __find_reference(reference, ref):
    ref_id = reference.attrs["External_Reference_ID"]
    ref_info = [r for r in ref if r.attrs["Reference_ID"] == ref_id][0]
    return __get_children(ref_info)


def __get_children(val):
    result = {}
    for child in val.children:
        if type(child) == NavigableString:
            continue
        result[child.name] = child.text.strip("\n")
    return result


def __get_consequences(consequences):
    if consequences == None:
        return None
    return [
        __get_consequence(consequence)
        for consequence in consequences.find_all("consequence")
    ]


def __get_consequence(consequence):
    return {
        "scope": [s.text.strip("\n") for s in consequence.find_all("scope")],
        "impact": [i.text.strip("\n") for i in consequence.find_all("impact")],
        "likelihood": [
            i.text.strip("\n") for i in consequence.find_all("likelihood")
        ],
        "note": [n.text.strip("\n") for n in consequence.find_all("note")],
    }


def __get_related_cwes(related):
    return {
        "cweid": related.attrs["cwe_id"],
        "relation": related.attrs["nature"],
    }


def __get_text_val(txt):
    if txt == None:
        return None
    return txt.text


################################ CAPEC HELPERS ################################


def __get_attack(flow):
    if flow == None:
        return None
    steps = [
        {
            "step": step.find("step").text,
            "phase": step.find("phase").text,
            "desc": step.find("description").text,
            "techniques": [val.text for val in step.find_all("technique")],
        }
        for step in flow.find_all("attack_step")
    ]


def __get_related_capec(related):
    return {
        "capecid": related.attrs["capec_id"],
        "relation": related.attrs["nature"],
    }


################################# CWE HELPERS #################################


def __get_conditions(conditions):
    if conditions == None:
        return None
    results = [__get_applicable(child) for child in conditions.children]
    return [res for res in results if res != None]


def __get_applicable(child):
    if child == None or type(child) == NavigableString:
        return None
    result = {"type": child.name}
    if "class" in child.attrs.keys():
        result["class"] = child.attrs["class"]
    if "name" in child.attrs.keys():
        result["name"] = child.attrs["name"]
    if "prevalence" in child.attrs.keys():
        result["prevalence"] = child.attrs["prevalence"]
    return result


def __get_cves(cves):
    if cves == None:
        return None
    return [
        ex.find("reference").text.strip("\n")
        for ex in cves.find_all("observed_example")
    ]


def __get_mitigations(mitigations):
    if mitigations == None:
        return None
    results = [
        __get_children(mitigation)
        for mitigation in mitigations.find_all("mitigation")
    ]
    return [res for res in results if res != {}]


def __get_detection(mthds):
    if mthds == None:
        return None
    results = [
        __get_children(mthd) for mthd in mthds.find_all("detection_method")
    ]
    return [res for res in results if res != {}]


def __get_capec(threats):
    if threats == None:
        return None
    threats = threats.find_all("related_attack_pattern")
    return ["CAPEC-" + threat.attrs["capec_id"] for threat in threats]


################################# ASVS HELPERS #################################

# PLACE YOUR HELPER FUNCTIONS HERE FOR ASVS
