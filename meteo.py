import requests

def trouver_ville(coords):
    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        response = requests.get(url, params={"name":coords,"count":1}, timeout=10)

        data = response.json()
        if "results" not in data:
            print("Ville introuvable")
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
        data = response.json()
        print(data)
        temp = data["current_weather"]["temperature"]
        windspeed = data["current_weather"]["windspeed"]
        return (temp,windspeed)
    except requests.exceptions.RequestException as e:
        print(f"Erreur : {e}")
        return None


if __name__ == "__main__":
   name_ville = input("Entrer le nom de la ville : ")
   ville =  trouver_ville(name_ville)
   if ville:
       meteo = obtenir_meteo(ville[1], ville[2])
       if meteo:   
        print(f"Il fait {meteo[0]}℃ à {ville[0]}, vent à {meteo[1]} km/h")
   else:
       print("ville introuvable")