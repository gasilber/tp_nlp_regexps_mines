import re

decision_ref_re = re.compile(r'<a\s+href="/decision/(?P<id>[^\?]+)')
ecli_re = re.compile(r"(?P<ecli>ECLI:[A-Z]+:[A-Z]+:\d{4}:[A-Z0-9]+)")
chamber_re = re.compile(r'class="h4-like">(?P<chamber>.*)')
formation_re = re.compile(r'class="h4-like">.*\s*\-\s*(?P<formation>.*)')
publication_re = re.compile(r'<p class="h4-like h4-like--emphase">\s*(?P<publication>[^\<]*)')
number_re = re.compile(r"<title>Décision - Pourvoi n°(?P<number>[0-9\-\.]*)")
decision_date_re = re.compile(r'<div class="decision-content decision-content--main">\s*<h1>(?P<day>[0-9]{1,2})\s(?P<month>[a-zA-Zéû]*)\s(?P<year>[0-9]{4})')
solution_re = re.compile(r"TODO")
content_re = re.compile(r"TODO")
texts_re = re.compile(r"TODO")