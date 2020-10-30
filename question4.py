#Cette question a été réalisée avec l'aide de Mr Blarel pour la fonction area_search

from pymongo import MongoClient
from pprint import pprint 
import requests
import json
import time
import dateutil.parser
from bson.objectid import ObjectId
import datetime


client = MongoClient('mongodb+srv://admin:admin123@cluster0.ut8s6.gcp.mongodb.net/bicycle?retryWrites=true&w=majority')

db = client.bicycle # or db = client['test-database']
db.datas.create_index([('station_id', 1),('date', -1)], unique=True)
db.stations2.create_index([('geometry','2dsphere')]) # on en a besoin pour la recherche par nom


def getCityLille():

    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"  
    response = requests.request("GET",url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records",[])

def getCityParis():
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes"  
    response = requests.request("GET",url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records",[])

def getCityLyon():
    url = "https://download.data.grandlyon.com/ws/grandlyon/pvo_patrimoine_voirie.pvostationvelov/all.json?maxfeatures=10&start=1"  
    response = requests.request("GET",url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records",[])

def getCityRennes():
    url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=stations_vls&q="  
    response = requests.request("GET",url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records",[])

#program to find a station by name
def getByname(nom):
    db.stations2.create_index([("name", "text")])
    stations=db.stations2.find({"$text":{"$search": nom }})

    return (list(stations))

#program to update a station
def update_Stations_Name(id,name):
    try:
        db.stations2.update_one( {"_id":id}, {"$set": {'name':name}})
    except:
        pprint("error update")
        pass

#program to delete station and datas (en identifiant l'id)
def delete_station(id):
    db.stations2.delete_many( {"_id":id} )
    db.datas.delete_many( {"station_id":id})


#deactivate all 
#On imagine une carte , délimitée par 4 points p1 a p4
def area_search(p1,p2,p3,p4,state):
    db.stations2.update_many(
        {"geometry": {
            "$geoWithin": 
                { 
                    "$polygon": [ [ p1[0] , p1[1] ], [ p2[0] , p2[1]], [ p3[0] , p3[1] ],[p4[0] , p4[1]] ] 
                }
            }
        },
        {"$set": {"deactivate":state}})


def ratio_bike():
    heure = datetime.datetime.today().hour
    day = datetime.datetime.today().strftime("%w")
    L_stations_id = []
    L_stations = list(db.stations2.find({}))
    result = []

    if ((heure >= 18 and heure <= 19) and day < 6):
        data = list(db.datas.find({ "station_id": 1 }, { 'stand_availbale': 1 },{'bike_availbale': 1}) )
        for elem in data:
            ratio = elem['bike_availbale'] / elem['stand_availbale']
            if (ratio < 0.2):
                L_stations_id.append(elem["station_id"])

    if (L_stations_id != []):
        for elem in L_stations_id:
            for elem1 in L_stations:
                if elem == elem1["_id"] :
                    result.append(elem1)

    return(result)

    
#print("Le result est :  ", ratio_bike)

# print(getByname("gare"))

# update_Stations_Name(ObjectId('5f8d42a27d02a896fcfd7d96'),"test_new_name")

# delete_station(ObjectId('5f8d42a37d02a896fcfd7d98'))

# p1 = [3.01, 50.01]

# p2 = [3.01,51.01]

# p3 = [3.99,51.01]

# p4 = [3.99,50.01]

#area_search(p1,p2,p3,p4,False)


#print(datetime.datetime.today().hour) 