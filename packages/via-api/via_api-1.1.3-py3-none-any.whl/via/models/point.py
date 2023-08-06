import hashlib
from numbers import Number
from operator import itemgetter

import numpy
from cached_property import cached_property
from shapely.geometry import MultiPoint, Point

from via import settings
from via.constants import HIGHWAYS_TO_EXCLUDE
from via import logger
from via.place_cache import place_cache
from via.models.generic import GenericObject, GenericObjects
from via.models.gps import GPSPoint
from via.utils import angle_between_slopes


class Context:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context_pre = []
        self.context_post = []

    def __del__(self):
        attrs_to_del = ["content_hash"]

        for attr in attrs_to_del:
            try:
                delattr(self, attr)
            except:
                pass

    def set_context(self, pre=None, post=None):
        if not self.is_context_populated:
            self.context_pre = pre
            self.context_post = post

    def get_slope_incoming(self, mode="near"):
        """

        :kwarg mode: near or far - how much context should be used
        """
        if mode == "far":
            return self.context_pre[0].gps.slope_between(self.gps)
        if mode == "near":
            return self.context_pre[-1].gps.slope_between(self.gps)
        raise ValueError(f"Mode {mode} not recognised")

    def get_slope_outgoing(self, mode="near"):
        """

        :kwarg mode: near or far - how much context should be used
        """
        if mode == "far":
            return self.gps.slope_between(self.context_post[-1].gps)
        if mode == "near":
            return self.gps.slope_between(self.context_post[0].gps)
        raise ValueError(f"Mode {mode} not recognised")

    def get_slope_around_point(self, mode="near"):
        """
        Get the slope of the few points around the point.

        Useful in getting a slope associated with the slope so we can
        compare it to the slope of a road

        :kwarg mode: near or far - how much context should be used
        """
        if mode == "far":
            return self.context_pre[0].gps.slope_between(self.context_post[-1])
        if mode == "near":
            return self.context_pre[-1].gps.slope_between(self.context_post[0])

        raise ValueError("Mode {mode} not recognised")

    def get_in_out_angle(self, mode="near"):
        """

        :kwarg mode: near or far - how much context should be used
        :return: positive smallest angle difference between in slope and
             out slope
        :rtype: float
        """
        # TODO: Rename this function, ew
        return angle_between_slopes(
            self.get_slope_incoming(mode=mode),
            self.get_slope_outgoing(mode=mode),
            absolute=True,
        )

    @property
    def is_context_populated(self) -> bool:
        """
        Do we have context forward and back?
        Not all context but at least some on either side
        """
        return self.context_pre != [] and self.context_post != []

    @property
    def dist_to_earliest(self):
        raise NotImplementedError()

    @property
    def dist_to_latest(self):
        raise NotImplementedError()

    def serialize(self, include_time=True):
        return {
            "pre": [
                p.serialize(include_time=include_time, include_context=False)
                for p in self.context_pre
            ],
            "post": [
                p.serialize(include_time=include_time, include_context=False)
                for p in self.context_post
            ],
        }


