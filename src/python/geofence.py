import simplekml

class GeoFence:
    def __init__(self, name):
        self.path = []
        self.name = name.replace(" ","").replace("[", "").replace("]", "").strip()
        self._children = []
        self._min_lat = None
        self._max_lat = None
        self._min_lng = None
        self._max_lng = None

    def _set_min(current, new):
        if not current:
            return new

        if current < new:
            return current

        return new

    def _set_max(current, new):
        if not current:
            return new

        if current > new:
            return current

        return new

    def add_point(self, lat, lng):
        self.path.append([lat,lng])

    def add_child(self, child):
        self._children.append(child)

    def getpath(self):
        if self._children:
            for child in self._children:
                for p in child.path:
                    self._min_lat = GeoFence._set_min(self._min_lat, p[0])                    
                    self._max_lat = GeoFence._set_max(self._max_lat, p[0])
                    self._min_lng = GeoFence._set_min(self._min_lng, p[1])                    
                    self._max_lng = GeoFence._set_max(self._max_lng, p[1])
            return [
                [self._min_lat, self._min_lng],
                [self._min_lat, self._max_lng],
                [self._max_lat, self._max_lng],
                [self._max_lat, self._min_lng]
            ]
        return self.path

    def to_list_of_dict(self):
        retval = [{
            "name": self.name,
            "path": self.getpath(),
        }]
        [retval.append({"name": c.name, "path": c.getpath(), "parent": self.name}) for c in self._children]
        return retval

    def append_polygons_to_kml(self, kml):
        parent = kml.newpolygon(name=self.name)
        parent.outerboundaryis = [(p[1],p[0]) for p in self.getpath()]
        
        for child in self._children:
            cpol = kml.newpolygon(name=child.name)
            cpol.outerboundaryis = [(p[1],p[0]) for p in child.path]

    def append_linestrings_to_kml(self, kml):
        kml.newlinestring(
            name=self.name,
            coords=[(p[1],p[0]) for p in self.getpath()]
            )
        
        for child in self._children:
            kml.newlinestring(
                name=child.name,
                coords=[(p[1],p[0]) for p in child.path]
                )