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
        fences.append({
            "name": name,
            "color": "#FFFFFF",
            "id": idx,
            "path": [
                [float(ll[0]), float(ll[1])]
                for ll in [p.split(',') for p in json.loads(fence_data) if p]
                ]
            })
        idx += 1

    print(json.dumps(fences, indent=2))
    cnx.close()
