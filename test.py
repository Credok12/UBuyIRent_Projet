import unittest
from datetime import date
from core import TypeBail, InvalidDataException
from models import Unit, LeaseContract, UnitAssignment, Landlord
from users import LeaseClerk, LeaseManager, LeaseManagerSupervisor

class TestSystemeLocation(unittest.TestCase):

    def test_unite_valide(self):
        u = Unit("Test Unit", "Canada", "Québec", "Résidentiel", 1, 1, True, False, -73.5, 45.5)
        self.assertTrue(u.estValide())

    def test_unite_invalide(self):
        u = Unit("Bad Unit", "France", "Bretagne", "Résidentiel", 1, 1, True, False, 1.0, 1.0)
        self.assertFalse(u.estValide())

    def test_creation_par_clerk(self):
        clerk = LeaseClerk(1, "Alice", "clerk")
        unit = clerk.creer_unite("Studio", "Canada", "Québec", "Résidentiel", 1, 1, True, True, -73.5, 45.5)
        self.assertIsInstance(unit, Unit)

    def test_contrat_par_manager(self):
        manager = LeaseManager(2, "Bob", "manager")
        landlord = Landlord("Owner")
        contrat = manager.creer_contrat(landlord, TypeBail.LONG_TERM, "Long term contract")
        self.assertIsInstance(contrat, LeaseContract)

    def test_affectation_double(self):
        landlord = Landlord("Owner")
        unite = Unit("Studio", "Canada", "Québec", "Résidentiel", 1, 1, True, True, -73.5, 45.5)
        contrat = LeaseContract(landlord, TypeBail.STUDENT, "Test doublon")
        assignment1 = UnitAssignment(unite, contrat, 1000, date(2024, 6, 1), date(2025, 6, 1))
        contrat.ajouterAffectation(assignment1)

        assignment2 = UnitAssignment(unite, contrat, 950, date(2024, 7, 1), date(2025, 6, 1))

        with self.assertRaises(InvalidDataException):
            contrat.ajouterAffectation(assignment2)

    def test_supprimer_unite_par_supervisor(self):
        supervisor = LeaseManagerSupervisor(3, "Charlie", "supervisor")
        landlord = Landlord("Owner")
        unite = supervisor.creer_unite("Loft", "Canada", "Québec", "Commercial", 1, 2, False, True, -73.5, 45.5)
        landlord.ajouterUnite(unite)
        self.assertIn(unite, landlord.liste_unites)

        supervisor.supprimer_unite(unite, landlord)
        self.assertNotIn(unite, landlord.liste_unites)

if __name__ == '__main__':
    unittest.main()
