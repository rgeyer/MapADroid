import argparse
import json

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

    args = parser.parse_args()

    fences = []
    cnx = mysql.connector.connect(user=args.dbuser, password=args.dbpass,
                                  host=args.dbhost, database=args.dbname)

    cursor = cnx.cursor()
    query = "select name,fence_type,fence_data from settings_geofence"
    cursor.execute(query)

    idx = 0
    for (name, fence_type, fence_data) in cursor:
        subname = "Unknown"
        path = []
        for coord_or_name in json.loads(fence_data):
            ll = coord_or_name.split(',')
            if len(ll) == 1:
                if path:
                    fences.append({
                        "name": subname,
                        "color": "#FFFFFF",
                        "id": idx,
                        "path": path,
                    })
                    path = []
                    idx += 1
                subname = ll[0]                
            else:
                path.append([float(ll[0]), float(ll[1])])
        if subname == "Unknown" and path:
            fences.append({
                "name": name,
                "color": "#FFFFFF",
                "id": idx,
                "path": path,
                })
            idx += 1

    print(json.dumps(fences, indent=2))
    cnx.close()
