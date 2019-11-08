from urllib import request
import json
from godisbilen.app import create_app, db
from godisbilen.region import Region

app = create_app(create_db=True)

cities = []

def getChoice(start, end):
    '''Retunerar ett värde mellan angiven start och slit'''
    choice = input("Ditt val: ")
    if(choice.isdigit()):
        choice = int(choice)
        if(choice > end or choice < start):
            print("Skriv endast siffror mellan {}-{}".format(start, end))
            return getChoice(start, end)
        return choice
    print("Skriv endast siffror mellan {}-{}".format(start, end))
    return getChoice(start, end)

def search():
    global cities
    cities = []
    search = input("Sök: ")
    url = "https://nominatim.openstreetmap.org/search.php?q={}&polygon_geojson=1&format=json".format("+".join(search.split(" ")))
    with request.urlopen(url) as url:
        data = json.loads(url.read().decode())
    print("0) Ny sökning")
    for index, city in enumerate(data, 1):
        print(str(index) + ") " + city["display_name"])
        cities.append(city["display_name"])
        #cities.append(city["geojson"]["coordinates"][0])

if(__name__ == "__main__"):
    choice = 0
    while(choice == 0):
        search()
        choice = getChoice(0, len(cities))
    
    poly = "POLYGON(({}))".format(",".join([str(coord[0]) + " " + str(coord[1]) for coord in cities[choice + 1]]))
    choice_name = input("Områdets namn: ")
    with app.test_request_context():
        region = Region(name=choice_name.lower(), bounds=poly)
        db.session.add(region)
        db.session.commit()
    print("Sparat!!!")