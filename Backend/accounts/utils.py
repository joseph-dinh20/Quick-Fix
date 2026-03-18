from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_app")

def coordinates_to_city(lat, lng):
    location = geolocator.reverse((lat, lng))
    if location:
        address = location.raw.get("address", {})
        return address.get("city")
    return None