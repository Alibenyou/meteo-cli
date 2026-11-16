import requests

CODES_METEO = {
    # 00-19 : Ciel et phénomènes sans précipitations
    0: "Ciel dégagé",
    1: "Principalement dégagé",
    2: "Partiellement nuageux",
    3: "Couvert",
    4: "Visibilité réduite par de la fumée",
    5: "Brume sèche",
    10: "Brume",
    17: "Orage sans précipitations",
    18: "Grains",
    
    # 40-49 : Brouillard
    45: "Brouillard",
    48: "Brouillard givrant",
    
    # 50-59 : Bruine
    51: "Bruine légère",
    53: "Bruine modérée",
    55: "Bruine dense",
    56: "Bruine verglaçante légère",
    57: "Bruine verglaçante dense",
    
    # 60-69 : Pluie
    61: "Pluie faible",
    63: "Pluie modérée",
    65: "Pluie forte",
    66: "Pluie verglaçante faible",
    67: "Pluie verglaçante forte",
    
    # 70-79 : Neige et précipitations solides
    71: "Chute de neige faible",
    73: "Chute de neige modérée",
    75: "Chute de neige forte",
    77: "Grains de neige",
    
    # 80-89 : Averses
    80: "Averses de pluie faibles",
    81: "Averses de pluie modérées",
    82: "Averses de pluie violentes",
    85: "Averses de neige faibles",
    86: "Averses de neige fortes",
    
    # 90-99 : Orages
    95: "Orage faible ou modéré",
    96: "Orage avec grêle faible",
    99: "Orage avec grêle forte"
}

def trouver_ville(ma_ville):
    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        response = requests.get(url, params={"name":ma_ville,"count":1}, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "results" not in data:
            return None
        else:
            ville = data["results"][0]["name"]
            lat   = data["results"][0]["latitude"]
            lon   = data["results"][0]["longitude"]
            return (ville, lat, lon)
    except requests.exceptions.RequestException as e:
        print(f"Erreur {e}")
        return None

def obtenir_meteo(lat, lon):
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        response = requests.get(url, params={"latitude":lat,"longitude":lon, "current_weather":True}, timeout=10)
        response.raise_for_status()
        data = response.json()
        temp      = data["current_weather"]["temperature"]
        windspeed = data["current_weather"]["windspeed"]
        code      = data["current_weather"]["weathercode"]
        return (temp, windspeed, code)
    except requests.exceptions.RequestException as e:
        print(f"Erreur : {e}")
        return None


if __name__ == "__main__":
   name_ville = input("Entrer le nom de la ville : ")
   ville =  trouver_ville(name_ville)
   if ville:
       meteo = obtenir_meteo(ville[1], ville[2])
       if meteo:
        temp, vent, code = meteo   
        print(f"Il fait {temp}℃ à {ville[0]}, vent à {vent} km/h, {CODES_METEO.get(code, 'inconnu')}")
   else:
       print("ville introuvable")
