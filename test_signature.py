from image_processing import preprocess_signature
from fingerprint import generate_fingerprint
from lcs import compare_fingerprints
from similarity import create_similarity_result


# ----------------------------------------
# FILE PATHS
# ----------------------------------------

reference_path = (
    "Signatures/reference/signature1.jpeg"
)

test_path = (
    "Signatures/test/signature2.jpeg"
)


print("========================================")
print("       SIGNAMATCH FINAL COMPARISON")
print("========================================")


# ----------------------------------------
# PROCESS REFERENCE SIGNATURE
# ----------------------------------------

reference_image = preprocess_signature(
    reference_path
)

reference_result = generate_fingerprint(
    reference_image["binary"]
)

reference_fingerprint = (
    reference_result["fingerprint"]
)


# ----------------------------------------
# PROCESS TEST SIGNATURE
# ----------------------------------------

test_image = preprocess_signature(
    test_path
)

test_result = generate_fingerprint(
    test_image["binary"]
)

test_fingerprint = (
    test_result["fingerprint"]
)


# ----------------------------------------
# LCS COMPARISON
# ----------------------------------------

comparison = compare_fingerprints(
    reference_fingerprint,
    test_fingerprint
)


lcs_length = comparison["lcs_length"]


# ----------------------------------------
# SIMILARITY RESULT
# ----------------------------------------

similarity_result = (
    create_similarity_result(
        lcs_length,
        len(reference_fingerprint)
    )
)


# ----------------------------------------
# DISPLAY
# ----------------------------------------

print()
print("REFERENCE SIGNATURE")
print("--------------------")

print(
    "Fingerprint:",
    reference_fingerprint
)


print()
print("TEST SIGNATURE")
print("--------------------")

print(
    "Fingerprint:",
    test_fingerprint
)


print()
print("COMPARISON")
print("--------------------")

print(
    "LCS Length:",
    similarity_result["lcs_length"],
    "/",
    similarity_result["fingerprint_length"]
)


print(
    "Similarity:",
    round(
        similarity_result[
            "similarity_percentage"
        ],
        2
    ),
    "%"
)


print(
    "Result:",
    similarity_result[
        "classification"
    ]
)


print()
print("========================================")
print("       SIGNAMATCH RESULT")
print("========================================")