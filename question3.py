#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      HP
#
# Created:     17/10/2020
# Copyright:   (c) HP 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import requests
import json
from pprint import pprint
from pymongo import MongoClient
import time
import dateutil.parser

atlas = MongoClient('mongodb+srv://admin:admin123@cluster0.ut8s6.gcp.mongodb.net/bicycle?retryWrites=true&w=majority')

db = atlas.bicycle
def main():
    pass

if __name__ == '__main__':
    main()


def nearStation(latitude,longitude):
    db.get.collection('stations').find({'geometry' :{
    $near:{$geometry:{
            type: "Point",
            coordinates: [latitude,longitude]},
            $maxDist:100,
            $minDist:0
            }
        }})