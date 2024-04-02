from bang_pytm.util import sources as s
asvs = s.load_owasp_asvs()
capec = s.load_capec()
cwes = s.load_cwes()
cwes[20].meta['related']
asvs[20].title