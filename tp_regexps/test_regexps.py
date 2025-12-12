import json
import os
import unittest
from pathlib import Path

from tp_regexps import regexps
from tp_regexps.decision import Decision


class TestRegexps(unittest.TestCase):

    @staticmethod
    def __iterate_on_decisions():
        reference_name = os.getenv("TP_REGEXP_TEST_REF", "data")
        print(reference_name)
        decisions_path = Path(__file__).parent / "data" / "ccass"
        reference_path = Path(__file__).parent / reference_name / "ccass"
        for filename in sorted(os.listdir(decisions_path)):
            if filename.endswith(".html"):
                id = filename[:-5]
                json_path = os.path.join(reference_path, filename[:-5] + ".json")
                html_path = os.path.join(decisions_path, filename)
                if os.path.exists(html_path):
                    with open(html_path, "r", encoding="utf-8") as f:
                        html_data = f.read()
                    with open(json_path, "r", encoding="utf-8") as f:
                        json_data = f.read()
                    reference_decision = Decision.from_json(json_data)
                    html_decision = Decision.from_html(id, html_data)
                    yield id, reference_decision, html_decision

    def test_chamber(self):
        """Récupération de la chambre"""
        for id, reference_decision, html_decision in self.__iterate_on_decisions():
            with self.subTest(id, id=id):
                self.assertEqual(reference_decision.chamber, html_decision.chamber, id)

    # TODO: uncomment
    def test_ecli(self):
       """Récupération du numéro ECLI"""
       for id, reference_decision, html_decision in self.__iterate_on_decisions():
           with self.subTest(id, id=id):
               self.assertEqual(reference_decision.ecli, html_decision.ecli, id)

    # TODO: uncomment
    def test_publication(self):
       """Récupération de la publication"""
       for id, reference_decision, html_decision in self.__iterate_on_decisions():
           with self.subTest(id, id=id):
               self.assertEqual(reference_decision.publication, html_decision.publication, id)

    # TODO: uncomment
    #def test_formation(self):
    #    """Récupération de la formation"""
    #    for id, reference_decision, html_decision in self.__iterate_on_decisions():
    #        with self.subTest(id, id=id):
    #            self.assertEqual(reference_decision.formation, html_decision.formation, id)

    # TODO: number, decision_date, ...
