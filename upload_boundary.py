from urllib import request
import json
from godisbilen.app import create_app, db
from godisbilen.region import Region

app = create_app(create_db=True)

search = input("Sök: ")
url = "https://nominatim.openstreetmap.org/search.php?q={}&polygon_geojson=1&format=json".format("+".join(search.split(" ")))
with request.urlopen(url) as url:
    data = json.loads(url.read().decode())
cities = ["quit"]
for index, city in enumerate(data, 1):
    print(str(index) + ") " + city["display_name"])
    cities.append(city["geojson"]["coordinates"][0])

choice_city = int(input("Välj alternativ: "))

poly = "POLYGON(({}))".format(",".join([str(coord[0]) + " " + str(coord[1]) for coord in cities[choice_city]]))

choice_name = input("Områdes namn: ")
with app.test_request_context():
    region = Region(name=choice_name.lower(), bounds=poly)
    db.session.add(region)
    db.session.commit()
print("Sparat!!!")