import numpy as np


def create_piece_shape(id_str: str, shape_array: list[list[int]]) -> dict:
    """
    Create a standardized piece shape with metadata.

    Args:
        id_str (str): String identifier for the piece (e.g., "I3", "L4", "T5")
        shape_array (list): 2D array representing the piece shape

    Returns:
        dict: Piece definition with id and shape
    """
    return {"id": id_str, "shape": np.array(shape_array)}


def get_standard_piece_shapes() -> list[dict]:
    """
    Create the standard 21 Blokus pieces as shape definitions.

    Returns:
        list: List of piece shape definitions
    """
    pieces = []

    # 1-square piece (monomino)
    pieces.append(create_piece_shape("1", [[1]]))

    # 2-square piece (domino)
    pieces.append(create_piece_shape("2", [[1, 1]]))

    # 3-square pieces (trominoes)
    pieces.append(create_piece_shape("I3", [[1, 1, 1]]))
    pieces.append(
        create_piece_shape(
            "V3",
            [
                [1, 0],
                [1, 1],
            ],
        )
    )

    # 4-square pieces (tetrominoes)
    pieces.append(
        create_piece_shape(
            "I4",
            [
                [1, 1, 1, 1],
            ],
        )
    )
    pieces.append(
        create_piece_shape(
            "L4",
            [
                [1, 0],
                [1, 0],
                [1, 1],
            ],
        )
    )
    pieces.append(
        create_piece_shape(
            "Z4",
            [
                [1, 1, 0],
                [0, 1, 1],
            ],
        )
    )
    pieces.append(
        create_piece_shape(
            "O4",
            [
                [1, 1],
                [1, 1],
            ],
        )
    )
    pieces.append(
        create_piece_shape(
            "T4",
            [
                [1, 1, 1],
                [0, 1, 0],
            ],
        )
    )

    # 5-square pieces (pentominoes) - all 12 of them
    pieces.append(
        create_piece_shape(
            "I5",
            [
                [1, 1, 1, 1, 1],
            ],
        )
    )

    pieces.append(
        create_piece_shape(
            "L5",
            [
                [1, 0],
                [1, 0],
                [1, 0],
                [1, 1],
            ],
        )
    )

    pieces.append(
        create_piece_shape(
            "Y5",
            [
                [0, 1],
                [1, 1],
                [0, 1],
                [0, 1],
            ],
        )
    )

    pieces.append(
        create_piece_shape(
            "N5",
            [
                [0, 1],
                [1, 1],
                [1, 0],
                [1, 0],
            ],
        )
    )

    pieces.append(
        create_piece_shape(
            "P5",
            [
                [1, 1],
                [1, 1],
                [1, 0],
            ],
        )
    )

    pieces.append(
        create_piece_shape(
            "U5",
            [
                [1, 0, 1],
                [1, 1, 1],
            ],
        )
    )

    pieces.append(
        create_piece_shape(
            "V5",
            [
                [1, 0, 0],
                [1, 0, 0],
                [1, 1, 1],
            ],
        )
    )

    pieces.append(
        create_piece_shape(
            "Z5",
            [
                [1, 1, 0],
                [0, 1, 0],
                [0, 1, 1],
            ],
        )
    )

    pieces.append(
        create_piece_shape(
            "T5",
            [
                [1, 1, 1],
                [0, 1, 0],
                [0, 1, 0],
            ],
        )
    )

    pieces.append(
        create_piece_shape(
            "W5",
            [
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 1],
            ],
        )
    )

    pieces.append(
        create_piece_shape(
            "F5",
            [
                [0, 1, 1],
                [1, 1, 0],
                [0, 1, 0],
            ],
        )
    )

    pieces.append(
        create_piece_shape(
            "X5",
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0],
            ],
        )
    )

    return pieces
