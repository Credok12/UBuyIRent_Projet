from models import *
from core import TypeBail, InvalidDataException
from users import *
from datetime import date

# ─────────────────────────────────────────────
# Démonstration simple principale
# ─────────────────────────────────────────────
def main():
    print("=== Démonstration principale ===\n")

    # Création des utilisateurs
    clerk = LeaseClerk(1, "Nom1", "clerk")
    manager = LeaseManager(2, "Nom2", "manager")
    supervisor = LeaseManagerSupervisor(3, "Nom3", "supervisor")

    # Création d’une unité
    unit = Unit("Appartement 101", "Canada", "Québec", "Résidentiel", 2, 1, True, True, -73.5673, 45.5017)
    print("Unité créée :", unit.nom)
    print("Unit valide ?", unit.estValide())

    # Création d’un propriétaire
    landlord = Landlord("Mr1")
    landlord.ajouterUnite(unit)

    # Création d’un contrat
    contrat = LeaseContract(landlord, TypeBail.STUDENT, "Contrat pour étudiants")
    landlord.ajouterContrat(contrat)

    # Affectation de l’unité au contrat
    assignment = UnitAssignment(unit, contrat, 1200, date(2024, 5, 1), date(2025, 5, 1))
    contrat.ajouterAffectation(assignment)

    # Affichage des résultats
    print(f"Montant total du contrat : {assignment.calculerMontantTotal()} $")
    print(f"Prochaine facture estimée : {assignment.calculerFactureEstimee()}")


# ─────────────────────────────────────────────
# Simulation des rôles utilisateurs
# ─────────────────────────────────────────────
def jeu_essai_roles():
    print("\n=== Simulation des rôles ===\n")

    # Utilisateurs simulés
    clerk = LeaseClerk(4, "Nom4", "clerk")
    manager = LeaseManager(5, "Nom5", "manager")
    supervisor = LeaseManagerSupervisor(6, "Nom6", "supervisor")

    landlord = Landlord("Mr2")

    unit = None
    contrat = None

    # Étapes du test
    if clerk.hasPermission("creer_unit"):
        unit = Unit("Appart Test", "France", "Île-de-France", "Résidentiel", 1, 1, True, False, 2.3522, 48.8566)
        landlord.ajouterUnite(unit)
        print(f"{clerk.nom} ({clerk.role}) a créé une unité.")

    if manager.hasPermission("creer_contrat"):
        contrat = LeaseContract(landlord, TypeBail.LONG_TERM, "Bail longue durée")
        landlord.ajouterContrat(contrat)
        print(f"{manager.nom} ({manager.role}) a créé un contrat.")

    if supervisor.hasPermission("creer_affectation") and unit and contrat:
        assignment = UnitAssignment(unit, contrat, 900, date(2024, 6, 1), date(2025, 6, 1))
        contrat.ajouterAffectation(assignment)
        print(f"{supervisor.nom} ({supervisor.role}) a affecté l’unité au contrat.")


# ─────────────────────────────────────────────
# Cas d’erreurs et validations métiers
# ─────────────────────────────────────────────
def test_erreurs():
    print("\n=== Tests de cas d’erreur ===\n")

    landlord = Landlord("Mr3")

    # Unité invalide (province non reconnue)
    mauvaise_unite = Unit("Villa 404", "France", "Bretagne", "Résidentiel", 2, 1, True, True, 1.0, 1.0)
    print("Unité valide ?", mauvaise_unite.estValide())  # False attendu

    # Création d’une unité correcte
    unite = Unit("Studio Test", "Canada", "Québec", "Résidentiel", 1, 1, True, True, -73.5, 45.5)
    landlord.ajouterUnite(unite)

    # Contrat vide (aucune affectation)
    contrat_vide = LeaseContract(landlord, TypeBail.SHORT_TERM, "Contrat sans unité")
    if not contrat_vide.liste_affectations:
        print("Contrat vide détecté (aucune unité affectée)")

    # Affectation en double : même unité affectée 2 fois sur la même période
    contrat = LeaseContract(landlord, TypeBail.STUDENT, "Contrat doublon test")
    landlord.ajouterContrat(contrat)

    assignment1 = UnitAssignment(unite, contrat, 1000, date(2024, 6, 1), date(2025, 6, 1))
    contrat.ajouterAffectation(assignment1)

    try:
        assignment2 = UnitAssignment(unite, contrat, 950, date(2024, 7, 1), date(2025, 6, 1))
        contrat.ajouterAffectation(assignment2)
    except InvalidDataException as e:
        print(f"Erreur détectée : {e}")


# ─────────────────────────────────────────────
# Exécution principale
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
    jeu_essai_roles()
    test_erreurs()
