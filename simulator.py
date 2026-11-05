

import numpy as np


def _pieces(state, key):
    """Iterate over complete pieces, always in shape (cells, 2)."""
    value = np.asarray(state[key], dtype=int)
    if key == "target":
        return [value.reshape(-1, 2)]
    if key == "unit":
        return value.reshape(-1, 1, 2)
    return value.reshape(-1, 2, 2)


def print_state(p, board_shape=None):
    if board_shape is None:
        coords = np.concatenate([
            value.reshape(-1, 2)
            for value in p.values()
            if value.size > 0
        ])

        board_shape = tuple((coords.max(axis=0) + 1).astype(int))

    table = np.zeros(board_shape, dtype=int)
    n = 1

    for key in ('target', 'hor', 'ver', 'unit'):
        if key == 'target':
            pieces = [p[key].reshape(-1, 2)]
        elif key == 'unit':
            pieces = p[key].reshape(-1, 1, 2)
        else:
            pieces = p[key]

        # Canonical ordering by position
        pieces = sorted(
            pieces,
            key=lambda obj: tuple(
                np.min(obj.reshape(-1, 2), axis=0)
            )
        )

        for piece in pieces:
            coords = piece.reshape(-1, 2)
            rows, cols = coords[:, 0], coords[:, 1]

            if np.any(rows < 0) or np.any(rows >= board_shape[0]) or \
               np.any(cols < 0) or np.any(cols >= board_shape[1]):
                raise ValueError("Piece outside board")

            if np.any(table[rows, cols] != 0):
                raise ValueError("Overlapping pieces")

            table[rows, cols] = n
            n += 1

    return table


def neighbors(coords, matrix):
    """Unique adjacent coordinates, excluding given coords and board exterior."""
    coords = np.asarray(coords, dtype=int).reshape(-1, 2)
    rows, cols = matrix.shape
    directions = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
    candidates = (coords[:, None, :] + directions).reshape(-1, 2)

    valid = (
        (candidates[:, 0] >= 0) & (candidates[:, 0] < rows) &
        (candidates[:, 1] >= 0) & (candidates[:, 1] < cols)
    )
    candidates = candidates[valid]
    overlap = np.any(
        np.all(candidates[:, None, :] == coords[None, :, :], axis=2), axis=1
    )
    return np.unique(candidates[~overlap], axis=0)


def table_to_state(table):
    """Convert a numbered table into target/hor/ver/unit coordinate arrays."""
    table = np.asarray(table, dtype=int)
    state = {"target": None, "hor": [], "ver": [], "unit": []}

    for number in np.unique(table):
        if number == 0:
            continue
        coords = np.argwhere(table == number)
        height, width = np.ptp(coords, axis=0) + 1

        if number == 1:
            state["target"] = coords
        elif (height, width) == (1, 2):
            state["hor"].append(coords)
        elif (height, width) == (2, 1):
            state["ver"].append(coords)
        elif (height, width) == (1, 1):
            state["unit"].append(coords[0])
        else:
            raise ValueError(f"Invalid piece {number}, dimensions {(height, width)}")

    if state["target"] is None:
        raise ValueError("Target piece (number 1) not found")
    state["hor"] = np.asarray(state["hor"], dtype=int).reshape(-1, 2, 2)
    state["ver"] = np.asarray(state["ver"], dtype=int).reshape(-1, 2, 2)
    state["unit"] = np.asarray(state["unit"], dtype=int).reshape(-1, 2)
    return state



def objects_around_zero(state, board_shape=None):
    """For each empty cell, list complete adjacent pieces from the state."""
    table = print_state(state, board_shape)
    zeros = np.argwhere(table == 0)
    result = {}

    for zero in zeros:
        nearby_coords = neighbors(zero.reshape(1, 2), table)
        objects = []
        for key in state:
            for piece in _pieces(state, key):
                overlap = np.any(np.all(
                    piece[:, None, :] == nearby_coords[None, :, :], axis=2
                ))
                if overlap:
                    objects.append(piece)
        result[tuple(zero)] = objects
    return result


def object_directions(nearby_objects):
    """One (row, col) movement vector for each adjacent piece."""
    result = {}
    for zero, objects in nearby_objects.items():
        zero = np.asarray(zero, dtype=int)
        vectors = []
        for obj in objects:
            diff = zero - obj
            mask = np.sum(np.abs(diff), axis=1) == 1
            if not np.any(mask):
                raise ValueError(f"No adjacent cell of {obj} for zero {zero}")
            vectors.append(diff[mask][0])
        result[tuple(zero)] = np.asarray(vectors, dtype=int).reshape(-1, 2)
    return result


def move_objects(nearby_objects, directions):
    """Return moved piece coordinates without modifying original pieces."""
    result = {}
    for zero, vectors in directions.items():
        result[zero] = [
            obj + direction
            for obj, direction in zip(nearby_objects[zero], vectors)
        ]
    return result


def movement_pairs(original, moved):
    """Return [[old_piece, moved_piece], ...] for all candidate moves."""
    pairs = []
    for zero in original:
        for old, new in zip(original[zero], moved[zero]):
            pairs.append([old, new])
    return pairs


def check_moves(state, pairs, board_shape=None):
    """Filter collisions, moves outside the board, and duplicate pairs."""
    if board_shape is None:
        board_shape = print_state(state).shape
    rows, cols = board_shape
    occupied = {
        tuple(coord)
        for value in state.values()
        for coord in np.asarray(value).reshape(-1, 2)
    }
    valid_pairs = []
    seen = set()

    for old, new in pairs:
        old_cells = set(map(tuple, old))
        new_cells = set(map(tuple, new))
        if any(not (0 <= r < rows and 0 <= c < cols) for r, c in new_cells):
            continue
        if new_cells & (occupied - old_cells):
            continue
        signature = (tuple(sorted(old_cells)), tuple(sorted(new_cells)))
        if signature in seen:
            continue
        seen.add(signature)
        valid_pairs.append([old, new])
    return valid_pairs


def create_new_states(state, valid_pairs):
    """Return one independent state per valid pair; never mutate input state."""
    new_states = []
    for old, new in valid_pairs:
        copy = {key: value.copy() for key, value in state.items()}
        found = False

        for key in copy:
            if key == "target":
                if np.array_equal(copy[key].reshape(-1, 2), old):
                    copy[key] = new.reshape(copy[key].shape).copy()
                    found = True
                    break
            else:
                for i in range(len(copy[key])):
                    if np.array_equal(copy[key][i].reshape(-1, 2), old):
                        copy[key][i] = new.reshape(copy[key][i].shape)
                        found = True
                        break
                if found:
                    break

        if not found:
            raise ValueError(f"Object not found in initial state: {old}")
        new_states.append(copy)
    return new_states


def generate_children(state, board_shape=None):
    """Return a NumPy array of child TABLES, shape (n_children, rows, cols)."""
    if board_shape is None:
        board_shape = print_state(state).shape
    board_shape = tuple(board_shape)

    nearby = objects_around_zero(state)
    directions = object_directions(nearby)
    moved = move_objects(nearby, directions)
    pairs = movement_pairs(nearby, moved)
    valids = check_moves(state, pairs)
    new_states = create_new_states(state, valids)

    tables = [print_state(child) for child in new_states]
    if not tables:
        return np.empty((0, *board_shape), dtype=int)
    return np.stack(tables)


if __name__ == "__main__":
    from lab4_states import p3

    children = generate_children(p3)
    print("Initial table:\n", print_state(p3))
    print("Child tables:", children.shape)
    for index, child in enumerate(children, start=1):
        print(f"Child {index}:\n{child}")
