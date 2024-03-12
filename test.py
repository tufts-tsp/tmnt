from bang_pytm.util import sources as s
data = s.load_xml("asvs.xml")
asvs = s.load_owasp_asvs()
capec = s.load_capec()
cwes = s.load_cwes()
cwes[20].meta['related']