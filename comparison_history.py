import csv
import os
from datetime import datetime


HISTORY_FILE = "results/comparison_history.csv"


def save_comparison(reference_path, test_path, similarity, similarity_level):
    """
    Save one signature comparison to the history CSV file.
    """

    os.makedirs("results", exist_ok=True)

    file_exists = os.path.exists(HISTORY_FILE)

    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Date and Time",
                "Reference Signature",
                "Test Signature",
                "Similarity Percentage",
                "Similarity Level"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            reference_path,
            test_path,
            f"{float(similarity):.2f}",
            similarity_level
        ])
       