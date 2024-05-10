from bang_pytm.core.finding import Finding


# Given the list of Components in a TM, return Findings for each Component
def get_findings(tm_components, threat_map):
    findings = []
    for component in tm_components:
        mt, umt = threat_map.component_threats(component)
        finding = Finding(affected_components=component, issues=umt)
        findings.append(finding)
    return findings
