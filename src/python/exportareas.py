import argparse
import mysql.connector

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Exports one or more MAD areas to a SQL file which can be "
        "imported into another MAD instance. Useful for calculating routes "
        "on a non-production instance and importing the result."
    )

    parser.add_argument("sqlpass", type=str, help="SQL Password")

    parser.add_argument("--sqlhost", type=str,
                        help="SQL hostname or IP (default: localhost)",
                        default="localhost")

    parser.add_argument("--sqluser", type=str,
                        help="SQL Username (default: root)",
                        default="root")

    parser.add_argument("--dbname", type=str,
                        help="SQL Database Name (default: mad)",
                        default="mad")

    parser.add_argument("from_id", type=int,
                        help="Beginning of the range of IDs in the"
                             "settings_area table to export")

    parser.add_argument("to_id", type=int,
                        help="End of the range of IDs in the"
                        "settings_area table to export")

    args = parser.parse_args()

    cnx = mysql.connector.connect(
        host=args.sqlhost, database=args.dbname,
        user=args.sqluser, password=args.sqlpass)
    cursor = cnx.cursor(buffered=True)

    query = ("SELECT * FROM settings_area where area_id between "
             f"{args.from_id} and {args.to_id}")

    cursor.execute(query)

    for (area_id, guid, instance_id, name, mode) in cursor:
        a_guid = f"'{guid}'" if guid else 'null'
        print("insert into settings_area values "
              f"(null,{a_guid},'{instance_id}','{name}','{mode}');")

        # Area Pokestop
        ps_query = ("SELECT * FROM settings_area_pokestops where area_id = "
                    f"{area_id}")
        ps_cursor = cnx.cursor(buffered=True)
        ps_cursor.execute(ps_query)
        for (
                ps_area_id,
                geofence_included,
                geofence_excluded,
                routecalc,
                init,
                level,
                route_calc_algorithm,
                speed, max_distance,
                ignore_spinned_stops,
                cleanup_every_spin) in ps_cursor:
            # Geofence
            gf_query = ("SELECT * FROM settings_geofence where geofence_id = "
                        f"{geofence_included}")
            gf_cursor = cnx.cursor(buffered=True)
            gf_cursor.execute(gf_query)
            for (
                    geofence_id,
                    gfguid,
                    gfinstance_id,
                    gfname,
                    fence_type,
                    fence_data) in gf_cursor:
                gf_guid = f"'{gfguid}'" if gfguid else 'null'
                print("insert into settings_geofence values "
                      f"(null,{gf_guid},{gfinstance_id},'{gfname}',"
                      f"'{fence_type}','{fence_data}');")

            # Routecalc
            rc_query = ("SELECT * FROM settings_routecalc where routecalc_id ="
                        f" {routecalc}")
            rc_cursor = cnx.cursor(buffered=True)
            rc_cursor.execute(rc_query)
            for (
                    routecalc_id,
                    rcguid,
                    rcinstance_id,
                    recalc_status,
                    last_updated,
                    routefile) in rc_cursor:
                rc_guid = f"'{rcguid}'" if rcguid else 'null'
                print("insert into settings_routecalc values "
                      f"(null,{rc_guid},{rcinstance_id},{recalc_status},"
                      f"'{last_updated}','{routefile}');")

            print("insert into settings_area_pokestops values "
                  "((select max(area_id) from settings_area),"
                  "(select max(geofence_id) from settings_geofence),"
                  "null,"
                  "(select max(routecalc_id) from settings_routecalc),"
                  f"{init},"
                  f"{level},"
                  f"'{route_calc_algorithm}',"
                  f"{speed or 'null'},"
                  f"{max_distance or 'null'},"
                  f"{ignore_spinned_stops or 'null'},"
                  f"{cleanup_every_spin or 'null'});")

    cursor.close()
    cnx.close()
