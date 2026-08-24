from similarity import (
    calculate_similarity_percentage,
    classify_similarity,
    create_similarity_result
)


print("========================================")
print("       SIMILARITY MODULE TEST")
print("========================================")


# Test values
lcs_length = 8
fingerprint_length = 16


# Calculate percentage
percentage = (
    calculate_similarity_percentage(
        lcs_length,
        fingerprint_length
    )
)


# Classify the result
classification = (
    classify_similarity(
        percentage
    )
)


# Create complete result
result = create_similarity_result(
    lcs_length,
    fingerprint_length
)


print()
print("LCS Length:", lcs_length)

print(
    "Fingerprint Length:",
    fingerprint_length
)

print(
    "Similarity:",
    round(percentage, 2),
    "%"
)

print(
    "Classification:",
    classification
)

print()
print("Complete Result:")
print(result)

print()
print("========================================")