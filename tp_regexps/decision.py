import json

from . import regexps


class Decision(object):
    """Décision de la Cour de Cassation."""

    def __init__(
        self,
        id,
        chamber=None,
        number=None,
        formation=None,
        publication=None,
        ecli=None,
        decision_date=None,
        solution=None,
        texts=None,
        content=None,
    ):
        self.kind = "decision"
        self.id = id
        self.chamber = chamber
        self.number = number
        self.formation = formation
        self.publication = publication
        self.ecli = ecli
        self.decision_date = decision_date
        self.solution = solution
        self.texts = texts
        self.content = content

    def to_dict(self):
        return {
            "kind": self.kind,
            "id": self.id,
            "chamber": self.chamber,
            "formation": self.formation,
            "publication": self.publication,
            "number": self.number,
            "ecli": self.ecli,
            "decision_date": self.decision_date,
            "solution": self.solution,
            "content": self.content,
            "texts": self.texts,
        }

    @staticmethod
    def custom_to_json(obj):
        if isinstance(obj, Zone):
            return obj.to_dict()
        raise TypeError(f"Cannot serialize object of {type(obj)}")

    def to_json(self):
        return json.dumps(
            self.to_dict(), indent=2, ensure_ascii=False, default=self.custom_to_json
        )

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            id=d.get("id"),
            chamber=d.get("chamber"),
            formation=d.get("formation"),
            publication=d.get("publication"),
            ecli=d.get("ecli"),
            number=d.get("number"),
            decision_date=d.get("decision_date"),
            solution=d.get("solution"),
            texts=d.get("texts"),
            content=d.get("content"),
        )

    @classmethod
    def from_json(cls, s: str):
        d = json.loads(s)
        if d.get("content"):
            new_content = list()
            for zone in d["content"]:
                new_content.append(Zone.from_dict(zone))
            d["content"] = new_content
        return cls.from_dict(d)

    @staticmethod
    def __get_ecli(data: str):
        m = regexps.ecli_re.search(data)
        if m:
            return m.group("ecli")
        return None
    
    @staticmethod
    def __get_chamber(data: str):
        m = regexps.chamber_re.search(data)
        if m:
            return m.group("chamber")
        return None
    
    @staticmethod
    def __get_formation(data: str):
        m = regexps.formation_re.search(data)
        if m:
            return m.group("formation")
        return None
    
    @staticmethod
    def __get_publication(data: str):
        m = regexps.publication_re.search(data)
        if m:
            return m.group("publication").replace("  ", "").replace("\n", "") or None
        return None
    
    @staticmethod
    def __get_number(data: str):
        m = regexps.number_re.search(data)
        if m:
            return m.group("number")
        return None
    
    @staticmethod
    def __get_decision_date(data: str):
        french_months = {
            "janvier": "01",
            "février": "02",
            "mars": "03",
            "avril": "04",
            "mai": "05",
            "juin": "06",
            "juillet": "07",
            "août": "08",
            "septembre": "09",
            "octobre": "10",
            "novembre": "11",
            "décembre": "12"
        }

        m = regexps.decision_date_re.search(data)
        if m:
            day = m.group("day")
            if len(day) == 1:
                day = '0' + day
                
            month = m.group("month")
            year = m.group("year")

            return '-'.join([year, french_months[month], day])

        return None
    
    @staticmethod
    def __get_solution(data: str):
        m = regexps.solution_re.search(data)
        if m:
            return m.group("solution")
        return None
    
    @staticmethod
    def __get_content(data: str):
        m = regexps.content_re.search(data)
        if m:
            return m.group("content")
        return None
    
    @staticmethod
    def __get_texts(data: str):
        m = regexps.texts_re.search(data)
        if m:
            return m.group("texts")
        return None

    @classmethod
    def from_html(cls, id: str, html: str):
        d = cls(id=id)
        d.ecli = cls.__get_ecli(html)
        d.chamber = cls.__get_chamber(html)
        d.formation = cls.__get_formation(html)
        d.publication = cls.__get_publication(html)
        d.number = cls.__get_number(html)
        d.decision_date = cls.__get_decision_date(html)
        d.solution = cls.__get_solution(html)
        d.content = cls.__get_content(html)
        d.texts = cls.__get_texts(html)
        return d


