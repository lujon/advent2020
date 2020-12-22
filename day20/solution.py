import fileinput
from collections import defaultdict
from itertools import groupby
from math import prod, sqrt

import numpy as np

input_rows = [line.rstrip() for line in fileinput.input('input.txt')]


def parse_tile(tile_rows):
    tile_id = int(tile_rows[0].split()[1][:-1])
    image_rows = tile_rows[1:]

    image = np.array([[1 if c == '#' else 0 for c in row] for row in image_rows], int)

    return tile_id, image, [
        tuple(image[0]),
        tuple(reversed(image[0])),
        tuple(image[-1]),
        tuple(reversed(image[-1])),
        tuple(image[:, 0]),
        tuple(reversed(image[:, 0])),
        tuple(image[:, -1]),
        tuple(reversed(image[:, -1]))
    ]


tiles = list(map(parse_tile, [list(rows) for k, rows in groupby(input_rows, bool) if k]))

tiles_by_edge = defaultdict(list)

for tile_id, _, edges in tiles:
    for edge in edges:
        tiles_by_edge[edge].append(tile_id)

matched_edges_by_tile = defaultdict(list)

for edge, tile_ids in tiles_by_edge.items():
    if len(tile_ids) > 1:
        for tile_id in tile_ids:
            matched_edges_by_tile[tile_id].append(edge)


# Part 1

def is_corner_piece(tile_id):
    return len(matched_edges_by_tile[tile_id]) == 4


print(prod([tile_id for tile_id in matched_edges_by_tile.keys() if is_corner_piece(tile_id)]))


# Part 2

def is_edge_piece(tile_id):
    return len(matched_edges_by_tile[tile_id]) == 6


def is_middle_piece(tile_id):
    return len(matched_edges_by_tile[tile_id]) == 8


square_side = int(sqrt(len(tiles)))


def find_path(unused_tiles, path):
    if len(unused_tiles) == 0:
        return path

    left_id, left_image = path[-1] if path and len(path) % square_side != 0 else (None, None)
    top_id, top_image = path[-square_side] if len(path) > square_side else (None, None)

    next_is_corner = len(path) in (0, square_side - 1, (square_side * (square_side - 1)), (square_side * square_side - 1))
    next_is_edge = not next_is_corner and (len(path) < square_side or len(path) > (square_side * (square_side - 1))
                                           or len(path) % square_side in (0, square_side - 1))

    if next_is_corner:
        relevant_tiles = ((tile_id, image, edges) for tile_id, image, edges in unused_tiles if is_corner_piece(tile_id))
    elif next_is_edge:
        relevant_tiles = ((tile_id, image, edges) for tile_id, image, edges in unused_tiles if is_edge_piece(tile_id))
    else:
        relevant_tiles = ((tile_id, image, edges) for tile_id, image, edges in unused_tiles if is_middle_piece(tile_id))

    for tile in relevant_tiles:
        tile_id, image, edges = tile
        for rotation in get_matching_rotations(image, left_image, top_image):
            path_cpy = path.copy()
            path_cpy.append((tile_id, rotation))
            unused_tiles_cpy = unused_tiles.copy()
            unused_tiles_cpy.remove(tile)

            if new_path := find_path(unused_tiles_cpy, path_cpy):
                return new_path
    return []


def get_matching_rotations(image, left_neighbour_image, top_neighbour_image):
    matching_rotations = []

    for i in range(0, 4):
        rotated_image = np.rot90(image, i)
        if matches_neighbours(rotated_image, left_neighbour_image, top_neighbour_image):
            matching_rotations.append(rotated_image)

        horizontally_flipped_image = np.fliplr(rotated_image)
        if matches_neighbours(horizontally_flipped_image, left_neighbour_image, top_neighbour_image):
            matching_rotations.append(horizontally_flipped_image)

        vertically_flipped_image = np.flipud(rotated_image)
        if matches_neighbours(vertically_flipped_image, left_neighbour_image, top_neighbour_image):
            matching_rotations.append(vertically_flipped_image)

    return matching_rotations


def matches_neighbours(image, left_neighbour_image, top_neighbour_image):
    if not (left_neighbour_image is None or np.array_equal(image[:, 0], left_neighbour_image[:, -1])):
        return False
    if not (top_neighbour_image is None or np.array_equal(image[0], top_neighbour_image[-1])):
        return False
    return True


path = find_path(tiles, list())


def remove_borders(image):
    return image[1:-1, 1:-1]


full_image = np.concatenate([np.concatenate([remove_borders(path[y * square_side + x][1])
                                             for x in range(0, square_side)], 1)
                             for y in range(0, square_side)], 0)

full_image_side = len(full_image)

monster = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
])

monster_height = len(monster)
monster_width = len(monster[0])

inverted_monster = 1 - monster


def is_monster(sub_image):
    return np.array_equal(np.bitwise_and(monster, sub_image), monster)


def find_monsters(image):
    monster_positions = []

    for x in range(0, full_image_side - monster_width):
        for y in range(0, full_image_side - monster_height):
            sub_image = image[y:y + monster_height, x:x + monster_width]

            if is_monster(sub_image):
                monster_positions.append((y, x))

    return monster_positions


def get_water_roughness(full_image):
    for i in range(0, 4):
        rotated_image = np.rot90(full_image, i)

        for image in (rotated_image, np.fliplr(rotated_image), np.fliplr(rotated_image)):
            monster_positions = find_monsters(image)

            if monster_positions:
                image = remove_monsters(image, monster_positions)
                return np.count_nonzero(image == 1)


def remove_monsters(image, monster_positions):
    for y, x in monster_positions:
        sub_image = image[y:y + monster_height, x:x + monster_width]
        sub_image = np.bitwise_and(sub_image, inverted_monster)

        for y2 in range(0, monster_height):
            for x2 in range(0, monster_width):
                image[y + y2][x + x2] = sub_image[y2][x2]

    return image


print(get_water_roughness(full_image))
