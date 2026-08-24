import os

from image_processing import preprocess_signature
from fingerprint import generate_fingerprint
from lcs import compare_fingerprints
from similarity import create_similarity_result


# ========================================
# SIGNATURE FILE PATHS
# ========================================

REFERENCE_PATH = (
    "Signatures/reference/signature1.jpeg"
)

TEST_PATH = (
    "Signatures/test/signature2.jpeg"
)


# ========================================
# CHECK WHETHER FILES EXIST
# ========================================

if not os.path.exists(REFERENCE_PATH):

    print()
    print("ERROR: Reference signature not found.")
    print("Expected file:")
    print(REFERENCE_PATH)
    print()

    raise SystemExit


if not os.path.exists(TEST_PATH):

    print()
    print("ERROR: Test signature not found.")
    print("Expected file:")
    print(TEST_PATH)
    print()

    raise SystemExit


# ========================================
# START PROGRAM
# ========================================

print()
print("============================================")
print("           SIGNAMATCH SYSTEM")
print("============================================")

print()
print("Reference image:")
print(REFERENCE_PATH)

print()
print("Test image:")
print(TEST_PATH)


# ========================================
# STEP 1 — PROCESS REFERENCE SIGNATURE
# ========================================

print()
print("--------------------------------------------")
print("STEP 1: PROCESSING REFERENCE SIGNATURE")
print("--------------------------------------------")

reference_image = preprocess_signature(
    REFERENCE_PATH
)

print("Reference image processed successfully.")


# ========================================
# STEP 2 — GENERATE REFERENCE FINGERPRINT
# ========================================

print()
print("--------------------------------------------")
print("STEP 2: GENERATING REFERENCE FINGERPRINT")
print("--------------------------------------------")

reference_result = generate_fingerprint(
    reference_image["binary"]
)

reference_fingerprint = (
    reference_result["fingerprint"]
)

print(
    "Reference fingerprint:",
    reference_fingerprint
)

print(
    "Fingerprint length:",
    len(reference_fingerprint)
)


# ========================================
# STEP 3 — PROCESS TEST SIGNATURE
# ========================================

print()
print("--------------------------------------------")
print("STEP 3: PROCESSING TEST SIGNATURE")
print("--------------------------------------------")

test_image = preprocess_signature(
    TEST_PATH
)

print("Test image processed successfully.")


# ========================================
# STEP 4 — GENERATE TEST FINGERPRINT
# ========================================

print()
print("--------------------------------------------")
print("STEP 4: GENERATING TEST FINGERPRINT")
print("--------------------------------------------")

test_result = generate_fingerprint(
    test_image["binary"]
)

test_fingerprint = (
    test_result["fingerprint"]
)

print(
    "Test fingerprint:",
    test_fingerprint
)

print(
    "Fingerprint length:",
    len(test_fingerprint)
)


# ========================================
# STEP 5 — LCS COMPARISON
# ========================================

print()
print("--------------------------------------------")
print("STEP 5: LCS COMPARISON")
print("--------------------------------------------")

comparison = compare_fingerprints(
    reference_fingerprint,
    test_fingerprint
)

lcs_length = comparison["lcs_length"]

print(
    "LCS length:",
    lcs_length
)


# ========================================
# STEP 6 — SIMILARITY ANALYSIS
# ========================================

print()
print("--------------------------------------------")
print("STEP 6: SIMILARITY ANALYSIS")
print("--------------------------------------------")

similarity_result = (
    create_similarity_result(
        lcs_length,
        len(reference_fingerprint)
    )
)

similarity_percentage = (
    similarity_result[
        "similarity_percentage"
    ]
)

classification = (
    similarity_result[
        "classification"
    ]
)

print(
    "Similarity:",
    round(
        similarity_percentage,
        2
    ),
    "%"
)

print(
    "Result:",
    classification
)


# ========================================
# FINAL RESULT
# ========================================

print()
print("============================================")
print("             FINAL RESULT")
print("============================================")

print()
print(
    "Reference fingerprint:",
    reference_fingerprint
)

print(
    "Test fingerprint:",
    test_fingerprint
)

print(
    "LCS length:",
    lcs_length,
    "/",
    len(reference_fingerprint)
)

print(
    "Similarity:",
    round(
        similarity_percentage,
        2
    ),
    "%"
)

print(
    "Classification:",
    classification
)

print()
print("============================================")
print("       SIGNAMATCH EXECUTION COMPLETE")
print("============================================")
print()