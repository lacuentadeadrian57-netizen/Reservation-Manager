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
        self.price : dict[str, int] = {}
        self.quantity : dict[str, int] = {}
        self.locations : list[str] = []
        self.requisites : dict[str, list[str]] = {}
        self.optionals : dict[str, list[str]] = {}
        self.reservations : list[dict[str, Any]] = []

        self.last_id = "RES-0"
        self.id_map = {}
    
    def add_reservation(self, start : date, end : date, location : str, optionals : list[str]):
        if start > end:
            return False, "Validation failed: the start date cannot be after the end date"
        elif start < datetime.now().date():
            return False, "Validation failed: the start date cannot be before the actual date"
        for option in optionals:
            if not option in self.optionals[location]:
                return False, f"Validation failed: the selected option {option} is invalid"
            
        self.last_id = id_to_code(code_to_id(self.last_id) + 1)
        _reserve = {
            "ID": self.last_id,
            "start": start,
            "end": end,
            "location": location,
            "optionals": optionals
        }
        nearest = self.find_spot(_reserve)
        if nearest[0] != start or nearest[1] != end:
            return False, f"Reservation colides: available date: {start.isoformat()}-{end.isoformat()}"
        
        self.id_map[self.last_id] = _reserve
        self.insert_reservation(_reserve)
        return True, "Reservation added!"    
    
    def calculate_price(self, start : date, end : date, location : str, optionals : list[str]):
        delta = (end - start).days + 1
        total = self.price[location]
        print(f" price: {self.price[location]} from: {location} total: {total}")
        for requisite in self.requisites[location]:
            total += self.price[requisite]
            print(f" price: {self.price[requisite]} from: {requisite} total: {total}")
        for optional in optionals:
            total += self.price[optional]
            print(f" price: {self.price[optional]} from: {optional} total: {total}")
        print(f"delta: {delta}")
        return total * delta
    
    def find_spot(self, reserve):
        best = (reserve["start"], reserve["end"])
        collitions = {}
        for _reserve in self.reservations:
            interval = (_reserve["start"], _reserve["end"])
            # Add the intersection calculation
            intersect = False
            if intersect:
                for requisite in self.requisites[_reserve["location"]]:
                    if requisite in collitions:
                        collitions[requisite] += 1
                    else:
                        collitions[requisite] = 1
                for optional in reserve.optionals:
                    if optional in collitions:
                        collitions[optional] += 1
                    else:
                        collitions[optional] = 1
                collides = _reserve["location"] == reserve["location"]
                if not collides:
                    for key in collitions:
                        if collitions[key] > self.quantity[key]:
                            collides = True
                            break
                if collides:
                    best = (interval[1], best[1] - best[0] + interval[1])
                    collitions = {}
        return best

    def insert_reservation(self, reserve):
        start = reserve["start"]
        left, right = 0, len(self.reservations)
        while left < right:
            half = (left + right) // 2
            if start < self.reservations[half]["start"]:
                right = half
            else:
                left = half + 1
        self.reservations.insert(left, reserve)
  
    def delete_reservation(self, id):
        reservations = []
        for r in self.reservations:
            if(id != r["ID"]):
                reservations.append(r)
        self.reservations = reservations
        del self.id_map[id]

    def save(self, filename : str):
        data = {
            "inventory" : self.inventory,
            "price" : self.price,
            "quantity" : self.quantity,
            "locations" : self.locations,
            "requisites" : self.requisites,
            "optionals" : self.optionals,
            "reservations" : []
        }
        for reserve in self.reservations:
            _reserve = {
                "ID": reserve["ID"],
                "start": reserve["start"].isoformat(),
                "end": reserve["end"].isoformat(),
                "location": reserve["location"],
                "optionals": reserve["optionals"]
            }
            data["reservations"].append(_reserve)
        return save_data(data, filename)

    def load(self, filename : str):
        data = load_data(filename)
        if data:
            self.inventory = data["inventory"]
            self.price = data["price"]
            self.quantity = data["quantity"]
            self.locations = data["locations"]
            self.requisites = data["requisites"]
            self.optionals = data["optionals"]
            self.reservations = []
            for reserve in data["reservations"]:
                _reserve = {                
                    "ID": reserve["ID"],
                    "start": date.fromisoformat(reserve["start"]),
                    "end": date.fromisoformat(reserve["end"]),
                    "location": reserve["location"],
                    "optionals": reserve["optionals"]
                }
                self.id_map[_reserve["ID"]] = _reserve
                if (code_to_id(reserve["ID"]) > code_to_id(self.last_id)):
                    self.last_id = reserve["ID"]
                self.reservations.append(_reserve)
            return True
        return False
