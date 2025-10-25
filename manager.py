from typing import Any
from datetime import datetime, date
from loader import load_data, save_data

def code_to_id(code: str) -> int:
    return int(code.replace("RES-", ""))

def id_to_code(num: int) -> str:
    return f"RES-{num:03d}"

class Manager:
    def __init__(self):
        self.inventory : list[str] = []
        self.properties : dict[str, list] = {}
        self.locations : list[str] = []
        self.requisites : dict[str, list[str]] = {}
        self.reservations : list[dict[str, Any]] = []

        self.last_id = "RES-0"
        self.id_map = {}
    
    def add_reservation(self, start : date, end : date, location : str):
        if start > end:
            return False, "Validation failed: the start date cannot be after the end date"
        elif start < datetime.now().date():
            return False, "Validation failed: the start date cannot be before the actual date"

        self.last_id = id_to_code(code_to_id(self.last_id) + 1)
        _reserve = {
            "ID_name": self.last_id,
            "start_date": start,
            "end_date": end,
            "location": location
        }
        nearest = self.find_spot(_reserve)
        if nearest[0] != start or nearest[1] != end:
            return False, f"Reservation colides: available date: {start.isoformat()}-{end.isoformat()}"
        
        self.id_map[self.last_id] = _reserve
        self.insert_reservation(_reserve)
        return True, "Reservation added!"    
    
    def calculate_price(self, start : date, end : date, location : str):
        total = 0
        for requisite in self.requisites[location]:
            rel_price = self.properties[requisite][1]
            delta = end - start
            total += (delta.days + 1) * rel_price
        return total
        
    
    def find_spot(self, reserve):
        best = (reserve["start_date"], reserve["end_date"])
        collitions = {}
        for _reserve in self.reservations:
            interval = (_reserve["start_date"], _reserve["end_date"])
            # Add the intersection calculation
            intersect = False
            if intersect:
                requisites = self.requisites[_reserve["location"]]
                for requisite in requisites:
                    if requisite in collitions:
                        collitions[requisite] += 1
                    else:
                        collitions[requisite] = 1
                collides = _reserve["location"] == reserve["location"]
                if not collides:
                    for key in collitions:
                        if collitions[key] > self.properties[key][0]:
                            collides = True
                            break
                if collides:
                    best = (interval[1], best[1] - best[0] + interval[1])
                    collitions = {}
        return best

    def insert_reservation(self, reserve):
        start = reserve["start_date"]
        left, right = 0, len(self.reservations)
        while left < right:
            half = (left + right) // 2
            if start < self.reservations[half]["start_date"]:
                right = half
            else:
                left = half + 1
        self.reservations.insert(left, reserve)
  
    def delete_reservation(self, id):
        reservations = []
        for r in self.reservations:
            if(id != r["ID_name"]):
                reservations.append(r)
        self.reservations = reservations
        del self.id_map[id]

    def save(self, filename : str):
        data = {
            "inventory" : self.inventory,
            "properties" : self.properties,
            "locations" : self.locations,
            "requisites" : self.requisites,
            "reservations" : []
        }
        for reserve in self.reservations:
            _reserve = {
                "ID_name": reserve["ID_name"],
                "start_date": reserve["start_date"].isoformat(),
                "end_date": reserve["end_date"].isoformat(),
                "location": reserve["location"]
            }
            data["reservations"].append(_reserve)
        return save_data(data, filename)


    def load(self, filename : str):
        data = load_data(filename)
        if data:
            self.inventory = data["inventory"]
            self.properties = data["properties"]
            self.locations = data["locations"]
            self.requisites = data["requisites"]
            self.reservations = []
            for reserve in data["reservations"]:
                _reserve = {                
                    "ID_name": reserve["ID_name"],
                    "start_date": date.fromisoformat(reserve["start_date"]),
                    "end_date": date.fromisoformat(reserve["end_date"]),
                    "location": reserve["location"]
                }
                self.id_map[_reserve["ID_name"]] = _reserve
                if (code_to_id(reserve["ID_name"]) > code_to_id(self.last_id)):
                    self.last_id = reserve["ID_name"]
                self.reservations.append(_reserve)
            return True
        return False
