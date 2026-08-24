import os
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from datetime import datetime

from PIL import Image, ImageTk

from difference_analysis import create_difference_image
from image_processing import preprocess_signature
from fingerprint import generate_fingerprint
from lcs import compare_fingerprints
from similarity import create_similarity_result
from explainable_result import explain_similarity
from comparison_history import save_comparison


# ============================================================
# CREATE RESULTS FOLDER
# ============================================================

os.makedirs("results", exist_ok=True)

DIFFERENCE_PATH = os.path.join(
    "results",
    "signature_difference.png"
)

HISTORY_FILE = os.path.join(
    "results",
    "comparison_history.csv"
)

REPORT_FILE = os.path.join(
    "results",
    "latest_result_report.txt"
)


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "SignaMatch - Signature Pattern Similarity Analyzer"
)

root.geometry(
    "1100x800"
)

root.configure(
    bg="#f4f6f8"
)

root.minsize(
    950,
    700
)


# ============================================================
# VARIABLES
# ============================================================

reference_path = None
test_path = None

comparison_done = False

reference_photo = None
test_photo = None

difference_photo = None

# Stage 11 - store latest comparison result
latest_result = {}


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    root,
    text="SIGNAMATCH",
    font=("Arial", 28, "bold"),
    bg="#f4f6f8"
)

title_label.pack(
    pady=(25, 5)
)


subtitle_label = tk.Label(
    root,
    text="Signature Pattern Similarity Analysis System",
    font=("Arial", 13),
    bg="#f4f6f8"
)

subtitle_label.pack(
    pady=(0, 20)
)


# ============================================================
# IMAGE AREA
# ============================================================

image_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

image_frame.pack(
    fill="x",
    padx=30
)


# ============================================================
# REFERENCE FRAME
# ============================================================

reference_frame = tk.Frame(
    image_frame,
    bg="white",
    bd=1,
    relief="solid"
)

reference_frame.pack(
    side="left",
    expand=True,
    fill="both",
    padx=10,
    pady=10
)


reference_title = tk.Label(
    reference_frame,
    text="REFERENCE SIGNATURE",
    font=("Arial", 14, "bold"),
    bg="white"
)

reference_title.pack(
    pady=10
)


reference_image_label = tk.Label(
    reference_frame,
    text="No signature selected",
    font=("Arial", 11),
    bg="white",
    width=40,
    height=12
)

reference_image_label.pack(
    padx=10,
    pady=10
)


# ============================================================
# TEST FRAME
# ============================================================

test_frame = tk.Frame(
    image_frame,
    bg="white",
    bd=1,
    relief="solid"
)

test_frame.pack(
    side="right",
    expand=True,
    fill="both",
    padx=10,
    pady=10
)


test_title = tk.Label(
    test_frame,
    text="TEST SIGNATURE",
    font=("Arial", 14, "bold"),
    bg="white"
)

test_title.pack(
    pady=10
)


test_image_label = tk.Label(
    test_frame,
    text="No signature selected",
    font=("Arial", 11),
    bg="white",
    width=40,
    height=12
)

test_image_label.pack(
    padx=10,
    pady=10
)


# ============================================================
# BUTTON FRAME
# ============================================================

button_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

button_frame.pack(
    pady=15
)


# ============================================================
# IMAGE DISPLAY FUNCTION
# ============================================================

def display_image(
    image_path,
    image_label,
    image_type
):

    global reference_photo
    global test_photo

    try:

        image = Image.open(
            image_path
        )

        image.thumbnail(
            (350, 220)
        )

        photo = ImageTk.PhotoImage(
            image
        )

        image_label.configure(
            image=photo,
            text=""
        )

        image_label.image = photo

        if image_type == "reference":

            reference_photo = photo

        else:

            test_photo = photo

    except Exception as error:

        messagebox.showerror(
            "Image Error",
            f"Unable to display image.\n\n{error}"
        )


# ============================================================
# SELECT REFERENCE SIGNATURE
# ============================================================

