from abc import ABC, abstractmethod
from core import PermissionDeniedException, TypeBail
from models import Unit, LeaseContract, UnitAssignment


class Utilisateur(ABC):
    def __init__(self, id, nom, role):
        self.id = id
        self.nom = nom
        self.role = role

    def __str__(self):
        return f"{self.nom} ({self.role})"

    @abstractmethod
    def hasPermission(self, action):
        pass

    def creer_unite(self, *args, **kwargs):
        raise PermissionDeniedException(f"{self.role} ne peut pas créer une unité.")

    def creer_contrat(self, *args, **kwargs):
        raise PermissionDeniedException(f"{self.role} ne peut pas créer un contrat.")

    def creer_affectation(self, *args, **kwargs):
        raise PermissionDeniedException(f"{self.role} ne peut pas affecter une unité.")


class LeaseClerk(Utilisateur):
    def hasPermission(self, action):
        return action in ["creer_unite", "creer_affectation"]

    def creer_unite(self, *args, **kwargs):
        return Unit(*args, **kwargs)

    def creer_affectation(self, unit, contrat, loyer, debut, fin):
        return UnitAssignment(unit, contrat, loyer, debut, fin)


class LeaseManager(LeaseClerk):  
    def hasPermission(self, action):
        return super().hasPermission(action) or action in ["creer_contrat", "modifier_unite"]

    def creer_contrat(self, landlord, type_bail, notes):
        return LeaseContract(landlord, type_bail, notes)

    def modifier_unite(self, unite, **kwargs):
        for attr, val in kwargs.items():
            if hasattr(unite, attr):
                setattr(unite, attr, val)


class LeaseManagerSupervisor(LeaseManager):  
    def hasPermission(self, action):
        return F"Accès total"

    def supprimer_unite(self, unite, landlord):
        if unite in landlord.liste_unites:
            landlord.liste_unites.remove(unite)
            print(f"Unité {unite.nom} supprimée.")

    def supprimer_contrat(self, contrat, landlord):
        if contrat in landlord.liste_contrats:
            landlord.liste_contrats.remove(contrat)
            print(f"Contrat {contrat.id} supprimé.")

    def supprimer_affectation(self, affectation, contrat):
        if affectation in contrat.liste_affectations:
            contrat.liste_affectations.remove(affectation)
            print(f"Affectation {affectation.id} supprimée.")
