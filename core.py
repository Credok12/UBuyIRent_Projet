from enum import Enum

class TypeBail(Enum):
    LONG_TERM = "Long-Term"
    SHORT_TERM = "Short-Term"
    STUDENT = "Student"
    
    
CORRESPONDANCE_PROVINCES = {
    "Canada": ["Québec", "Ontario", "Colombie-Britannique", "Alberta", "Manitoba"],
    "Etats-unis":["Californie", "New York", "Texas", "Floride","Pennsylvanie"],
    "Republique democratique du congo"  : ["Kinshasa", "Lubumbashi", "Kananga","Likasi", "kipushi"],
    "Afrique du sud" : ["Pretoria", "Johannesburg", "Durban", "Cape Town", "Port Elizabeth"],
}

class PermissionDeniedException(Exception):
    pass

class InvalidDataException(Exception):
    pass
