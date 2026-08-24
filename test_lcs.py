from lcs import (
    calculate_lcs_length,
    calculate_similarity,
    compare_fingerprints
)


print("======================================")
print("          LCS ALGORITHM TEST")
print("======================================")


string1 = "ABCDEF"
string2 = "ACEF"


lcs_length = calculate_lcs_length(
    string1,
    string2
)


similarity = calculate_similarity(
    string1,
    string2
)


result = compare_fingerprints(
    string1,
    string2
)


print()
print("String 1:", string1)
print("String 2:", string2)

print()
print("LCS length:", lcs_length)

print(
    "Similarity:",
    round(similarity, 2),
    "%"
)

print()
print("Complete result:")
print(result)

print("======================================")