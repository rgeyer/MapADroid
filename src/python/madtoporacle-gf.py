import argparse
import json
import simplekml
import geofence

import mysql.connector

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetches geofences from a MAD database and converts them "
        "to a json format compatible with PoracleJS.")

    parser.add_argument("dbuser", type=str,
                        help="Username for the MAD MySQL database")
    parser.add_argument("dbpass", type=str,
                        help="Password for the MAD MySQL database")
    parser.add_argument("dbname", type=str,
                        help="Name of the MAD MySQL database")
    parser.add_argument("--dbhost", type=str,
                        help="Hostname of the MAD MySQL database",
                        default="127.0.0.1")
    parser.add_argument("--kml", type=str,
                        help="A KML file with the found areas")    
    parser.add_argument("--poraclejs", type=str,
                        help="A json file formatted for use with poraclejs")

    args = parser.parse_args()

    kml = simplekml.Kml()

    fences = []
    fenceobs = []
    cnx = mysql.connector.connect(user=args.dbuser, password=args.dbpass,
                                  host=args.dbhost, database=args.dbname)

    cursor = cnx.cursor()
    query = "select name,fence_type,fence_data from settings_geofence"
    cursor.execute(query)

    for (name, fence_type, fence_data) in cursor:
        fenceob = geofence.GeoFence(name)
        subname = "Unknown"
        subfenceob = None
        for idx, coord_or_name in enumerate(json.loads(fence_data), start=1):
            if not coord_or_name:
                continue
            ll = coord_or_name.split(',')
            # It's not a lat/lng pair, it's a new subfence
            if len(ll) == 1:
                # When a new one starts
                if subfenceob:
                    fenceob.add_child(subfenceob)
                subname = ll[0]
                subfenceob = geofence.GeoFence(subname)
            else:
                lat = float(ll[0])
                lng = float(ll[1])
                if subfenceob:
                    subfenceob.add_point(lat,lng)
                else:
                    fenceob.add_point(lat,lng)
        # To capture the "last" one        
        if subfenceob:
            fenceob.add_child(subfenceob)
        fenceobs.append(fenceob)
    
    [f.append_polygons_to_kml(kml) for f in fenceobs]
    if args.kml:
        kml.save(args.kml)
    if args.poraclejs:
        with open(args.poraclejs, 'w') as jsout:
            jsout.write(json.dumps([f for flist in fenceobs for f in flist.to_list_of_dict()], indent=2))
    cnx.close()
