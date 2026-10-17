import csv
import os
from datetime import datetime

# Absolute path resolution ensuring reliability across local and cloud environments
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
HISTORY_FILE = os.path.join(RESULTS_DIR, "comparison_history.csv")

__all__ = ["save_comparison", "load_history", "clear_history", "HISTORY_FILE"]


def save_comparison(reference_path, test_path, similarity, similarity_level):
    """
    Save one signature comparison to the history CSV file.
    Compatible with file paths, file names, or uploaded stream objects.
    """
    os.makedirs(RESULTS_DIR, exist_ok=True)

    file_exists = os.path.exists(HISTORY_FILE)

    ref_name = os.path.basename(str(reference_path))
    test_name = os.path.basename(str(test_path))

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
            ref_name,
            test_name,
            f"{float(similarity):.2f}",
            similarity_level
        ])


def load_history():
    """
    Load comparison history records as a list of dictionaries.
    Returns an empty list if no history file exists yet.
    """
    if not os.path.exists(HISTORY_FILE):
        return []

    records = []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                records.append(row)
    except Exception:
        return []

    return records


def clear_history():
    """
    Clear comparison history file.
    """
    if os.path.exists(HISTORY_FILE):
        try:
            os.remove(HISTORY_FILE)
        except OSError:
            pass