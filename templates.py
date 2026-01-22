class UnitTemplate:
    def __init__(self, name, tanks, apc, trucks, soldiers, speed, tank_power, apc_power, inf_power):
        self.name = name
        self.tanks = tanks
        self.apc = apc
        self.trucks = trucks
        self.soldiers = soldiers
        self.speed = speed
        self.tank_power = tank_power
        self.apc_power = apc_power
        self.inf_power = inf_power

TEMPLATES = {
    "PACT": {
        # Batalion Pancerny T-72A: Dużo czołgów, solidna siła ognia, ale słabsze APC (MT-LB/BTR)
        "PANCERNY": UnitTemplate("Batalion Pancerny T-72A", 54, 6, 10, 300, 1.2, 2.4, 0.4, 0.05),
        # Pułk Piechoty: Ogromna liczba ludzi, bardzo wolni, brak czołgów, słaba siła ognia APC
        "PIECHOTA": UnitTemplate("Pułk Piechoty", 0, 20, 100, 1200, 0.6, 0.0, 0.3, 0.12),
        # Zmechanizowany: Balans. BMP-1/2 dają dużą siłę ognia APC (rakiety kornet/fagot)
        "ZMECHANIZOWANY": UnitTemplate("Batalion Zmechanizowany", 15, 40, 40, 400, 1.0, 2.0, 1.1, 0.10),
    },
    "NATO": {
        # Abrams: Mniej czołgów niż u PACT, ale potężna siła ognia (celność i pancerz)
        "PANCERNY": UnitTemplate("Batalion Pancerny M1 Abrams", 45, 8, 10, 300, 1.3, 3.5, 0.5, 0.05),
        # Batalion Piechoty: Mniej ludzi niż PACT, ale lepiej wyszkoleni (wyższy inf_power)
        "PIECHOTA": UnitTemplate("Batalion Piechoty", 0, 20, 90, 1100, 0.5, 0.0, 0.8, 0.15),
        # Zmechanizowany NATO: Transportery Bradley/Marder mają bardzo silne działka/rakiety
        "ZMECHANIZOWANY": UnitTemplate("Batalion Zmechanizowany", 14, 40, 80, 350, 1.1, 2.5, 1.3, 0.12)
    }
}