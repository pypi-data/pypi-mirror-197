import logging
import math

import geopandas as gpd
import numpy as np
from shapely.geometry.linestring import LineString
from shapely.geometry.multilinestring import MultiLineString
from metadrive.utils.coordinates_shift import nuplan_to_metadrive_vector
from metadrive.component.lane.point_lane import PointLane
from metadrive.constants import DrivableAreaProperty
from metadrive.utils.interpolating_line import InterpolatingLine


class NuPlanLane(PointLane):
    VIS_LANE_WIDTH = 6.5

    def __init__(self, lane_meta_data, nuplan_center, need_lane_localization):
        """
        Extract the lane information of one waymo lane, and do coordinate shift
        """
        super(NuPlanLane, self).__init__(self._extract_centerline(lane_meta_data, nuplan_center), None)
        self.index = lane_meta_data.id
        self.need_lane_localization = need_lane_localization
        if isinstance(lane_meta_data.polygon.boundary, MultiLineString):
            boundary = gpd.GeoSeries(lane_meta_data.polygon.boundary).explode()
            sizes = []
            for idx, polygon in enumerate(boundary[0]):
                sizes.append(len(polygon.xy[1]))
            points = boundary[0][np.argmax(sizes)].xy
        elif isinstance(lane_meta_data.polygon.boundary, LineString):
            points = lane_meta_data.polygon.boundary.xy
        self.polygon = [[points[0][i], points[1][i], 0.1] for i in range(len(points[0]))]
        self.polygon += [[points[0][i], points[1][i], 0.] for i in range(len(points[0]))]
        self.polygon = nuplan_to_metadrive_vector(self.polygon, nuplan_center=[nuplan_center[0], nuplan_center[1], 0])

        self.entry_lanes = lane_meta_data.incoming_edges,
        self.exit_lanes = lane_meta_data.outgoing_edges,
        self.left_lanes = lane_meta_data.adjacent_edges[0],
        self.right_lanes = lane_meta_data.adjacent_edges[-1]

        self.left_boundary = InterpolatingLine(self._get_boundary_points(lane_meta_data.left_boundary, nuplan_center))
        self.right_boundary = InterpolatingLine(self._get_boundary_points(lane_meta_data.right_boundary, nuplan_center))
        self.width = self.VIS_LANE_WIDTH

    @staticmethod
    def _extract_centerline(map_obj, nuplan_center):
        path = map_obj.baseline_path.discrete_path
        points = np.array([nuplan_to_metadrive_vector([pose.x, pose.y], nuplan_center) for pose in path])
        return points

    def width_at(self, longitudinal: float) -> float:
        l_pos = self.left_boundary.position(longitudinal, 0)
        r_pos = self.right_boundary.position(longitudinal, 0)
        return min(np.linalg.norm(r_pos - l_pos), self.VIS_LANE_WIDTH)

    def __del__(self):
        logging.debug("NuPlanLane is released")

    def destroy(self):
        self.index = None
        super(NuPlanLane, self).destroy()

    @staticmethod
    def _get_boundary_points(boundary, center):
        path = boundary.discrete_path
        points = np.array([nuplan_to_metadrive_vector([pose.x, pose.y], nuplan_center=center) for pose in path])
        return points

    def construct_lane_in_block(self, block, lane_index):
        """
        Modified from base class, the width is set to 6.5
        """
        lane = self
        if lane_index is not None:
            lane.index = lane_index

        # build visualization
        segment_num = int(self.length / DrivableAreaProperty.LANE_SEGMENT_LENGTH)
        if segment_num == 0:
            middle = self.position(self.length / 2, 0)
            end = self.position(self.length, 0)
            theta = self.heading_theta_at(self.length / 2)
            self._construct_lane_only_vis_segment(block, middle, self.VIS_LANE_WIDTH, self.length, theta)

        for i in range(segment_num):
            middle = self.position(self.length * (i + .5) / segment_num, 0)
            end = self.position(self.length * (i + 1) / segment_num, 0)
            direction_v = end - middle
            theta = -math.atan2(direction_v[1], direction_v[0])
            length = self.length
            self._construct_lane_only_vis_segment(block, middle, self.VIS_LANE_WIDTH, length * 1.3 / segment_num, theta)

        # build physics contact
        if self.need_lane_localization:
            self._construct_lane_only_physics_polygon(block, self.polygon)
            self.polygon = None  # save memory


if __name__ == "__main__":
    raise ValueError("Can not be run")
    file_path = AssetLoader.file_path("waymo", "test.pkl", return_raw_style=False)
    data = read_waymo_data(file_path)
    print(data)
    lane = NuPlanLane(108, data["map"])