class FramePoint(Context, GenericObject):
    """
    Data which snaps to the gps giving something like
    {gps: (1, 2), acc: [1,2,3], time: 1}

    Rather than
    {gps: (1, 2), acc: 1, time: 1}
    {gps: (1, 2), acc: 2, time: 2}
    {gps: (1, 2), acc: 3, time: 3}
    """

    def __init__(self, time, gps, acceleration, slow=None):
        """

        :param time:
        :param gps: GPSPoint or dict serialization of GPSPoint
        :param acceneration:
        :kwarg slow: If at this point the person is going slow
        """
        super().__init__()

        self.time = time
        self.gps = GPSPoint.parse(gps)
        self._slow = slow

        if isinstance(acceleration, list):
            self.acceleration = [
                acc for acc in acceleration if acc >= settings.MIN_ACC_SCORE
            ]
        else:
            if acceleration is None:
                acceleration = 0
            assert isinstance(acceleration, Number)
            self.acceleration = [
                acc for acc in [acceleration] if acc >= settings.MIN_ACC_SCORE
            ]

    @property
    def slow(self):
        if self.speed is None:
            return False  # Is this fair?

        if self._slow is not None:
            return self._slow

        return self._slow is False or (
            isinstance(self.speed, float)
            and self.speed <= settings.MIN_METRES_PER_SECOND
        )

    @property
    def speed(self):
        """
        Get the speed at this point (in metres per second) from the
        first and last context of this object

        Should have an option to get from the immediately surrounding points

        :rtype: float
        """
        if self.is_context_populated:
            origin = self.context_pre[0]
            dst = self.context_post[-1]

            if origin.time is None and dst.time is None:
                return None

            metres_per_second = 0
            distance = origin.distance_from(dst.gps)
            if distance != 0:
                time_diff = dst.time - origin.time
                metres_per_second = distance / time_diff
            return round(metres_per_second, 2)

        return None

    def get_edges_with_context(self, graph, edges, include_slow=True):
        """
        Get a list of dicts, giving context to how it relates to the
        current FramePoint

        :param graph:
        :param edges:
        :return: list of dicts with keys
            edge:
            origin: GPSPoint of start of edge
            dst: GPSPoint of end of edge
            slope: the slope of the edge
            angle_between: the smallest angle between the slope of the edge
                and the slope of actual travel
        :rtype: list
        """
        if self.slow and not include_slow:
            # FIXME: should not return, should get the context of the previous edge not slow and the next edge not slow
            return

        edge_node_data = []
        slope_around = self.get_slope_around_point()

        for edge in edges:
            try:
                origin = graph.nodes[edge[0][0]]
                dst = graph.nodes[edge[0][1]]
                data = {
                    "edge": edge,
                    "origin": GPSPoint(origin["y"], origin["x"]),
                    "dst": GPSPoint(dst["y"], dst["x"]),
                }
                data["slope"] = data["origin"].slope_between(data["dst"])
                data["angle_between"] = angle_between_slopes(
                    slope_around, data["slope"], absolute=True
                )
                edge_node_data.append(data)
            except Exception as ex:
                logger.warning(f"Could not get edge data: {edge}: {ex}")

        return edge_node_data

    def get_best_edge(self, edges, graph=None, mode=None, include_slow=True):
        """

        :kwarg mode: strategy to use to get the best edge
        """
        if self.slow and not include_slow:
            # FIXME: should not return, should get the context of the previous edge not slow and the next edge not slow
            return

        default_mode = "nearest"
        modes_require_graph = {"matching_angle", "angle_nearest"}
        modes_require_context = {"matching_angle", "angle_nearest"}

        def nearest(edges):
            return sorted(edges, key=itemgetter(1))[0]

        def matching_angle(edges, graph):
            return sorted(
                self.get_edges_with_context(graph, edges, include_slow=include_slow),
                key=lambda x: x["angle_between"],
            )[0]["edge"]

        def angle_nearest(edges, graph):
            # Find a middleground between the best angle match and the
            # nearest by distance

            # If previous and next the same, this should be the same.
            # Can do for the previous few

            edges_by_angle = sorted(
                self.get_edges_with_context(graph, edges, include_slow=include_slow),
                key=lambda x: x["angle_between"],
            )

            if not edges_by_angle:
                return None

            best_edge = edges_by_angle[0]
            for edge in edges_by_angle:
                # if best angle match is x degrees within the next and the
                # next is closer, use the closer one
                if all(
                    [
                        edge["angle_between"] < settings.CLOSE_ANGLE_TO_ROAD,
                        edge["edge"][1] < best_edge["edge"][1],
                        edge["edge"][1] < 0.0001,  # TODO: to settings
                    ]
                ):
                    best_edge = edge

            return best_edge["edge"]

        if mode is None:
            mode = default_mode

        if mode in modes_require_graph:
            if not graph:
                logger.warning(
                    f"graph not supplied to get_best_edge and mode '{mode}' was selected. Defaulting to mode '{default_mode}'"
                )
                return self.get_best_edge(edges, mode=default_mode, graph=graph)

        if mode in modes_require_context:
            if not self.is_context_populated:
                logger.debug(
                    f"Cannot use mode '{mode}' as point context is not populated, using mode '{default_mode}'"
                )
                # can probably warn if there's no post AND no pre, that would
                # show there was no context ever set on the journey?
                return self.get_best_edge(edges, mode="nearest", graph=graph)

        # Remove footway (unless there's no other options).
        # May want to keep included if it's the only thing close
        if graph is not None:
            without_footway = []
            for edge in edges:
                if edge[0] not in graph.edges:
                    logger.warning(f"Could not find edge {edge[0]}")
                    continue

                highway = graph.edges[edge[0]]["highway"]
                include = True

                if not isinstance(highway, list):
                    include = highway not in HIGHWAYS_TO_EXCLUDE
                else:
                    # TODO: if highway is a list be more fancy
                    pass

                if include:
                    without_footway.append(edge)

            if without_footway != []:
                edges = without_footway

        # TODO: store nearest on the object
        if mode == "nearest":
            return nearest(edges)
        elif mode == "matching_angle":
            return matching_angle(edges, graph)
        elif mode == "angle_nearest":
            return angle_nearest(edges, graph)
        elif mode == "sticky":
            # Try to stick to previous road if it makes sense
            # Might want to be sticky on top of some other mode?
            # Not important now
            raise NotImplementedError()
        else:
            logger.warning(
                f"Can not use mode '{mode}' to get best edge as that is not recognised. Defaulting to mode '{default_mode}'"
            )
            return self.get_best_edge(edges, mode=default_mode, graph=graph)

    def append_acceleration(self, acc):
        if self.slow:
            return
        if isinstance(acc, list):
            for item in acc:
                self.append_acceleration(item)
        elif isinstance(acc, type(None)):
            return
        else:
            if acc >= settings.MIN_ACC_SCORE:
                self.acceleration.append(acc)

    @staticmethod
    def parse(obj):
        """
        Given a dict representation of a FramePoint (or a FramePoint object)
        return with a FramePoint object
        """
        if isinstance(obj, FramePoint):
            return obj

        if isinstance(obj, dict):
            return FramePoint(
                obj.get("time", None),
                obj["gps"],
                [acc for acc in obj["acc"] if acc >= settings.MIN_ACC_SCORE],
            )
        raise NotImplementedError(f"Can't parse Point from type {type(obj)}")

    def speed_between(self, point: GPSPoint) -> float:
        """
        Get the speed between this and another point (as the crow flies) in
        metres per second

        :param point: A FramePoint obj
        :return: metres per second
        :rtype: float
        """
        metres_per_second = None
        distance = self.distance_from(point.gps)
        if distance != 0:
            time_diff = point.time - self.time
            if time_diff == 0:
                return 0
            metres_per_second = distance / time_diff
        return metres_per_second

    def distance_from(self, point: GPSPoint) -> float:
        """

        :param point: GPSPoint or tuple of (lat, lng) or Frame object
        :rtype: float
        :return: Distance between points in metres
        """
        if isinstance(point, FramePoint):
            point = point.gps
        return self.gps.distance_from(point)

    @property
    def is_complete(self) -> bool:
        """
        Does the point contain all expected data
        """
        return (
            isinstance(self.time, float)
            and self.gps.is_populated
            and self.acceleration != []
        )

    @property
    def road_quality(self) -> int:
        """
        Get the average quality at this point (and a little before)

        :return: mean of acceleration points
        :rtype: float
        """
        if self.slow:
            return 0
        if self.acceleration == []:
            return 0
        try:
            return int(numpy.mean(self.acceleration) * 100)
        except:
            logger.warning(
                f"Could not calculate road quality from: {self.acceleration}. Defauling to 0",
            )
            return 0

    def serialize(
        self, include_time: bool = True, include_context: bool = True
    ) -> dict:
        data = {
            "gps": self.gps.serialize(),
            "acc": list(self.acceleration),
            "slow": self.slow,
        }
        if include_time:
            if self.time is not None:
                data["time"] = round(self.time, 2)
            else:
                data["time"] = None
        if include_context:
            data["context"] = {
                "pre": [
                    p.serialize(include_time=include_time, include_context=False)
                    for p in self.context_pre
                ],
                "post": [
                    p.serialize(include_time=include_time, include_context=False)
                    for p in self.context_post
                ],
            }
        return data

    @property
    def gps_hash(self) -> int:
        """
        Get the hash of the GPS of this point`
        """
        return self.gps.content_hash

    @cached_property
    def content_hash(self) -> int:
        """
        Get the hash of the contents of this point`
        """
        return (
            int.from_bytes(
                f"{self.acceleration} {self.gps.point} {self.time}".encode(), "little"
            )
            % 2**100
        )


