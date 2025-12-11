import re

decision_ref_re = re.compile(r'<a\s+href="/decision/(?P<id>[^\?]+)')

#
# Regexps pour le bloc titre
#
title_re = None  # TODO

#
# Regexps pour le "header"
#
# Le bloc "header" est de la forme:
#
#<div class="decision-header">
# <p class="h4-like">Troisième chambre civile
#                          -
#              Formation restreinte RNSM/NA
#                      </p>
#                              <p class="h4-like h4-like--emphase">
#                      </p>
#          <p>ECLI:FR:CCASS:2024:C310675</p>
#        </div>
#
header_re = re.compile(r'<div\s+class="decision-header">(?P<header>.*?)</div>', re.DOTALL)
chambre_re = re.compile(
	r'(?P<chambre>'
	r'Chambre\scommerciale\sfinancière\set\séconomique'
	r'|Chambre\scriminelle'
	r'|Chambre\ssociale'
	r'|Deuxième\schambre\scivile'
	r'|Première\schambre\scivile'
	r'|Première\sprésidence\s\(Ordonnance\)'
	r'|Troisième\schambre\scivile'
	r')', re.UNICODE
)
publication_re = None  # TODO
formation_re = None  # TODO
ecli_re = None  # TODO
