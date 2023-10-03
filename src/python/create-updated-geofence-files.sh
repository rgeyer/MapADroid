prefix=$(date +%m%d%Y)

KMLFILE="/code/$prefix.kml"
PORFILE="/code/$prefix.json"

docker build -t madpy .
docker run -it --rm -v $(pwd):/code madpy sh -c "python /code/madtoporacle-gf.py $DBUSER $DBPASS $DBNAME --dbhost $DBHOST --kml $KMLFILE --poraclejs $PORFILE"