def select_reference():

    global reference_path
    global comparison_done

    selected_file = filedialog.askopenfilename(
        title="Select Reference Signature",
        filetypes=[
            (
                "Image Files",
                "*.jpg *.jpeg *.png"
            )
        ]
    )

    if not selected_file:
        return

    reference_path = selected_file
    comparison_done = False

    display_image(
        reference_path,
        reference_image_label,
        "reference"
    )

    reference_name_label.configure(
        text=(
            "Reference: "
            + os.path.basename(reference_path)
        )
    )

    check_ready()


# ============================================================
# SELECT TEST SIGNATURE
# ============================================================

def select_test():

    global test_path
    global comparison_done

    selected_file = filedialog.askopenfilename(
        title="Select Test Signature",
        filetypes=[
            (
                "Image Files",
                "*.jpg *.jpeg *.png"
            )
        ]
    )

    if not selected_file:
        return

    test_path = selected_file
    comparison_done = False

    display_image(
        test_path,
        test_image_label,
        "test"
    )

    test_name_label.configure(
        text=(
            "Test: "
            + os.path.basename(test_path)
        )
    )

    check_ready()


# ============================================================
# BUTTONS
# ============================================================

reference_button = tk.Button(
    button_frame,
    text="Select Reference",
    command=select_reference,
    font=("Arial", 11, "bold"),
    padx=20,
    pady=8
)

reference_button.pack(
    side="left",
    padx=10
)


test_button = tk.Button(
    button_frame,
    text="Select Test Signature",
    command=select_test,
    font=("Arial", 11, "bold"),
    padx=20,
    pady=8
)

test_button.pack(
    side="left",
    padx=10
)


# ============================================================
# FILE NAME LABELS
# ============================================================

name_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

name_frame.pack(
    fill="x",
    padx=50
)


reference_name_label = tk.Label(
    name_frame,
    text="Reference: Not selected",
    font=("Arial", 10),
    bg="#f4f6f8"
)

reference_name_label.pack(
    side="left"
)


test_name_label = tk.Label(
    name_frame,
    text="Test: Not selected",
    font=("Arial", 10),
    bg="#f4f6f8"
)

test_name_label.pack(
    side="right"
)


# ============================================================
# CHECK WHETHER BOTH IMAGES ARE SELECTED
# ============================================================

def check_ready():

    if (
        reference_path is not None
        and test_path is not None
    ):

        compare_button.config(
            state="normal"
        )


# ============================================================
# STAGE 11
# GENERATE RESULT REPORT
# ============================================================

def generate_result_report():

    if not latest_result:

        messagebox.showwarning(
            "No Result",
            "Please compare two signatures first."
        )

        return

    try:

        report_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        report_text = ""

        report_text += "=" * 60 + "\n"
        report_text += "SIGNAMATCH - SIGNATURE COMPARISON REPORT\n"
        report_text += "=" * 60 + "\n\n"

        report_text += (
            "Date and Time: "
            + report_time
            + "\n\n"
        )

        report_text += (
            "Reference Signature:\n"
            + str(
                latest_result["reference_path"]
            )
            + "\n\n"
        )

        report_text += (
            "Test Signature:\n"
            + str(
                latest_result["test_path"]
            )
            + "\n\n"
        )

        report_text += "-" * 60 + "\n"
        report_text += "COMPARISON RESULTS\n"
        report_text += "-" * 60 + "\n\n"

        report_text += (
            "Reference Fingerprint:\n"
            + str(
                latest_result["reference_fingerprint"]
            )
            + "\n\n"
        )

        report_text += (
            "Test Fingerprint:\n"
            + str(
                latest_result["test_fingerprint"]
            )
            + "\n\n"
        )

        report_text += (
            "LCS Length: "
            + str(
                latest_result["lcs_length"]
            )
            + " / "
            + str(
                latest_result["reference_length"]
            )
            + "\n\n"
        )

        report_text += (
            "Similarity Percentage: "
            + str(
                round(
                    latest_result["percentage"],
                    2
                )
            )
            + "%\n\n"
        )

        report_text += (
            "Classification:\n"
            + str(
                latest_result["classification"]
            )
            + "\n\n"
        )

        report_text += (
            "Similarity Level:\n"
            + str(
                latest_result["level"]
            )
            + "\n\n"
        )

        report_text += (
            "Explanation:\n"
            + str(
                latest_result["explanation"]
            )
            + "\n\n"
        )

        report_text += (
            "Recommendation:\n"
            + str(
                latest_result["recommendation"]
            )
            + "\n\n"
        )

        report_text += "=" * 60 + "\n"
        report_text += "END OF REPORT\n"
        report_text += "=" * 60 + "\n"


        with open(
            REPORT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                report_text
            )


        messagebox.showinfo(
            "Report Generated",
            "Result report has been generated successfully.\n\n"
            "Saved at:\n"
            + REPORT_FILE
        )


    except Exception as error:

        messagebox.showerror(
            "Report Error",
            "Unable to generate result report.\n\n"
            + str(error)
        )


