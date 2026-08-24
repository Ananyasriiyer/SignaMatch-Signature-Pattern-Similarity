def calculate_similarity_percentage(
    lcs_length,
    fingerprint_length
):
    """
    Calculate similarity percentage
    from the LCS length.
    """

    if fingerprint_length <= 0:
        return 0.0

    similarity = (
        lcs_length / fingerprint_length
    ) * 100

    return similarity


def classify_similarity(similarity):
    """
    Give a simple interpretation
    of the similarity percentage.
    """

    if similarity >= 90:
        return "Very High Similarity"

    elif similarity >= 75:
        return "High Similarity"

    elif similarity >= 50:
        return "Moderate Similarity"

    else:
        return "Low Similarity"


def create_similarity_result(
    lcs_length,
    fingerprint_length
):
    """
    Create a complete similarity result.
    """

    percentage = (
        calculate_similarity_percentage(
            lcs_length,
            fingerprint_length
        )
    )

    classification = (
        classify_similarity(
            percentage
        )
    )

    return {
        "lcs_length": lcs_length,
        "fingerprint_length": fingerprint_length,
        "similarity_percentage": percentage,
        "classification": classification
    }