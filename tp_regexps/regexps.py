import re

decision_ref_re = re.compile(r'<a\s+href="/decision/(?P<id>[^\?]+)')

# Regex pour le bloc titre
# <h1>10 décembre 2024<br>
#                       Cour de cassation<br>
#                                 Pourvoi n°
#                     24-82.423
#         </h1>
# from this we must extract the groups :
# number : 24-82.423
# day : 10
# month : décembre
# year : 2024

title_re = re.compile(
    # Début du H1 et capture de la date (Jour, Mois, Année)
    r"<h1>\s*(?P<day>\d+)\s+(?P<month>[a-zéûé]+)\s+(?P<year>\d{4})<br>"
    # Nouvelle section : capture tout (y compris les sauts de ligne) jusqu'à "Pourvoi n°"
    r".*?"
    # Début de la référence du pourvoi
    r"Pourvoi n°\s*(?P<number>[\d\-. ]+)\s*<\/h1>",
    re.DOTALL | re.IGNORECASE,
)


# Regexps pour le "header"
#
# Le bloc "header" est de la forme:
#
# <div class="decision-header">
# <p class="h4-like">Troisième chambre civile
#                          -
#              Formation restreinte RNSM/NA
#                      </p>
#                              <p class="h4-like h4-like--emphase">
#                      </p>
#          <p>ECLI:FR:CCASS:2024:C310675</p>
#        </div>
#
header_re = re.compile(
    r'<div\s+class="decision-header">(?P<header>.*?)</div>', re.DOTALL
)
chambre_re = re.compile(
    r"(?P<chambre>"
    r"Chambre\scommerciale\sfinancière\set\séconomique"
    r"|Chambre\scriminelle"
    r"|Chambre\ssociale"
    r"|Deuxième\schambre\scivile"
    r"|Première\schambre\scivile"
    r"|Première\sprésidence\s\(Ordonnance\)"
    r"|Troisième\schambre\scivile"
    r")",
    re.UNICODE,
)

# <p class="h4-like h4-like--emphase">
#                                           Publié au Bulletin
#                                                     </p>
publication_re = re.compile(
    r'<p\s+class="h4-like\s+h4-like--emphase"\s*>\s*(?P<publication>.*?)\s*</p>',
    re.DOTALL,
)

#   <p class="h4-like">Chambre criminelle
#                   -
#       Formation restreinte hors RNSM/NA
#               </p>
formation_re = re.compile(
    r'<p\s+class="h4-like"\s*>\s*Chambre criminelle\s*-\s*(?P<formation>.*?)\s*</p>',
    re.DOTALL,
)
ecli_re = re.compile(r"<p>(?P<ecli>ECLI:.*?)</p>")