class Zone(object):
    """Zone d'une décision.

    Exemples:

            {
                    "kind": "ENTETE",
                    "paragraphs": [
                            "N° M 24-82.423 F-B",
                            "N° 01492",
                            "MAS2",
                            "10 DÉCEMBRE 2024",
                            "CASSATION",
                            "M. BONNAL président,",
                            "R É P U B L I Q U E F R A N Ç A I S E",
                            "________________________________________",
                            "AU NOM DU PEUPLE FRANÇAIS",
                            "_________________________",
                            "ARRÊT DE LA COUR DE CASSATION, CHAMBRE CRIMINELLE,",
                            "DU 10 DÉCEMBRE 2024"
                    ]
            },
            {
                    "kind": "INTRODUCTION",
                    "paragraphs": [
                            "M. [B] [J] a formé un pourvoi contre l'arrêt de la chambre de l'instruction de la cour d'appel de Versailles, en date du 26 mars 2024, qui, dans l'information suivie contre lui des chefs de meurtre et tentative, destruction par un moyen dangereux, en bande organisée, et association de malfaiteurs, a déclaré irrecevable sa demande d'annulation de pièces de la procédure.",
                            "Par ordonnance du 5 août 2024, le président de la chambre criminelle a prescrit l'examen immédiat du pourvoi.",
                            "Un mémoire et des observations complémentaires ont été produits.",
                            "Sur le rapport de Mme Chaline-Bellamy, conseiller, les observations de Me Laurent Goldman, avocat de M. [B] [J], et les conclusions de M. Tarabeux, avocat général, après débats en l'audience publique du 13 novembre 2024 où étaient présents M. Bonnal, président, Mme Chaline-Bellamy, conseiller rapporteur, Mme Labrousse, conseiller de la chambre, et Mme Sommier, greffier de chambre,",
                            "la chambre criminelle de la Cour de cassation, composée en application de l'article 567-1-1 du code de procédure pénale, des président et conseillers précités, après en avoir délibéré conformément à la loi, a rendu le présent arrêt."
                    ]
            },
            {
                    "kind": "EXPOSE_LITIGE",
                    "paragraphs": [
                            "Faits et procédure",
                            "1. Il résulte de l'arrêt attaqué et des pièces de la procédure ce qui suit.",
                            "2. Mis en examen des chefs susvisés, M. [B] [J] a été placé sous mandat de dépôt le 3 juin 2022.",
                            "3. Par ordonnance du 22 mai 2023, le juge des libertés et de la détention a prolongé la détention provisoire."
                            "4. Par arrêt du 13 septembre 2023, la Cour de cassation a ordonné la mise en liberté d'office de M. [J] et, en application de l'article 803-7 du code de procédure pénale, l'a placé sous un contrôle judiciaire l'astreignant notamment à l'obligation de se présenter au commissariat central de police de [Localité 1] le lendemain de sa libération avant 17 heures, puis une fois par jour, et à l'interdiction de sortir des limites territoriales du département de la Seine-Saint-Denis.",
                            "5. Interpellé le 14 septembre 2023 à [Localité 2], M. [J] a été placé en garde à vue puis en rétention judiciaire avant d'être déféré. Son avocat a déposé des observations contestant la régularité de ces mesures.",
                            "6. Par ordonnance du 15 septembre 2023, le juge des libertés et de la détention a révoqué le contrôle judiciaire de M. [J] et décerné mandat de dépôt à son encontre, décision confirmée par la chambre de l'instruction le 22 septembre suivant.",
                            "7. Le 2 octobre 2023, l'avocat de M. [J] a déposé une requête en annulation du procès-verbal d'interpellation du 14 septembre précédent et de tous les actes subséquents dont il est le support nécessaire, comprenant les ordonnances de saisine du juge des libertés et de la détention, de révocation du contrôle judiciaire et de placement en détention provisoire ainsi que l'arrêt confirmatif de la chambre de l'instruction, et a sollicité la mise en liberté d'office de l'intéressé."
                    ]
            },
            {
                    "kind": "MOYENS",
                    "paragraphs": [
                            "Examen du moyen",
                            "Enoncé du moyen",
                            "8. Le moyen critique l'arrêt attaqué en ce qu'il a déclaré sa requête irrecevable, alors « que la personne mise en examen est recevable à critiquer devant la chambre de l'instruction saisie en application de l'article 173 du code de procédure pénale tous les actes de procédure contre lesquels la voie de l'appel n'est pas ouverte ; qu'en se fondant, pour déclarer irrecevable la requête de M. [J], qui visait les actes relatifs aux conditions de son interpellation, contre lesquels la voie de l'appel n'était pas ouverte, sur la circonstance inopérante qu'il ne s'agirait pas d'actes de fond et qu'ils seraient le support indissociable de la révocation du contrôle judiciaire, la chambre de l'instruction a méconnu les articles 173 et 186 du code de procédure pénale. »"
                    ]
            },
            {
                    "kind": "MOTIVATION",
                    "paragraphs": [
                            "Réponse de la Cour",
                            "Vu les articles 170 et 173, alinéa 4, du code de procédure pénale :",
                            "9. Selon le premier de ces textes, en toute matière, la chambre de l'instruction peut, au cours de l'information, être saisie aux fins d'annulation d'un acte ou d'une pièce de la procédure notamment par les parties.",
                            "10. Il résulte du second que ne peuvent faire l'objet d'une saisine de la chambre de l'instruction aux fins d'annulation les actes ou pièces de la procédure susceptibles d'un appel de la part des parties, et notamment les décisions rendues en matière de détention provisoire ou de contrôle judiciaire, à l'exception des actes pris en application du chapitre IX du titre II du livre II du code de la sécurité intérieure.",
                            "11. Pour déclarer la requête en nullité irrecevable, l'arrêt attaqué rappelle qu'en application de I'article 173, alinéa 4, du code de procédure pénale, les ordonnances rendues en matière de détention provisoire ne peuvent être contestées que par la voie de l'appel et non par celle de la requête en nullité et relève que tel a été le cas en l'espèce, la chambre de I'instruction ayant statué le 22 septembre 2023 sur l'appel interjeté contre l'ordonnance de révocation du contrôle judiciaire et de placement en détention provisoire.\n\n12. Les juges énoncent que le requérant sollicite notamment I'annulation de cette ordonnance et que, si les actes de filature, interpellation et placement en garde à vue argués d'irrégularité ne sont pas susceptibles d'appel, ils ne constituent pas des actes d'investigation sur le fond du dossier mais Ie support nécessaire et préalable à la décision de révocation du contrôle judiciaire et de placement en détention provisoire et qu'ils en sont indissociables.\n\n13. Ils ajoutent que leur annulation éventuelle n'aurait de sens et d'intérêt qu'au regard de celle des actes subséquents, et en particulier de I'ordonnance de révocation du contrôle judiciaire et de placement en détention provisoire qui n'est susceptible que d'un appel.\n\n\n14. Ils concluent qu'il appartenait au requérant de faire valoir l'irrégularité de I'ordonnance de révocation du contrôle judiciaire et de placement en détention provisoire mais également des actes qui en constituaient Ie support nécessaire et exclusif à l'occasion de I'appel formé contre ladite ordonnance, de sorte qu'il n'est désormais plus possible d'invoquer Ia nullité des actes ayant mené au placement en détention provisoire de M. [J].\n\n15. En statuant ainsi, la chambre de l'instruction a méconnu les textes susvisés et les principes ci-dessus rappelés pour les motifs qui suivent.\n\n16. Si la requête présentée sollicite l'annulation d'actes juridictionnels qui ne peuvent faire l'objet que d'un appel et est dès lors irrecevable en ce qui les concerne, elle tend au premier chef à l'annulation d'actes de la procédure, tels le procès-verbal de surveillance, de filature et d'interpellation de M. [J] ainsi que les mesures de garde à vue et de rétention qui ont suivi.\n\n17. Ces actes accomplis par des officiers ou agents de police judiciaire pour s'assurer du respect par la personne mise en examen des obligations de son contrôle judiciaire se rattachent à la procédure d'information en ce qu'ils participent de la poursuite des infractions et sont mis en oeuvre pour vérifier le respect d'une mesure prononcée en raison des nécessités de l'instruction ou à titre de mesure de sûreté. Ils entrent, en conséquence, dans le champ des actes et pièces de la procédure susceptibles de faire l'objet d'une saisine de la chambre de l'instruction aux fins d'annulation.\n\n18. De tels actes, qui ne présentent pas de caractère indissociable de l'ordonnance de révocation du contrôle judiciaire et de placement en détention provisoire, ne pouvaient en outre être contestés à l'occasion d'un appel devant la chambre de l'instruction en raison de la règle de l'unique objet de la saisine de cette juridiction.\n\n19. La cassation est par conséquent encourue.\n"
                    ]
            },
            {
                    "kind": "DISPOSITIF",
                    "paragraphs": [
                            "PAR CES MOTIFS, la Cour :",
                            "CASSE et ANNULE, en toutes ses dispositions, l'arrêt susvisé de la chambre de l'instruction de la cour d'appel de Versailles, en date du 26 mars 2024, et pour qu'il soit à nouveau jugé, conformément à la loi ;",
                            "RENVOIE la cause et les parties devant la chambre de l'instruction de la cour d'appel de Versailles, autrement composée, à ce désignée par délibération spéciale prise en chambre du conseil ;",
                            "ORDONNE l'impression du présent arrêt, sa transcription sur les registres du greffe de la chambre de l'instruction de la cour d'appel de Versailles et sa mention en marge ou à la suite de l'arrêt annulé ;",
                            "Ainsi fait et jugé par la Cour de cassation, chambre criminelle, et prononcé par le président en son audience publique du dix décembre deux mille vingt-quatre."
                    ]
            }
    """

    def __init__(self, kind, paragraphs=None):
        self.kind = kind
        self.paragraphs = paragraphs

    def to_dict(self) -> dict:
        return {"kind": self.kind, "paragraphs": self.paragraphs}

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    @classmethod
    def from_dict(cls, d: dict):
        return cls(kind=d.get("kind"), paragraphs=d.get("paragraphs"))

    @classmethod
    def from_json(cls, s: str):
        d = json.loads(s)
        return cls.from_dict(d)
