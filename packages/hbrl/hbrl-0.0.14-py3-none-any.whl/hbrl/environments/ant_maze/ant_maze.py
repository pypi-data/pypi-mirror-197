import math
import random
from .mujoco_files.maps.maps_index import TileType
import numpy as np
from gym.spaces import Box
from mujoco_py import load_model_from_path, MjSim, MjViewer
from scipy.spatial import distance
from .mujoco_files.xml_generator import generate_xml
from .mujoco_model_utils import quat2mat, euler2quat, mat2euler

"""
SETTINGS
"""

MAZE_TILE_RESOLUTION = 50  # size os a tile of the maze_grid in pixels


class AntMaze:

    def __init__(self, angle=0, maze_name="empty_room", image_resolution_per_tile=50, show=False):
        """
        Initialise an ant maze environment.
        THe model is automatically created using a map specification defined in /mujoco_files/maps/
        The maze_name should correspond to a map name, so /mujoco_files/maps/<maze_name>.txt should exist.
        """
        self.angle = angle
        self.maze_name = maze_name
        self.image_resolution_per_tile = image_resolution_per_tile
        self.maze_array, xml_spec_path = generate_xml(maze_name)  # TODO : check maze_info["reachable_spaces_size"]
        self.maze_array = np.array(self.maze_array)
        self.maze_array_height, self.maze_array_width = self.maze_array.shape

        # Create Mujoco Simulation
        self.model = load_model_from_path(xml_spec_path)
        self.sim = MjSim(self.model)

        low = self.map_coordinates_to_env_position(0, -1)
        high = self.map_coordinates_to_env_position(-1, 0)
        self.maze_space = Box(low=low, high=high)  # Verify low and high
        self.goal_space = Box(low=np.append(low, 0.45), high=np.append(high, 0.55))
        self.goal_size = self.goal_space.shape[0]

        # Observation space
        self.state_size = len(self.sim.data.qpos) + len(self.sim.data.qvel)
        fill_size = self.state_size - self.maze_space.shape[0]
        observation_low = np.concatenate((self.maze_space.low, np.full(fill_size, float("-inf"))))
        observation_high = np.concatenate((self.maze_space.high, np.full(fill_size, float("inf"))))
        self.state_space = Box(low=observation_low, high=observation_high)

        # Action space
        self.action_space = Box(low=self.sim.model.actuator_ctrlrange[:, 0],
                                high=self.sim.model.actuator_ctrlrange[:, 1])
        self.action_size = self.action_space.shape[0]

        max_actions = 500
        num_frames_skip = 10

        self.goal_thresholds = np.array([0.5, 0.5, 0.2, 0.5, 0.5])

        self.max_actions = max_actions

        # Implement visualization if necessary
        self.show = show
        if self.show:
            self.viewer = MjViewer(self.sim)
        self.num_frames_skip = num_frames_skip

        self.goal = None

    # Get state, which concatenates joint positions and velocities
    def get_state(self):
        return np.concatenate((self.sim.data.qpos, self.sim.data.qvel))

    def map_coordinates_to_env_position(self, x, y):
        x = self.maze_array_width + x if x < 0 else x
        y = self.maze_array_height + y if y < 0 else y
        return np.array([x - self.maze_array_width / 2 + 0.5, - (y - self.maze_array_height / 2 + 0.5)])

    def sample_reachable_position(self):
        # sample empty tile
        tile_coordinates = np.flip(random.choice(np.argwhere(self.maze_array != TileType.WALL.value)))
        position = self.map_coordinates_to_env_position(*tile_coordinates)

        # Sample a random position in the chosen tile
        low, high = position - 0.5, position + 0.5
        return np.random.uniform(low, high)

    # Reset simulation to state within initial state specified by user
    def reset(self):

        # Reset controls
        self.sim.data.ctrl[:] = 0

        # Reset joint positions and velocities

        # Sample a start position
        start_tiles = np.argwhere(self.maze_array == TileType.START.value)
        start_coordinates = np.flip(random.choice(start_tiles))
        start_position = self.map_coordinates_to_env_position(*start_coordinates)

        # Build the state from it, using fixed joints and velocities values.
        angle = random.random() * 2 - 1  # Sample random orientation for the beginning
        initial_qpos = np.array([0.55, 1.0, 0.0, 0.0, angle, 0.0, 1.0, 0.0, -1.0, 0.0, -1.0, 0.0, 1.0])
        initial_qvel = np.zeros(14)
        state = np.concatenate((start_position, initial_qpos, initial_qvel))

        self.sim.data.qpos[:] = state[:len(self.sim.data.qpos)]
        self.sim.data.qvel[:] = state[len(self.sim.data.qpos):]
        self.sim.step()

        # Choose a goal. Weights are used to keep a uniform sampling over the reachable space,
        # since boxes don't cover areas of the same size.
        goal_position = self.sample_reachable_position()
        torso_height = np.random.uniform(0.45, 0.55, (1,))
        self.goal = np.concatenate((goal_position, torso_height))
        if self.show:
            self.sim.data.mocap_pos[0][:2] = np.copy(self.goal[:2])

        if self.show:
            self.viewer.render()
        # Return state
        state = self.get_state()
        return state, self.goal

    # Execute low-level action for number of frames specified by num_frames_skip
    def step(self, action):
        self.sim.data.ctrl[:] = action
        for _ in range(self.num_frames_skip):
            self.sim.step()
            if self.show:
                self.viewer.render()
        new_state = self.get_state()

        reached = (np.abs(new_state[:len(self.goal)] - self.goal) < self.goal_thresholds[:len(self.goal)]).all()
        return self.get_state(), 0 if reached else -1, reached

    # Visualize end goal. This function may need to be adjusted for new environments.
    def display_end_goal(self):
        self.sim.data.mocap_pos[0][:2] = np.copy(self.goal[:2])

    # Visualize all sub-goals
    def display_sub_goals(self, sub_goals):

        # Display up to 10 sub-goals and end goal
        if len(sub_goals) <= 11:
            sub_goal_ind = 0
        else:
            sub_goal_ind = len(sub_goals) - 11

        for i in range(1, min(len(sub_goals), 11)):
            self.sim.data.mocap_pos[i][:2] = np.copy(sub_goals[sub_goal_ind][:2])
            self.sim.model.site_rgba[i][3] = 1

            sub_goal_ind += 1

    def set_node(self, node_name, rgba=None, position=None):
        geom_id = self.sim.model.geom_name2id(node_name)

        if rgba is not None:
            if isinstance(rgba, str):
                rgba = np.array([float(elt) for elt in rgba.split(" ")])
            if isinstance(rgba, list):
                rgba = np.array(rgba)
            self.sim.model.geom_rgba[geom_id, :] = rgba

        if position is not None:
            if isinstance(position, list):
                position = np.array(position)
            assert len(position) <= 3
            self.sim.model.geom_pos[geom_id, :len(position)] = position

    def set_edge(self, edge_name, first_node: np.ndarray, second_node: np.ndarray, rgba=None):
        edge_id = self.sim.model.geom_name2id(edge_name)

        assert first_node.shape == (2,)
        assert second_node.shape == (2,)

        # Compute edge position
        position = (first_node + second_node) / 2
        self.sim.model.geom_pos[edge_id] = position

        # Compute angle between these two nodes
        diff = second_node - first_node
        angle = math.acos(diff[0] / np.linalg.norm(diff))
        euler_rotation = np.array([-math.pi / 2, angle, 0])
        self.sim.model.geom_quat[edge_id] = euler2quat(euler_rotation)

        if rgba is not None:
            assert isinstance(rgba, str) and len(rgba.split(" ")) <= 4
            self.sim.model.geom_rgba[edge_id] = rgba

    def toggle_geom_object(self, object_name):
        geom_id = self.sim.model.geom_name2id(object_name)
        self.sim.model.geom_rgba[geom_id, -1] = 1 - self.sim.model.geom_rgba[geom_id, -1]

    def set_space_color(self, image_array: np.ndarray, low, high, color) -> np.ndarray:
        """
        Set a tile color with the given color in the given image as a numpy array of pixels
        :param image_array: The image where the tile should be set
        :param low: the box lower corner
        :param high: the box higher corner
        :param color: new color of the tile : numpy array [Red, Green, Blue]
        :return: The new image
        """
        tile_size = MAZE_TILE_RESOLUTION
        tile_width, tile_height = np.rint((high - low) * tile_size).astype(int)
        tile_img = np.tile(color, (tile_height, tile_width, 1))

        image_width, image_height, _ = image_array.shape

        # We add +1 to take images borders in consideration. Without it, x/y_min positions are computed from the
        # border of self.maze_space, that do not include maze borders.
        # NB: Y coordinates don't work the same in the state space and in the image.
        # High values (in the state space) are at the top of the image (low numpy index), with low coordinates in
        # the image. Opposite for X values.
        x_min = round((low[0] - self.maze_space.low[0] + 1) * tile_size)
        y_max = round(((image_height / tile_size) - (low[1] - self.maze_space.low[1] + 1)) * tile_size)

        x_max = x_min + tile_width
        y_min = y_max - tile_height

        image_array[y_min:y_max, x_min:x_max, :] = tile_img
        return image_array

    def render(self) -> np.ndarray:
        """
        Return a np.ndarray of size (width, height, 3) of pixels that represent the environments and it's walls
        :return: The final image.
        """

        # we add np.full(2, 2) to get image borders, because border walls are not included in env.maze_space.
        # We assume walls have a width of one, but it's not really important for a generated image.
        image_width_px, image_height_px = np.rint((self.maze_space.high - self.maze_space.low + np.full(2, 2))
                                                  * self.image_resolution_per_tile).astype(int)

        img = np.zeros(shape=(image_height_px, image_width_px, 3), dtype=np.uint8)

        # Render the grid
        for coordinates in np.argwhere(self.maze_array != TileType.WALL.value):
            coordinates = np.flip(coordinates)
            position = self.map_coordinates_to_env_position(*coordinates)
            img = self.set_space_color(img, position - 0.5, position + 0.5, np.array([255, 255, 255]))

        self.place_point(img, self.sim.data.qpos[:2], [0, 0, 255], width=10)
        self.place_point(img, self.goal[:2], [255, 0, 0], width=10)
        return img

    def place_point(self, image: np.ndarray, state, color: np.ndarray, width=50):
        """
        Modify the input image
        param image: Initial image that will be modified.
        param x: x coordinate in the state space of the point to place.
        param y: y coordinate in the state space of the point to place.
        param color: Color to give to the pixels that compose the point.
        param width: Width of the circle (in pixels).
        """
        x, y = tuple(state[:2])
        tile_size = MAZE_TILE_RESOLUTION

        # Convert x, y state_space_position into maze_coordinates to get point center
        # Explanation: same as in self.set_space_color, lines of code 5/6
        x_center_px = round((x - self.maze_space.low[0] + 1) * tile_size)
        y_center_px = round(((image.shape[1] / tile_size) - (y - self.maze_space.low[1] + 1)) * tile_size)

        # Imagine a square of size width * width, with the coordinates computed above as a center. Iterate through
        # each pixel inside this square to
        radius = round(width / 2) + 1
        for i in range(x_center_px - radius, x_center_px + radius):
            for j in range(y_center_px - radius, y_center_px + radius):
                if distance.euclidean((i + 0.5, j + 0.5), (x_center_px, y_center_px)) < radius:
                    image[j, i] = color

    def place_edge(self, image: np.ndarray, state_1, state_2, color: np.ndarray, width=40):
        """
        Modify the input image
        param image: Initial image that will be modified.
        param x: x coordinate in the state space of the point to place.
        param y: y coordinate in the state space of the point to place.
        param color: Color to give to the pixels that compose the point.
        param width: Width of the circle (in pixels).
        """
        tile_size = MAZE_TILE_RESOLUTION
        x1, y1 = tuple(state_1[:2])
        x2, y2 = tuple(state_2[:2])

        # Convert x, y state_space_position into maze_coordinates to get point center
        # Explanation: same as in self.set_space_color, lines of code 5/6
        x1_center_px = (x1 - self.maze_space.low[0] + 1) * tile_size
        y1_center_px = ((image.shape[1] / tile_size) - (y1 - self.maze_space.low[1] + 1)) * tile_size
        x2_center_px = (x2 - self.maze_space.low[0] + 1) * tile_size
        y2_center_px = ((image.shape[1] / tile_size) - (y2 - self.maze_space.low[1] + 1)) * tile_size
        x_min = int(min(x1_center_px, x2_center_px))
        x_max = int(max(x1_center_px, x2_center_px))
        y_min = int(min(y1_center_px, y2_center_px))
        y_max = int(max(y1_center_px, y2_center_px))
        # Imagine a square of size width * width, with the coordinates computed above as a center. Iterate through
        # each pixel inside this square to
        for i in range(x_min, x_max):
            for j in range(y_min, y_max):
                cross_product = (y2_center_px - y1_center_px) * (i - x1_center_px) \
                    - (x2_center_px - x1_center_px) * (j - y1_center_px)
                # compare versus epsilon for floating point values, or != 0 if using integers
                if abs(cross_product) > width * 10:
                    continue
                image[j, i] = color
