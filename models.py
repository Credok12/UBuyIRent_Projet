from core import *
from datetime import date, timedelta

class Unit:
    _id_gen = 1

    def __init__(self, nom, pays, etat_province, classe, nb_chambres, nb_sdb, wifi, clim, longitude, latitude):
        self.id = Unit._id_gen
        Unit._id_gen += 1
        self.nom = nom
        self.pays = pays
        self.etat_province = etat_province
        self.classe = classe
        self.nb_chambres = nb_chambres
        self.nb_sdb = nb_sdb
        self.wifi = wifi
        self.clim = clim
        self.longitude = longitude
        self.latitude = latitude

    def afficherDetails(self):
        return vars(self)

    def genererLienGoogleMaps(self):
        return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"

    def estValide(self):
        return (
            self.pays in CORRESPONDANCE_PROVINCES and
            self.etat_province in CORRESPONDANCE_PROVINCES[self.pays] and
            self.nb_chambres > 0 and self.nb_sdb > 0
        )

class Landlord:
    _id_gen = 1

    def __init__(self, nom):
        self.id = Landlord._id_gen
        Landlord._id_gen += 1
        self.nom = nom
        self.liste_unites = []
        self.liste_contrats = []

    def ajouterUnite(self, unite):
        self.liste_unites.append(unite)

    def ajouterContrat(self, contrat):
        self.liste_contrats.append(contrat)

class LeaseContract:
    _id_seq = 1000

    def __init__(self, landlord, type_bail: TypeBail, notes):
        self.id = f"LEACON-{LeaseContract._id_seq}"
        LeaseContract._id_seq += 1
        self.landlord = landlord
        self.type_bail = type_bail
        self.notes = notes if len(notes) <= 4000 else notes[:4000]
        self.liste_affectations = []

    def ajouterAffectation(self, affectation):
        for a in self.liste_affectations:
            if a.unit == affectation.unit and a.estEnCours():
                raise InvalidDataException("Unité déjà affectée à un contrat actif.")
        self.liste_affectations.append(affectation)

class UnitAssignment:
    _id_seq = 1

    def __init__(self, unit, contrat, loyer_mensuel, date_debut, date_fin):
        self.id = f"UNIT-{UnitAssignment._id_seq:06d}-ASS"
        UnitAssignment._id_seq += 1
        self.unit = unit
        self.contrat = contrat
        self.loyer_mensuel = loyer_mensuel
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.date_prochaine_facture = date_debut
        self.factures_precedentes = []

    def calculerMontantTotal(self):
        nb_mois = (self.date_fin.year - self.date_debut.year) * 12 + (self.date_fin.month - self.date_debut.month)
        return nb_mois * self.loyer_mensuel

    def estEnCours(self):
        return self.date_debut <= date.today() <= self.date_fin

    def calculerFactureEstimee(self):
        if self.factures_precedentes:
            derniere_date = self.factures_precedentes[-1]
        else:
            derniere_date = self.date_prochaine_facture
        prochaine = derniere_date + timedelta(days=30)
        return prochaine
