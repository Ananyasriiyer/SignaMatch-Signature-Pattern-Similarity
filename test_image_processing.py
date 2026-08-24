from image_processing import preprocess_signature
from PIL import Image


# Your reference signature
image_path = "Signatures/reference/signature1.jpeg"


# Process the signature
result = preprocess_signature(image_path)


print("======================================")
print("     SIGNAMATCH IMAGE PROCESSING")
print("======================================")

print(
    "Original image size:",
    result["original"].size
)

print(
    "Grayscale image size:",
    result["grayscale"].size
)

print(
    "Resized image size:",
    result["resized"].size
)

print(
    "Binary matrix shape:",
    result["binary"].shape
)

print(
    "Binary matrix data type:",
    result["binary"].dtype
)

print("======================================")


# Save grayscale version
result["grayscale"].save(
    "results/grayscale_signature.png"
)


# Save 64 x 64 version
result["resized"].save(
    "results/resized_signature.png"
)


# Convert binary matrix into a visible image
binary_image = result["binary"] * 255

binary_image = Image.fromarray(
    binary_image.astype("uint8")
)


# Save black-and-white version
binary_image.save(
    "results/binary_signature.png"
)


print("Processed images saved in results folder.")