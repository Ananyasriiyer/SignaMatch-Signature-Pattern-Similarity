from difference_analysis import create_difference_image


# -------------------------------------------------
# CHANGE ONLY THESE FILE PATHS IF NEEDED
# -------------------------------------------------

reference_path = "Signatures/reference/signature1.jpeg"
test_path = "Signatures/test/signature2.jpeg"

output_path = "Results/signature_difference.png"


# -------------------------------------------------
# CREATE DIFFERENCE IMAGE
# -------------------------------------------------

result = create_difference_image(
    reference_path,
    test_path,
    output_path
)


print("Difference image created successfully!")
print("Saved at:", result)