class FramePoints(GenericObjects):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("child_class", FramePoint)
        super().__init__(*args, **kwargs)

    def __del__(self):
        attrs_to_del = ["country"]

        for attr in attrs_to_del:
            try:
                delattr(self, attr)
            except AttributeError:
                pass

    @property
    def most_northern(self) -> float:
        """
        Get the max lat of all points
        """
        return max([frame.gps.lat for frame in self])

    @property
    def most_southern(self) -> float:
        """
        Get the min lat of all points
        """
        return min([frame.gps.lat for frame in self])

    @property
    def most_eastern(self) -> float:
        """
        Get the max lng of all points
        """
        return max([frame.gps.lng for frame in self])

    @property
    def most_western(self) -> float:
        """
        Get the min lng of all points
        """
        return min([frame.gps.lng for frame in self])

    @property
    def bbox(self) -> dict:
        return {
            "north": self.most_northern,
            "south": self.most_southern,
            "east": self.most_eastern,
            "west": self.most_western,
        }

    @property
    def data_quality(self) -> float:
        """
        Get the percentage of frames that are good. Should
        automatically disregard journeys with low data quality

        :rtype: float
        :return: The percent between 0 and 1
        """
        return 1.0  # TODO

    @property
    def origin(self):
        """
        Get the FramePoint at the start of the journey

        :rtype: via.models.Frame
        :return: The first frame of the journey
        """
        return self[0]

    @property
    def destination(self):
        """
        Get the FramePoint at the end of the journey

        :rtype: via.models.Frame
        :return: The last frame of the journey
        """
        return self[-1]

    @property
    def duration(self) -> float:
        """

        :rtype: float
        :return: The number of seconds the journey took
        """
        if self.destination.time is None or self.origin.time is None:
            return None
        return self.destination.time - self.origin.time

    @property
    def direct_distance(self) -> float:
        """

        :rtype: float
        :return: distance from origin to destination in metres
        """
        return self[0].distance_from(self[-1])

    def serialize(
        self, include_time: bool = False, include_context: bool = True
    ) -> list:
        return [
            frame.serialize(include_time=include_time, include_context=include_context)
            for frame in self
        ]

    def get_multi_points(self) -> MultiPoint:
        """
        Get a shapely.geometry.MultiPoint of all the points
        """
        unique_points = []
        prev = None
        for frame in self:
            if frame.gps.is_populated:
                if prev is not None:
                    if prev.gps.lat != frame.gps.lat:
                        unique_points.append(Point(frame.gps.lng, frame.gps.lat))

            prev = frame

        return MultiPoint(unique_points)

    @property
    def gps_hash(self) -> str:
        """
        Get the hash of all the GPSs of all of the points
        """
        return hashlib.md5(
            str([point.gps.content_hash for point in self]).encode()
        ).hexdigest()

    @property
    def content_hash(self) -> str:
        """
        Get the hash of all the data of all of the points
        """
        return hashlib.md5(
            str([point.content_hash for point in self]).encode()
        ).hexdigest()

    @cached_property
    def country(self) -> str:
        """
        Get what country this journey started in

        :return: a two letter country code
        :rtype: str
        """
        return self.origin.gps.reverse_geo["cc"]

    def is_in_place(self, place_name: str) -> bool:
        """
        Get if a journey is entirely within the bounds of some place.
        Does this by rect rather than polygon so it isn't exact but mainly
        to be used to focus on a single city.

        :param place_name: An osmnx place name. For example "Dublin, Ireland"
            To see if the place name is valid try graph_from_place(place).
            Might be good to do that in here and throw an ex if it's not found
        """
        return place_cache.is_in_place(self.bbox, place_name)
