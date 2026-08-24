import numpy as np


def compress_matrix(binary_matrix):
    """
    Compress a 64 x 64 binary matrix
    into a 16 x 16 matrix.

    Each 4 x 4 block becomes one value.
    """

    height, width = binary_matrix.shape

    if height != 64 or width != 64:
        raise ValueError(
            "Expected a 64 x 64 binary matrix."
        )

    compressed = np.zeros(
        (16, 16),
        dtype=float
    )

    for row in range(16):
        for col in range(16):

            block = binary_matrix[
                row * 4:(row + 1) * 4,
                col * 4:(col + 1) * 4
            ]

            compressed[row, col] = np.mean(block)

    return compressed


def calculate_row_density(compressed_matrix):
    """
    Calculate the average ink density
    of each row.
    """

    row_density = np.mean(
        compressed_matrix,
        axis=1
    )

    return row_density


def calculate_column_density(compressed_matrix):
    """
    Calculate the average ink density
    of each column.
    """

    column_density = np.mean(
        compressed_matrix,
        axis=0
    )

    return column_density


def combine_row_column_density(
    row_density,
    column_density
):
    """
    Combine corresponding row and column
    density values.
    """

    combined = (
        row_density + column_density
    ) / 2

    return combined


def quantize_to_hex(value):
    """
    Convert a density value between 0 and 1
    into one hexadecimal character.

    0.0 → 0
    1.0 → F
    """

    value = max(
        0.0,
        min(1.0, float(value))
    )

    level = int(
        round(value * 15)
    )

    return format(
        level,
        "X"
    )


def generate_fingerprint(binary_matrix):
    """
    Generate a 16-character fingerprint
    from a 64 x 64 binary matrix.
    """

    compressed_matrix = compress_matrix(
        binary_matrix
    )

    row_density = calculate_row_density(
        compressed_matrix
    )

    column_density = calculate_column_density(
        compressed_matrix
    )

    combined_density = combine_row_column_density(
        row_density,
        column_density
    )

    fingerprint = ""

    for value in combined_density:

        fingerprint += quantize_to_hex(
            value
        )

    return {
        "compressed_matrix": compressed_matrix,
        "row_density": row_density,
        "column_density": column_density,
        "combined_density": combined_density,
        "fingerprint": fingerprint
    }