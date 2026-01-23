from templates import TEMPLATES
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_NATO, COLOR_PACT

MISSIONS_DB = {
    "NATO": [
        {
            "id": 1, "title": "STALOWA KURTYNA", "map": "fulda",
            "desc": "ZSRR uderza w luce Fulda. Utrzymaj pozycje obronne za wszelką cenę.",
            "goal": "Zniszcz wszystkie jednostki pancerne PACT.",
            "player_units": [
                ("PANCERNY", 200, 400), ("PANCERNY", 200, 600), ("KOMPANIA_ZMECH", 300, 500)
            ],
            "ai_units": [
                ("PANCERNY", 1400, 400, True), ("PANCERNY", 1400, 600, True),
                ("PANCERNY", 1000, 500, False), ("ZMECHANIZOWANY", 1100, 300, False)
            ]
        },
        {
            "id": 2, "title": "OGIEŃ NAD WISŁĄ", "map": "debe_wielkie",
            "desc": "Odwrót z Warszawy. Musisz powstrzymać desant przez rzekę.",
            "goal": "Powstrzymaj forsujące rzekę BMP.",
            "player_units": [("ZMECHANIZOWANY", 300, 500), ("PIECHOTA", 300, 700)],
            "ai_units": [("ZMECHANIZOWANY", 1500, 500, False), ("KOMPANIA_ZMECH", 1400, 300, False)]
        },
        {
            "id": 3, "title": "KOSZMAR W PORCIE", "map": "gdansk",
            "desc": "Gdańsk został odcięty. Przebij się do terminalu kontenerowego.",
            "goal": "Oczyść doki z piechoty PACT.",
            "player_units": [("PIECHOTA", 200, 500), ("PIECHOTA", 200, 300)],
            "ai_units": [("PIECHOTA", 800, 400, True), ("PIECHOTA", 900, 600, True)]
        },
        {
            "id": 4, "title": "CIENIE SIENNICY", "map": "siennica",
            "desc": "Zasadzka w lesie na kolumnę zaopatrzeniową.",
            "goal": "Zaskocz siły PACT w marszu.",
            "player_units": [("KOMPANIA_PANC", 600, 200), ("KOMPANIA_PANC", 600, 800)],
            "ai_units": [("ZMECHANIZOWANY", 1200, 500, False), ("PANCERNY", 1400, 500, False)]
        },
        {
            "id": 5, "title": "SERCE STOLICY", "map": "warszawa_zoliborz",
            "desc": "Walki uliczne na Żoliborzu. Każdy budynek to twierdza.",
            "goal": "Utrzymaj centrum dzielnicy.",
            "player_units": [("PIECHOTA", 500, 500), ("KOMPANIA_ZMECH", 400, 400)],
            "ai_units": [("PIECHOTA", 1500, 500, False), ("PIECHOTA", 1400, 300, False)]
        }
    ],
    "PACT": [
        {
            "id": 1, "title": "CZERWONY ŚWIT", "map": "fulda",
            "desc": "Operacja 'Tarcza'. Przełam umocnienia Abramsów i otwórz drogę na Frankfurt.",
            "goal": "Zmieć obronę NATO z mapy.",
            "player_units": [("PANCERNY", 200, 400), ("PANCERNY", 200, 600)],
            "ai_units": [("PANCERNY", 1400, 500, True), ("KOMPANIA_PANC", 1300, 300, True)]
        },
        {
            "id": 2, "title": "MOST DO WOLNOŚCI", "map": "debe_wielkie",
            "desc": "Zdobądź przyczółek i utrzymaj go do przybycia sił głównych.",
            "goal": "Wypchnij Marderów z Wisły.",
            "player_units": [("ZMECHANIZOWANY", 300, 500), ("KOMPANIA_ZMECH", 300, 300)],
            "ai_units": [("ZMECHANIZOWANY", 1200, 500, True), ("PIECHOTA", 1300, 700, True)]
        },
        {
            "id": 3, "title": "BURZA NAD BAŁTYKIEM", "map": "gdansk",
            "desc": "Desant morski. Opanuj infrastrukturę portową Gdańska.",
            "goal": "Zniszcz garnizon NATO.",
            "player_units": [("PIECHOTA", 100, 400), ("KOMPANIA_ZMECH", 100, 600)],
            "ai_units": [("PIECHOTA", 1000, 500, True), ("PIECHOTA", 1100, 300, True)]
        },
        {
            "id": 4, "title": "DROGA NA ZACHÓD", "map": "siennica",
            "desc": "Oczyść węzeł komunikacyjny Siennica z niedobitków NATO.",
            "goal": "Pacyfikacja sektora.",
            "player_units": [("PANCERNY", 400, 500), ("PANCERNY", 200, 500)],
            "ai_units": [("KOMPANIA_PANC", 1400, 400, True), ("PIECHOTA", 1400, 600, True)]
        },
        {
            "id": 5, "title": "UPADEK ŻOLIBORZA", "map": "warszawa_zoliborz",
            "desc": "NATO ucieka. Nie pozwól im się przegrupować w mieście.",
            "goal": "Zdław ostatni punkt oporu.",
            "player_units": [("PANCERNY", 400, 500), ("ZMECHANIZOWANY", 300, 300)],
            "ai_units": [("PIECHOTA", 1200, 500, True), ("PIECHOTA", 1200, 300, True)]
        }
    ]
}