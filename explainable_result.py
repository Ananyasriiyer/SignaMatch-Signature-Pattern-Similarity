def explain_similarity(similarity):
    """
    Generate a simple explanation for the signature similarity score.
    """

    try:
        similarity = float(similarity)
    except (ValueError, TypeError):
        return {
            "level": "Unknown",
            "explanation": "The similarity score could not be calculated.",
            "recommendation": "Please check the signature images and comparison process."
        }

    if similarity >= 90:
        level = "Very High Similarity"
        explanation = (
            "The two signatures show a very high level of similarity. "
            "Their compared patterns are strongly alike."
        )
        recommendation = (
            "The signatures appear highly similar based on the calculated score."
        )

    elif similarity >= 75:
        level = "High Similarity"
        explanation = (
            "The two signatures show a high level of similarity. "
            "Several important signature patterns are common between them."
        )
        recommendation = (
            "The signatures appear similar based on the calculated score."
        )

    elif similarity >= 50:
        level = "Moderate Similarity"
        explanation = (
            "The signatures show a moderate level of similarity. "
            "Some patterns are common, while other patterns are different."
        )
        recommendation = (
            "The result should be examined together with the difference image."
        )

    elif similarity >= 25:
        level = "Low Similarity"
        explanation = (
            "The signatures show a low level of similarity. "
            "Several patterns differ between the two signatures."
        )
        recommendation = (
            "The signatures appear substantially different based on the score."
        )

    else:
        level = "Very Low Similarity"
        explanation = (
            "The signatures show very little similarity. "
            "Most of the compared patterns are different."
        )
        recommendation = (
            "The signatures appear significantly different based on the score."
        )

    return {
        "level": level,
        "explanation": explanation,
        "recommendation": recommendation
    }
