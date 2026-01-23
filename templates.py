class UnitTemplate:
    def __init__(self, name, tanks, apc, trucks, soldiers, speed, tank_power, apc_power, inf_power, rank):
        self.name = name; 
        self.tanks = tanks; 
        self.apc = apc; 
        self.trucks = trucks; 
        self.soldiers = soldiers; 
        self.speed = speed; 
        self.tank_power = tank_power; 
        self.apc_power = apc_power; 
        self.inf_power = inf_power; 
        self.rank = rank
        
    def get_firepower(self):
        return round(self.tanks * self.tank_power + self.apc * self.apc_power + self.soldiers * self.inf_power, 0)

TEMPLATES = {
    "PACT": {
        "PANCERNY": UnitTemplate("Batalion Pancerny T-72A", 54, 6, 10, 300, 1.2, 2.4, 0.4, 0.05, 2),
        "ZMECHANIZOWANY": UnitTemplate("Batalion Zmechanizowany", 15, 40, 40, 400, 1.0, 2.0, 1.1, 0.10, 2),
        "KOMPANIA_PANC": UnitTemplate("Kompania Pancerna T-72A", 18, 2, 3, 100, 1.2, 2.4, 0.4, 0.05, 1),
        "KOMPANIA_ZMECH": UnitTemplate("Kompania Zmechanizowana", 5, 13, 13, 130, 1.0, 2.0, 1.1, 0.10, 1),
        "PIECHOTA": UnitTemplate("Pułk Piechoty", 0, 20, 100, 1200, 0.6, 0.0, 0.3, 0.12, 2),
    },
    "NATO": {
        "PANCERNY": UnitTemplate("Batalion Pancerny M1 Abrams", 45, 8, 10, 300, 1.3, 3.5, 0.5, 0.05, 2),
        "ZMECHANIZOWANY": UnitTemplate("Batalion Zmechanizowany", 14, 40, 80, 350, 1.1, 2.5, 1.3, 0.12, 2),
        "KOMPANIA_PANC": UnitTemplate("Kompania Pancerna Abrams", 15, 3, 3, 100, 1.3, 3.5, 0.5, 0.05, 1),
        "KOMPANIA_ZMECH": UnitTemplate("Kompania Zmechanizowana", 5, 13, 26, 115, 1.1, 2.5, 1.3, 0.12, 1),
        "PIECHOTA": UnitTemplate("Batalion Piechoty", 0, 20, 90, 1100, 0.5, 0.0, 0.8, 0.15, 2),
    }
}