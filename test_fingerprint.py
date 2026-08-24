from image_processing import preprocess_signature
from fingerprint import generate_fingerprint


# Reference signature
image_path = "Signatures/reference/signature1.jpeg"


print("======================================")
print("       SIGNAMATCH FINGERPRINT")
print("======================================")


# Step 1: Process the signature
result = preprocess_signature(
    image_path
)


# Step 2: Generate fingerprint
fingerprint_result = generate_fingerprint(
    result["binary"]
)


compressed_matrix = (
    fingerprint_result["compressed_matrix"]
)

row_density = (
    fingerprint_result["row_density"]
)

column_density = (
    fingerprint_result["column_density"]
)

fingerprint = (
    fingerprint_result["fingerprint"]
)


print()
print("Original binary matrix:")
print(result["binary"].shape)


print()
print("Compressed matrix:")
print(compressed_matrix.shape)


print()
print("Row density values:")
print(row_density)


print()
print("Column density values:")
print(column_density)


print()
print("======================================")
print("SIGNATURE FINGERPRINT:")
print(fingerprint)
print("======================================")


print()
print(
    "Fingerprint length:",
    len(fingerprint)
)