# ============================================================
# STAGE 11
# VIEW COMPARISON HISTORY
# ============================================================

def view_comparison_history():

    if not os.path.exists(HISTORY_FILE):

        messagebox.showinfo(
            "Comparison History",
            "No comparison history found yet.\n\n"
            "Please compare at least two signatures first."
        )

        return


    try:

        history_window = tk.Toplevel(
            root
        )

        history_window.title(
            "Comparison History"
        )

        history_window.geometry(
            "1050x500"
        )

        history_window.configure(
            bg="#f4f6f8"
        )


        # ====================================================
        # TITLE
        # ====================================================

        history_title = tk.Label(
            history_window,
            text="COMPARISON HISTORY",
            font=("Arial", 20, "bold"),
            bg="#f4f6f8"
        )

        history_title.pack(
            pady=15
        )


        # ====================================================
        # TABLE FRAME
        # ====================================================

        table_frame = tk.Frame(
            history_window,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )


        # ====================================================
        # SCROLLBARS
        # ====================================================

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical"
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal"
        )


        # ====================================================
        # TREEVIEW
        # ====================================================

        columns = (
            "Date and Time",
            "Reference Signature",
            "Test Signature",
            "Similarity Percentage",
            "Similarity Level"
        )


        history_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )


        vertical_scrollbar.config(
            command=history_table.yview
        )

        horizontal_scrollbar.config(
            command=history_table.xview
        )


        # ====================================================
        # COLUMN HEADINGS
        # ====================================================

        for column in columns:

            history_table.heading(
                column,
                text=column
            )


        history_table.column(
            "Date and Time",
            width=150
        )

        history_table.column(
            "Reference Signature",
            width=250
        )

        history_table.column(
            "Test Signature",
            width=250
        )

        history_table.column(
            "Similarity Percentage",
            width=160
        )

        history_table.column(
            "Similarity Level",
            width=180
        )


        # ====================================================
        # READ CSV
        # ====================================================

        with open(
            HISTORY_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.reader(
                file
            )

            rows = list(
                reader
            )


        # ====================================================
        # INSERT DATA
        # ====================================================

        if len(rows) > 1:

            for row in rows[1:]:

                if len(row) >= 5:

                    history_table.insert(
                        "",
                        "end",
                        values=(
                            row[0],
                            row[1],
                            row[2],
                            row[3] + "%",
                            row[4]
                        )
                    )


        # ====================================================
        # PACK TABLE
        # ====================================================

        history_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        vertical_scrollbar.pack(
            side="right",
            fill="y"
        )

        horizontal_scrollbar.pack(
            side="bottom",
            fill="x"
        )


        # ====================================================
        # CLOSE BUTTON
        # ====================================================

        close_button = tk.Button(
            history_window,
            text="CLOSE",
            command=history_window.destroy,
            font=("Arial", 11, "bold"),
            width=15
        )

        close_button.pack(
            pady=15
        )


    except Exception as error:

        messagebox.showerror(
            "History Error",
            "Unable to display comparison history.\n\n"
            + str(error)
        )


# ============================================================
# COMPARISON FUNCTION
# ============================================================

def compare_signatures():

    global comparison_done
    global latest_result

    comparison_done = False

    if reference_path is None:

        messagebox.showwarning(
            "Missing Signature",
            "Please select the reference signature."
        )

        return


    if test_path is None:

        messagebox.showwarning(
            "Missing Signature",
            "Please select the test signature."
        )

        return


    try:

        # ====================================================
        # CREATE DIFFERENCE IMAGE
        # STAGE 9
        # ====================================================

        create_difference_image(
            reference_path,
            test_path,
            DIFFERENCE_PATH
        )


        # ====================================================
        # PROCESS REFERENCE
        # ====================================================

        reference_image = (
            preprocess_signature(
                reference_path
            )
        )

        reference_result = (
            generate_fingerprint(
                reference_image["binary"]
            )
        )

        reference_fingerprint = (
            reference_result["fingerprint"]
        )


        # ====================================================
        # PROCESS TEST
        # ====================================================

        test_image = (
            preprocess_signature(
                test_path
            )
        )

        test_result = (
            generate_fingerprint(
                test_image["binary"]
            )
        )

        test_fingerprint = (
            test_result["fingerprint"]
        )


        # ====================================================
        # LCS COMPARISON
        # ====================================================

        comparison = (
            compare_fingerprints(
                reference_fingerprint,
                test_fingerprint
            )
        )

        lcs_length = (
            comparison["lcs_length"]
        )


        # ====================================================
        # SIMILARITY
        # STAGES 5/6/7/8
        # ====================================================

        similarity_result = (
            create_similarity_result(
                lcs_length,
                len(reference_fingerprint)
            )
        )


        percentage = (
            similarity_result[
                "similarity_percentage"
            ]
        )

        classification = (
            similarity_result[
                "classification"
            ]
        )


        # ====================================================
        # STAGE 10
        # EXPLAINABLE SIMILARITY RESULT
        # ====================================================

        explanation = explain_similarity(
            percentage
        )


        # ====================================================
        # DISPLAY FINGERPRINT RESULT
        # ====================================================

        fingerprint_result_label.config(
            text=(
                "Reference: "
                + reference_fingerprint
                + "\n"
                + "Test:       "
                + test_fingerprint
            )
        )


        # ====================================================
        # DISPLAY LCS RESULT
        # ====================================================

        lcs_result_label.config(
            text=(
                "LCS Length: "
                + str(lcs_length)
                + " / "
                + str(
                    len(
                        reference_fingerprint
                    )
                )
            )
        )


        # ====================================================
        # DISPLAY SIMILARITY
        # ====================================================

        similarity_result_label.config(
            text=(
                "Similarity: "
                + str(
                    round(
                        percentage,
                        2
                    )
                )
                + "%"
            )
        )


        # ====================================================
        # DISPLAY CLASSIFICATION
        # ====================================================

        classification_result_label.config(
            text=classification
        )


        # ====================================================
        # STAGE 10
        # DISPLAY EXPLAINABLE RESULT
        # ====================================================

        explanation_level_label.config(
            text=(
                "Similarity Level: "
                + explanation["level"]
            )
        )


        explanation_label.config(
            text=(
                "Explanation:\n"
                + explanation["explanation"]
            )
        )


        recommendation_label.config(
            text=(
                "Recommendation:\n"
                + explanation["recommendation"]
            )
        )


        # ====================================================
        # SUCCESS MESSAGE FOR DIFFERENCE ANALYSIS
        # ====================================================

        if os.path.exists(
            DIFFERENCE_PATH
        ):

            difference_button.config(
                state="normal"
            )


        # ====================================================
        # STAGE 11
        # SAVE COMPARISON HISTORY
        # ====================================================

        save_comparison(
            reference_path,
            test_path,
            percentage,
            explanation["level"]
        )


        # ====================================================
        # STAGE 11
        # STORE LATEST RESULT
        # FOR RESULT REPORT
        # ====================================================

        latest_result = {

            "reference_path":
                reference_path,

            "test_path":
                test_path,

            "reference_fingerprint":
                reference_fingerprint,

            "test_fingerprint":
                test_fingerprint,

            "lcs_length":
                lcs_length,

            "reference_length":
                len(
                    reference_fingerprint
                ),

            "percentage":
                percentage,

            "classification":
                classification,

            "level":
                explanation["level"],

            "explanation":
                explanation["explanation"],

            "recommendation":
                explanation["recommendation"]
        }


        # ====================================================
        # ENABLE STAGE 11 BUTTONS
        # ====================================================

        history_button.config(
            state="normal"
        )

        report_button.config(
            state="normal"
        )


        # ====================================================
        # COMPARISON COMPLETED
        # ====================================================

        comparison_done = True


        # ====================================================
        # STAGE 11 SUCCESS MESSAGE
        # ====================================================

        messagebox.showinfo(
            "Comparison Completed",
            "Signature comparison completed successfully.\n\n"
            "Similarity: "
            + str(
                round(
                    percentage,
                    2
                )
            )
            + "%\n\n"
            "Comparison history has been saved."
        )


    except Exception as error:

        messagebox.showerror(
            "Comparison Error",
            "Something went wrong while "
            "comparing the signatures.\n\n"
            + str(error)
        )


# ============================================================
# VIEW DIFFERENCE FUNCTION
# ============================================================

def view_difference():

    global difference_photo

    difference_path = DIFFERENCE_PATH


    # ========================================================
    # CHECK DIFFERENCE IMAGE
    # ========================================================

    if not os.path.exists(
        difference_path
    ):

        messagebox.showwarning(
            "Difference Image",
            "Please compare two signatures first."
        )

        return


    try:

        # ====================================================
        # CREATE NEW WINDOW
        # ====================================================

        difference_window = tk.Toplevel(
            root
        )

        difference_window.title(
            "Signature Difference Analysis"
        )

        difference_window.geometry(
            "700x600"
        )


        # ====================================================
        # TITLE
        # ====================================================

        difference_title_label = tk.Label(
            difference_window,
            text="VISUAL DIFFERENCE ANALYSIS",
            font=("Arial", 20, "bold")
        )

        difference_title_label.pack(
            pady=15
        )


        # ====================================================
        # OPEN DIFFERENCE IMAGE
        # ====================================================

        image = Image.open(
            difference_path
        )


        # ====================================================
        # RESIZE IMAGE
        # ====================================================

        image.thumbnail(
            (600, 450)
        )


        # ====================================================
        # CONVERT FOR TKINTER
        # ====================================================

        difference_photo = ImageTk.PhotoImage(
            image
        )


        # ====================================================
        # DISPLAY IMAGE
        # ====================================================

        image_label = tk.Label(
            difference_window,
            image=difference_photo
        )

        image_label.image = difference_photo

        image_label.pack(
            pady=10
        )


        # ====================================================
        # EXPLANATION
        # ====================================================

        info_label = tk.Label(
            difference_window,
            text=(
                "Black/white regions represent "
                "detected pixel differences."
            ),
            font=("Arial", 11)
        )

        info_label.pack(
            pady=10
        )


        # ====================================================
        # CLOSE BUTTON
        # ====================================================

        close_button = tk.Button(
            difference_window,
            text="CLOSE",
            command=difference_window.destroy,
            font=("Arial", 12, "bold"),
            width=15
        )

        close_button.pack(
            pady=10
        )


    except Exception as error:

        messagebox.showerror(
            "Difference Analysis Error",
            "Unable to display difference image.\n\n"
            + str(error)
        )


# ============================================================
# COMPARE BUTTON
# ============================================================

compare_button = tk.Button(
    root,
    text="COMPARE SIGNATURES",
    command=compare_signatures,
    font=("Arial", 13, "bold"),
    padx=35,
    pady=10,
    state="disabled"
)

compare_button.pack(
    pady=15
)


# ============================================================
# VIEW DIFFERENCE BUTTON
# ============================================================

difference_button = tk.Button(
    root,
    text="VIEW DIFFERENCE",
    command=view_difference,
    font=("Arial", 12, "bold"),
    padx=30,
    pady=8,
    state="disabled"
)

difference_button.pack(
    pady=5
)


# ============================================================
# STAGE 11 BUTTON FRAME
# ============================================================

stage11_button_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

stage11_button_frame.pack(
    pady=8
)


# ============================================================
# VIEW COMPARISON HISTORY BUTTON
# ============================================================

history_button = tk.Button(
    stage11_button_frame,
    text="VIEW COMPARISON HISTORY",
    command=view_comparison_history,
    font=("Arial", 11, "bold"),
    padx=20,
    pady=8,
    state="disabled"
)

history_button.pack(
    side="left",
    padx=8
)


# ============================================================
# GENERATE RESULT REPORT BUTTON
# ============================================================

report_button = tk.Button(
    stage11_button_frame,
    text="GENERATE RESULT REPORT",
    command=generate_result_report,
    font=("Arial", 11, "bold"),
    padx=20,
    pady=8,
    state="disabled"
)

report_button.pack(
    side="left",
    padx=8
)


# ============================================================
# RESULT FRAME
# ============================================================

result_frame = tk.Frame(
    root,
    bg="white",
    bd=1,
    relief="solid"
)

result_frame.pack(
    fill="x",
    padx=80,
    pady=10
)


# ============================================================
# RESULT TITLE
# ============================================================

result_title_label = tk.Label(
    result_frame,
    text="ANALYSIS RESULT",
    font=("Arial", 16, "bold"),
    bg="white"
)

result_title_label.pack(
    pady=(15, 8)
)


# ============================================================
# FINGERPRINT RESULT
# ============================================================

fingerprint_result_label = tk.Label(
    result_frame,
    text="Fingerprints will appear here.",
    font=("Courier New", 10),
    bg="white"
)

fingerprint_result_label.pack(
    pady=5
)


# ============================================================
# LCS RESULT
# ============================================================

lcs_result_label = tk.Label(
    result_frame,
    text="LCS Length: --",
    font=("Arial", 11),
    bg="white"
)

lcs_result_label.pack(
    pady=3
)


# ============================================================
# SIMILARITY RESULT
# ============================================================

similarity_result_label = tk.Label(
    result_frame,
    text="Similarity: --",
    font=("Arial", 18, "bold"),
    bg="white"
)

similarity_result_label.pack(
    pady=5
)


# ============================================================
# CLASSIFICATION RESULT
# ============================================================

classification_result_label = tk.Label(
    result_frame,
    text="Waiting for comparison",
    font=("Arial", 13, "bold"),
    bg="white"
)

classification_result_label.pack(
    pady=(3, 10)
)


# ============================================================
# STAGE 10.7
# EXPLAINABLE SIMILARITY RESULT FRAME
# ============================================================

explanation_frame = tk.Frame(
    result_frame,
    bg="white"
)

explanation_frame.pack(
    fill="x",
    padx=20,
    pady=(5, 15)
)


# ============================================================
# SIMILARITY LEVEL
# ============================================================

explanation_level_label = tk.Label(
    explanation_frame,
    text="Similarity Level: --",
    font=("Arial", 13, "bold"),
    bg="white"
)

explanation_level_label.pack(
    pady=5
)


# ============================================================
# EXPLANATION
# ============================================================

explanation_label = tk.Label(
    explanation_frame,
    text="Explanation:\n--",
    font=("Arial", 11),
    bg="white",
    justify="left",
    wraplength=850
)

explanation_label.pack(
    pady=5
)


# ============================================================
# RECOMMENDATION
# ============================================================

recommendation_label = tk.Label(
    explanation_frame,
    text="Recommendation:\n--",
    font=("Arial", 11),
    bg="white",
    justify="left",
    wraplength=850
)

recommendation_label.pack(
    pady=5
)


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()