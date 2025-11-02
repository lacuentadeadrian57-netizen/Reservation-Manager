from typing import Any
from datetime import datetime, date
from loader import load_data, save_data

def code_to_id(code: str) -> int:
    return int(code.replace("RES-", ""))

def id_to_code(num: int) -> str:
    return f"RES-{num:03d}"

class Manager:
    def __init__(self):
        self.price : dict[str, int] = {}
        self.quantity : dict[str, int] = {}
        self.resources : list[str] = []
        self.locations : list[str] = []
        self.requisites : dict[str, list[str]] = {}
        self.optionals : dict[str, list[str]] = {}
        self.reservations : list[dict[str, Any]] = []

        self.last_id = "RES-0"
        self.id_map = {}
    
    def calculate_price(self, start : date, end : date, location : str, optionals : list[str]):
        delta = (end - start).days + 1
        total = self.price[location]
        for requisite in self.requisites[location]:
            total += self.price[requisite]
        for optional in optionals:
            total += self.price[optional]
        return total * delta
    
    def stock(self, inventory : dict[str , int], reservation : dict[str, Any]):
        for optional in reservation["optionals"]:
            if not optional in inventory:
                inventory[optional] = 1
            else:
                inventory[optional] += 1
        for requisite in self.requisites[reservation["location"]]:
            if not requisite in inventory:
                inventory[requisite] = 1
            else:
                inventory[requisite] += 1

    def insert(self, reservation, reservations : list, property = "start"):
        first = reservation[property]
        left, right = 0, len(self.reservations)
        while left < right:
            half = (left + right) // 2
            if first < self.reservations[half][property]:
                right = half
            else:
                left = half + 1
        reservations.insert(left, reservation)

    def refresh(self):
        collitions = []
        i = 0
        while i < len(self.reservations):
            reservation = self.reservations[i]
            for j in range(len(collitions) - 1, -1, -1):
                if collitions[j]["end"] <= reservation["start"]:
                    collitions = collitions[j + 1:]
                    break
            collide = None
            inventory = {}
            self.stock(inventory, reservation)
            for collition in reversed(collitions):
                if collition["location"] == reservation["location"]:
                    collide = collition
                    break
                else:
                    self.stock(inventory, collition)
                    for item in inventory:
                        if self.quantity[item] < inventory[item]:
                            collide = collition
                            break
                    if collide:
                        break
            if collide:
                del self.reservations[i]
                reservation["end"] = collide["end"] + (reservation["end"] - reservation["start"])
                reservation["start"] = collide["end"]
                self.insert(reservation, self.reservations)
            else:
                self.insert(reservation, collitions, "end")
                i += 1
  
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
        self.id_map[self.last_id] = _reserve


        self.insert(_reserve, self.reservations)
        self.refresh()
        if(_reserve["start"] != start):
            return True, f"Reservation added in start: {_reserve["start"]}, end: {_reserve["end"]}" 
        return True, "Reservation added!"    
    
    def delete_reservation(self, id):
        reservations = []
        for reservation in self.reservations:
            if(id != reservation["ID"]):
                reservations.append(reservation)
        self.reservations = reservations
        del self.id_map[id]

    def add_resource(self, name : str, quantity : int, price : int):
        if name in self.resources:
            return False, f"Resource {name} already tracked"
        self.resources.append(name)
        self.quantity[name] = quantity
        self.price[name] = price
        return True, "Operation Succeded"
    
    def delete_resource(self, name : str):
        if name in self.resources:
            reservations = []
            for reservation in self.reservations:
                location = reservation["location"]
                if not name in self.requisites[location]:
                    if name in reservation["optionals"]:
                        reservation["optionals"].remove(name)
                    reservations.append(reservation)
            self.reservations = reservations
            locations = []
            for location in self.locations:
                if not name in self.requisites[location]:
                    if name in self.optionals[location]:
                        self.optionals[location].remove(name)
                    locations.append(location)
                else:
                    del self.requisites[location]
            self.locations = locations
            del self.quantity[name]
            del self.price[name]
            self.resources.remove(name)
    
    def add_location(self, name : str, price : int, requisites : list[str], optionals : list[str]):
        if name in self.locations:
            return False, f"Location {name} already tracked"
        self.locations.append(name)
        self.price[name] = price
        self.requisites[name] = requisites
        self.optionals[name] = optionals
        return True, "Operation Succeded"
    
    def delete_location(self, name : str):
        if name in self.locations:
            reservations = []
            for reservation in self.reservations:
                if reservation["location"] != name:
                    reservations.append(reservation)
            self.reservations = reservations
            del self.price[name]
            del self.requisites[name]
            del self.optionals[name]
            self.locations.remove(name) 

    def update_price(self, name : str, value : int):
        if value > 0:
           self.price[name] = value
    
    def update_quantity(self, name : str, value : int):
        if value > 0:
            self.quantity[name] = value
            if value < self.quantity[name]:
                self.refresh()
            
    def save(self, filename : str):
        data = {
            "price" : self.price,
            "quantity" : self.quantity,
            "resources" : self.resources,
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
            self.price = data["price"]
            self.quantity = data["quantity"]
            self.resources = data["resources"]
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
