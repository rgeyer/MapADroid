# Description
This is a repository for all of resources that were used to build our local communities Pokemon scanner.

Primarily, this is the Map-A-Droid software, with some minor modifications, a docker compose file for our specific setup, and finally a 3d printed, rack mountable case for holding 16 of the Android TV boxes that are required for scanning.

This is an initial commit of VERY rough notes and resources, expect it to get more refined over time.

# BOM

|Qty|Item|Link|Cost Per|Total|Bulk Total|
|---|----|----|--------|-----|----------|
|16|A95X F1|https://www.amazon.com/Sawpy-Android-Smart-Quad-core-Cortex-A53/dp/B07PF271DF|$25.99|$415.84|$415.84|
|1|Meanwell 5v PSU|https://www.amazon.com/MEAN-WELL-LRS-350-5-Single-Switchable/dp/B0131V9TG0|$35.92|$35.92|$35.92|
|1|16 Channel 5v Relay Board|https://www.amazon.com/Organizer-16-Channel-Interface-Optocoupler-Arduino/dp/B07Y2X4F77|$13.98|$13.98|$13.98|
|16|DC Power Socket|https://www.amazon.com/gp/product/B01G6EB5U2/|$0.69|$11.04|$13.98|
|16|~1ft Length 22ga Power Wire|https://www.amazon.com/gp/product/B07SLBD1FY/|$0.15|$2.04|$15.00|
|1|Arduino ESP8266 NodeMCU|https://www.amazon.com/gp/product/B07HF44GBT/|$4.00|$4.00|$11.99|
|1|Waveshare Arduino IO Expansion Board 16ch|https://www.amazon.com/dp/B07P2H1NZG/|$7.95|$7.95|$7.95|
|1|1m Strip addressable LEDs|https://www.amazon.com/dp/B01CDTEJR0/|$21.88|$21.88|$21.88|
|1|Power Cable|https://www.amazon.com/gp/product/B01J4M3QDW|$3.59|$3.59|$17.95|
|3|18ga U Terminals|https://www.amazon.com/GFORTUN-Terminals-Insulated-Connector-22-16AWG/dp/B06XV8GLXJ/|$0.07|$0.21|$6.98|
|2|1kg PETG Filament|https://www.amazon.com/gp/product/B07PGYL6SV/|$18.33|$36.66|$54.99|
|2|80mm 5v cooling fan|https://www.amazon.com/dp/B0119SLG18/|$7.01|$14.02|$14.02|
|4|8 Position Dual Row Terminal Strip + Barrier Strip|https://www.amazon.com/dp/B07CLX1VW5/|$1.92|$7.66|$11.49|
|16|1ft Ethernet Patch Cables (CAT5 is fine, but impossible to find)|https://www.amazon.com/dp/B07CXPQ4SX/|$0.95|$15.20|$18.99|
|1|24 Port Ethernet switch|Ebay|~$60|~$60|~$60|
|1|IKEA Lack Side Table|https://www.ikea.com/us/en/p/lack-side-table-black-20011408/|$15|$15|$15|
|||||||
||Totals|||$663.11|$741.84|

# 3D Printed Parts

STLs in the `resources/ATVRackSTLs` directory.

Design 1, before optimization

|Qty|STL|Weight ea.|Weight Total|
|---|---|----------|------------|
|1|CabCenter|480g|480g|
|1|CabLeft|316g|316g|
|1|CabRight|316g|316g|
|16|Tray|18g|288g|
|2|ATVFrontLidBottom|14g|28g|
|2|ATVRearLidBottom|15g|30g|
|2|ATVFrontLidTop|12g|24g|
|2|ATVRearLidTop|53g|106g|
|1|PSUBracket|42g|42g|
|1|LidCenter|37g|37g|
||||1667g|

|Qty|STL|Weight ea.|Weight Total|Spool Before|Spool After|
|---|---|----------|------------|------------|-----------|
|1|CabCenter|300g|300g|1240g|1067g|
|1|CabLeft|246g|246g|654g|464g2|
|1|CabRight|246g|246g|||
|16|Tray|9g|144g|||
|2|ATVFrontLidBottom|||||
|2|ATVRearLidBottom|||||
|2|ATVFrontLidTop|||||
|2|ATVRearLidTop|||||
|1|PSUBracket|||||
|1|LidCenter|||||
||||1203g|

# TODO

* Modify RocketMAD to use a public sprite set
  * https://github.com/whitewillem/PogoAssets
  * https://github.com/ZeChrales/PogoAssets

* Scheduled Maintenance
  * DB
    * (actually delete) select count(*) from pokemon where last_modified < DATE_SUB(NOW(), INTERVAL 72 HOUR);
