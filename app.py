import os
import io
import time
from datetime import datetime
from PIL import Image, UnidentifiedImageError
import streamlit as st
import pandas as pd
import numpy as np

# Import existing core modular algorithms (Original logic preserved)
from image_processing import (
    load_image,
    convert_to_grayscale,
    resize_image,
    convert_to_binary,
    preprocess_signature
)
from fingerprint import (
    generate_fingerprint,
    compress_matrix,
    calculate_row_density,
    calculate_column_density,
    combine_row_column_density
)
from lcs import (
    calculate_lcs_length,
    calculate_similarity,
    compare_fingerprints,
    get_lcs_subsequence
)
from similarity import create_similarity_result, classify_similarity
from difference_analysis import create_difference_image
from explainable_result import explain_similarity
from comparison_history import save_comparison, load_history, clear_history
import config

# ============================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="SignaMatch - Signature Verification using LCS",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, professional, high-contrast UI
st.markdown("""
<style>
    /* Main container enhancements */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1200px;
    }
    
    /* Hero Title styling */
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(120deg, #1E3A8A, #2563EB, #0284C7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .hero-sub {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    /* Card container */
    .custom-card {
        background-color: var(--secondary-background-color, #F8FAFC);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -2px rgba(0, 0, 0, 0.04);
    }
    
    .badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        font-size: 0.85rem;
        font-weight: 700;
        border-radius: 9999px;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    
    .badge-very-high { background-color: #DEF7EC; color: #03543F; border: 1px solid #31C48D; }
    .badge-high { background-color: #E1EFFE; color: #1E429F; border: 1px solid #76A9FA; }
    .badge-moderate { background-color: #FEF08A; color: #713F12; border: 1px solid #FACC15; }
    .badge-low { background-color: #FDE8E8; color: #9B1C1C; border: 1px solid #F98080; }
    
    .fingerprint-box {
        font-family: 'Courier New', Courier, monospace;
        background-color: #0F172A;
        color: #38BDF8;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-size: 1.15rem;
        letter-spacing: 0.2em;
        font-weight: 700;
        display: inline-block;
        margin-top: 0.3rem;
        border: 1px solid #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# Ensure results directory exists
os.makedirs("results", exist_ok=True)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if "reference_image" not in st.session_state:
    st.session_state.reference_image = None
if "reference_name" not in st.session_state:
    st.session_state.reference_name = ""
if "test_image" not in st.session_state:
    st.session_state.test_image = None
if "test_name" not in st.session_state:
    st.session_state.test_name = ""
if "comparison_result" not in st.session_state:
    st.session_state.comparison_result = None

# ============================================================
# INPUT VALIDATION & HELPER FUNCTIONS
# ============================================================
def validate_and_load_image(uploaded_file):
    """
    Validates uploaded file integrity, format, dimensions, and size.
    Returns: (PIL.Image or None, error_message or None)
    """
    if uploaded_file is None:
        return None, None

    try:
        # Check size (max 20 MB)
        uploaded_file.seek(0, io.SEEK_END)
        file_size = uploaded_file.tell()
        uploaded_file.seek(0)

        if file_size == 0:
            return None, "The uploaded file is empty (0 bytes). Please upload a valid image file."

        if file_size > 20 * 1024 * 1024:
            return None, f"File size ({file_size / (1024 * 1024):.1f} MB) exceeds the 20 MB limit."

        # Verify image integrity using PIL
        try:
            image = Image.open(uploaded_file)
            image.verify()
        except (UnidentifiedImageError, OSError, ValueError) as err:
            return None, f"Cannot parse image: The file is corrupted or not a supported image format. ({err})"

        # Reopen after verify() (PIL requires reopen after verify)
        uploaded_file.seek(0)
        image = Image.open(uploaded_file)
        image.load()

        # Dimension checks
        if image.width < 10 or image.height < 10:
            return None, f"Image dimensions ({image.width}×{image.height} px) are too small. Minimum size is 10×10 pixels."

        return image, None

    except Exception as exc:
        return None, f"Unexpected error while reading image: {str(exc)}"

def load_sample_file(rel_path):
    """Safely loads a sample image from the Signatures directory."""
    if os.path.exists(rel_path):
        try:
            return Image.open(rel_path)
        except Exception:
            return None
    return None

def reset_all():
    """Resets all uploaded and calculated data."""
    st.session_state.reference_image = None
    st.session_state.reference_name = ""
    st.session_state.test_image = None
    st.session_state.test_name = ""
    st.session_state.comparison_result = None
    st.rerun()

# ============================================================
# SIDEBAR CONTROLS
# ============================================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/signature.png", width=64)
    st.title("SignaMatch")
    st.caption("v2.0 • LCS Signature Analyzer")
    st.markdown("---")
    
    st.subheader("💡 Demo Signature Pairs")
    st.caption("Select a preset pair for instant verification:")
    sample_choice = st.selectbox(
        "Load demo pair:",
        [
            "Select a preset pair...",
            "Demo 1: Reference 1 vs Test 2 (Original Test Pair)",
            "Demo 2: Reference 1 vs Extra Signature 3",
            "Demo 3: Extra Signature 3 vs Extra Signature 4",
            "Demo 4: Exact Match (Reference 1 vs Reference 1)"
        ],
        key="sample_selector"
    )

    if sample_choice == "Demo 1: Reference 1 vs Test 2 (Original Test Pair)":
        st.session_state.reference_image = load_sample_file("Signatures/reference/signature1.jpeg")
        st.session_state.reference_name = "signature1.jpeg (Reference)"
        st.session_state.test_image = load_sample_file("Signatures/test/signature2.jpeg")
        st.session_state.test_name = "signature2.jpeg (Test)"
    elif sample_choice == "Demo 2: Reference 1 vs Extra Signature 3":
        st.session_state.reference_image = load_sample_file("Signatures/reference/signature1.jpeg")
        st.session_state.reference_name = "signature1.jpeg (Reference)"
        st.session_state.test_image = load_sample_file("Signatures/extra/Signature3.jpeg")
        st.session_state.test_name = "Signature3.jpeg (Extra)"
    elif sample_choice == "Demo 3: Extra Signature 3 vs Extra Signature 4":
        st.session_state.reference_image = load_sample_file("Signatures/extra/Signature3.jpeg")
        st.session_state.reference_name = "Signature3.jpeg (Extra)"
        st.session_state.test_image = load_sample_file("Signatures/extra/Signature4.jpeg")
        st.session_state.test_name = "Signature4.jpeg (Extra)"
    elif sample_choice == "Demo 4: Exact Match (Reference 1 vs Reference 1)":
        st.session_state.reference_image = load_sample_file("Signatures/reference/signature1.jpeg")
        st.session_state.reference_name = "signature1.jpeg (Original)"
        st.session_state.test_image = load_sample_file("Signatures/reference/signature1.jpeg")
        st.session_state.test_name = "signature1.jpeg (Duplicate)"

    st.markdown("---")
    st.subheader("⚙️ Processing Parameters")
    custom_threshold = st.slider(
        "Binarization Threshold (Ink vs Background):",
        min_value=50,
        max_value=220,
        value=config.THRESHOLD,
        step=1,
        help=f"Default is {config.THRESHOLD}. Pixels with grayscale value below this are treated as ink."
    )
    st.write(f"• **Grid Resolution:** {config.IMAGE_WIDTH} × {config.IMAGE_HEIGHT} px")
    st.write(f"• **Compression Grid:** {config.COMPRESSED_WIDTH} × {config.COMPRESSED_HEIGHT} blocks")
    
    st.markdown("---")
    st.subheader("🔄 Reset Controls")
    if st.button("🗑️ Reset All Data", use_container_width=True, type="secondary"):
        reset_all()

    st.markdown("---")
    st.markdown("""
    **Algorithm Steps:**
    1. Grayscale & Alpha Flattening
    2. Spatial Normalization (64×64)
    3. Binary Ink Masking
    4. 16×16 Average Density Pooling
    5. Row/Col Density Vector Combination
    6. 16-level Hex Quantization
    7. 2D Dynamic Programming LCS
    """)

# ============================================================
# HEADER
# ============================================================
col_header, col_reset = st.columns([3, 1])
with col_header:
    st.markdown('<div class="hero-title">SignaMatch Verification System</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Handwritten signature biometric pattern comparison utilizing the Longest Common Subsequence (LCS) algorithm.</div>', unsafe_allow_html=True)

with col_reset:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Clear / Reset", use_container_width=True):
        reset_all()

# ============================================================
# IMAGE UPLOAD & PREVIEW SECTION WITH VALIDATION
# ============================================================
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 1️⃣ Reference Signature (Genuine)")
    ref_upload = st.file_uploader(
        "Upload authentic signature (PNG, JPG, JPEG):",
        type=["png", "jpg", "jpeg"],
        key="ref_file_uploader"
    )
    if ref_upload is not None:
        validated_img, err_msg = validate_and_load_image(ref_upload)
        if err_msg:
            st.error(f"❌ Reference Signature Error: {err_msg}")
        else:
            st.session_state.reference_image = validated_img
            st.session_state.reference_name = ref_upload.name

    if st.session_state.reference_image is not None:
        st.image(
            st.session_state.reference_image,
            caption=f"Reference: {st.session_state.reference_name}",
            use_container_width=True
        )
        img_w, img_h = st.session_state.reference_image.size
        st.caption(f"📐 Dimensions: {img_w} × {img_h} px | Mode: {st.session_state.reference_image.mode}")
    else:
        st.info("👆 Upload an authentic reference signature image or select a demo pair from the sidebar.")

with col2:
    st.markdown("### 2️⃣ Test Signature (Questioned)")
    test_upload = st.file_uploader(
        "Upload test signature to verify (PNG, JPG, JPEG):",
        type=["png", "jpg", "jpeg"],
        key="test_file_uploader"
    )
    if test_upload is not None:
        validated_img, err_msg = validate_and_load_image(test_upload)
        if err_msg:
            st.error(f"❌ Test Signature Error: {err_msg}")
        else:
            st.session_state.test_image = validated_img
            st.session_state.test_name = test_upload.name

    if st.session_state.test_image is not None:
        st.image(
            st.session_state.test_image,
            caption=f"Test: {st.session_state.test_name}",
            use_container_width=True
        )
        img_w, img_h = st.session_state.test_image.size
        st.caption(f"📐 Dimensions: {img_w} × {img_h} px | Mode: {st.session_state.test_image.mode}")
    else:
        st.info("👆 Upload a test / questioned signature image or select a demo pair from the sidebar.")

st.markdown("---")

# ============================================================
# COMPARISON EXECUTION (INPUT VALIDATION & CONNECTED ALGORITHM)
# ============================================================
has_reference = st.session_state.reference_image is not None
has_test = st.session_state.test_image is not None

col_btn, col_info = st.columns([1, 2])
with col_btn:
    run_comparison = st.button(
        "🔍 Compare Signatures",
        type="primary",
        disabled=not (has_reference and has_test),
        use_container_width=True
    )

with col_info:
    if not has_reference and not has_test:
        st.warning("⚠️ Please provide both the Reference and Test signatures to enable comparison.")
    elif not has_reference:
        st.warning("⚠️ Reference signature is missing. Please upload or select one.")
    elif not has_test:
        st.warning("⚠️ Test signature is missing. Please upload or select one.")
    else:
        st.success("✅ Both signatures loaded and validated. Ready for algorithmic LCS verification.")

if run_comparison:
    # Explicit double-check validation before execution
    if not has_reference or not has_test:
        st.error("Validation Error: Both signature images must be provided before running comparison.")
    else:
        try:
            with st.spinner("Executing biometric feature extraction and Dynamic Programming LCS matching..."):
                start_time = time.time()
                
                # Step 1: Preprocess both signatures (Grayscale -> 64x64 Resize -> Binary Matrix)
                ref_prep = preprocess_signature(
                    st.session_state.reference_image,
                    threshold=custom_threshold
                )
                test_prep = preprocess_signature(
                    st.session_state.test_image,
                    threshold=custom_threshold
                )
                
                # Step 2: Generate 16-character hexadecimal biometric fingerprints
                ref_fp_data = generate_fingerprint(ref_prep["binary"])
                test_fp_data = generate_fingerprint(test_prep["binary"])
                
                ref_fp = ref_fp_data["fingerprint"]
                test_fp = test_fp_data["fingerprint"]
                
                # Step 3: Run Dynamic Programming LCS algorithm
                lcs_res = compare_fingerprints(ref_fp, test_fp)
                lcs_len = lcs_res["lcs_length"]
                sim_pct = lcs_res["similarity"]
                lcs_subseq = get_lcs_subsequence(ref_fp, test_fp)
                
                # Step 4: Classify similarity and generate forensic explanation
                sim_result = create_similarity_result(lcs_len, len(ref_fp))
                explanation_data = explain_similarity(sim_pct)
                
                # Step 5: Visual pixel-by-pixel difference analysis
                diff_result = create_difference_image(
                    st.session_state.reference_image,
                    st.session_state.test_image,
                    output_path=os.path.join("results", "signature_difference.png")
                )
                if isinstance(diff_result, str):
                    diff_img = Image.open(diff_result)
                else:
                    diff_img = diff_result
                
                # Step 6: Log to audit history CSV
                save_comparison(
                    st.session_state.reference_name or "Reference",
                    st.session_state.test_name or "Test",
                    sim_pct,
                    explanation_data["level"]
                )
                
                elapsed_ms = (time.time() - start_time) * 1000.0

                # Store result in session state
                st.session_state.comparison_result = {
                    "ref_prep": ref_prep,
                    "test_prep": test_prep,
                    "ref_fp_data": ref_fp_data,
                    "test_fp_data": test_fp_data,
                    "ref_fp": ref_fp,
                    "test_fp": test_fp,
                    "lcs_len": lcs_len,
                    "lcs_subseq": lcs_subseq,
                    "sim_pct": sim_pct,
                    "sim_result": sim_result,
                    "explanation": explanation_data,
                    "diff_img": diff_img,
                    "elapsed_ms": elapsed_ms
                }

        except Exception as exc:
            st.error(f"❌ An error occurred during algorithm execution: {str(exc)}")
            st.info("Tip: Ensure the images are clear signature drawings or scans on relatively uniform backgrounds.")

# ============================================================
# RESULTS PRESENTATION (TABS)
# ============================================================
if st.session_state.comparison_result is not None:
    res = st.session_state.comparison_result
    pct = res["sim_pct"]
    level = res["explanation"]["level"]

    # Assign color and badge styles
    if pct >= 90:
        badge_cls = "badge-very-high"
    elif pct >= 75:
        badge_cls = "badge-high"
    elif pct >= 50:
        badge_cls = "badge-moderate"
    else:
        badge_cls = "badge-low"

    st.markdown("## 📊 Comparison Analysis")
    
    # Primary KPI metrics row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Similarity Score", value=f"{pct:.2f} %")
    with m2:
        st.metric(label="LCS Match Length", value=f"{res['lcs_len']} / {len(res['ref_fp'])}")
    with m3:
        st.metric(label="Match Verdict", value=res["sim_result"]["classification"])
    with m4:
        st.metric(label="Execution Time", value=f"{res['elapsed_ms']:.1f} ms")

    # Visual progress bar
    st.progress(pct / 100.0)

    # Detailed inspection tabs
    tab_summary, tab_diff, tab_pipeline, tab_history = st.tabs([
        "📋 Verification Summary",
        "🔍 Visual Difference Map",
        "🧬 LCS & Pipeline Inspector",
        "📜 Comparison History & Audit"
    ])

    with tab_summary:
        st.markdown(f"""
        <div class="custom-card">
            <h4>Verdict Status: <span class="badge {badge_cls}">{level}</span></h4>
            <p style="font-size: 1.05rem; margin-top: 0.5rem; line-height: 1.6;">
                <strong>Forensic Explanation:</strong> {res["explanation"]["explanation"]}<br>
                <strong>Recommendation:</strong> {res["explanation"]["recommendation"]}
            </p>
        </div>
        """, unsafe_allow_html=True)

        c_fp1, c_fp2 = st.columns(2)
        with c_fp1:
            st.markdown("**Reference Biometric Fingerprint (16-char Hex):**")
            st.markdown(f'<div class="fingerprint-box">{res["ref_fp"]}</div>', unsafe_allow_html=True)
            st.caption("Extracted density distribution across 16 block vectors")
        with c_fp2:
            st.markdown("**Test Biometric Fingerprint (16-char Hex):**")
            st.markdown(f'<div class="fingerprint-box">{res["test_fp"]}</div>', unsafe_allow_html=True)
            st.caption("Extracted density distribution across 16 block vectors")

        st.markdown(f"""
        **Matched Longest Common Subsequence (LCS):**  
        `{res["lcs_subseq"]}` *(Length: **{res["lcs_len"]}** / {len(res["ref_fp"])} sequential tokens matched)*
        """)

        # Downloadable comprehensive forensic report
        report_text = f"""================================================================================
                       SIGNAMATCH VERIFICATION REPORT
================================================================================
Date and Time:           {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Reference Signature:     {st.session_state.reference_name}
Test Signature:          {st.session_state.test_name}
--------------------------------------------------------------------------------
Reference Fingerprint:   {res["ref_fp"]}
Test Fingerprint:        {res["test_fp"]}
Matched LCS Subsequence: {res["lcs_subseq"]}
LCS Length:              {res["lcs_len"]} / {len(res["ref_fp"])}
--------------------------------------------------------------------------------
Similarity Percentage:   {pct:.2f} %
Classification:          {res["sim_result"]["classification"]}
Similarity Level:        {res["explanation"]["level"]}
Execution Time:          {res["elapsed_ms"]:.2f} ms
--------------------------------------------------------------------------------
Explanation:
{res["explanation"]["explanation"]}

Recommendation:
{res["explanation"]["recommendation"]}
================================================================================
Generated by SignaMatch LCS Signature Engine.
"""
        st.download_button(
            label="📥 Download Detailed Forensic Report (.txt)",
            data=report_text,
            file_name=f"SignaMatch_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

    with tab_diff:
        st.markdown("#### Pixel-by-Pixel Differential Analysis")
        st.caption("Aligns both signatures and isolates pixel variations (> 20 intensity delta).")
        
        d_col1, d_col2, d_col3 = st.columns(3)
        with d_col1:
            st.image(st.session_state.reference_image, caption="Reference", use_container_width=True)
        with d_col2:
            st.image(st.session_state.test_image, caption="Test", use_container_width=True)
        diff_display = res["diff_img"]
        if isinstance(diff_display, str):
            diff_display = Image.open(diff_display)

        with d_col3:
            st.image(diff_display, caption="Visual Difference (White = Discrepancies)", use_container_width=True)

        buf = io.BytesIO()
        diff_display.save(buf, format="PNG")
        st.download_button(
            label="📥 Download Difference Map Image (.png)",
            data=buf.getvalue(),
            file_name="signature_difference.png",
            mime="image/png"
        )

    with tab_pipeline:
        st.markdown("#### Feature Extraction Pipeline Walkthrough")
        st.caption("Inspect the mathematical transformation stages from raw strokes to normalized matrices:")

        p1, p2, p3, p4 = st.columns(4)
        with p1:
            st.image(res["ref_prep"]["grayscale"], caption="1. Grayscale & Alpha Flattening", use_container_width=True)
        with p2:
            st.image(res["ref_prep"]["resized"], caption="2. 64x64 Spatial Normalization", use_container_width=True)
        with p3:
            st.image(res["ref_prep"]["binary"].astype(np.uint8) * 255, caption="3. Binary Ink Mask (< 128)", use_container_width=True)
        with p4:
            st.image((res["ref_fp_data"]["compressed_matrix"] * 255).astype(np.uint8), caption="4. 16x16 Pooling Heatmap", use_container_width=True)

        st.markdown("##### Row vs Column Ink Density Distribution")
        chart_data = pd.DataFrame({
            "Block Vector": [f"B{i+1}" for i in range(16)],
            "Ref Row Density": res["ref_fp_data"]["row_density"],
            "Test Row Density": res["test_fp_data"]["row_density"],
            "Ref Col Density": res["ref_fp_data"]["column_density"],
            "Test Col Density": res["test_fp_data"]["column_density"],
        })
        st.line_chart(chart_data.set_index("Block Vector"))

    with tab_history:
        st.markdown("#### Comparison Audit Log")
        history_list = load_history()
        if history_list:
            df_hist = pd.DataFrame(history_list)
            st.dataframe(df_hist, use_container_width=True)
            
            c_h1, c_h2 = st.columns(2)
            with c_h1:
                csv_bytes = df_hist.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export History as CSV",
                    data=csv_bytes,
                    file_name="comparison_history.csv",
                    mime="text/csv"
                )
            with c_h2:
                if st.button("🗑️ Clear Audit History", type="secondary"):
                    clear_history()
                    st.rerun()
        else:
            st.info("No prior comparisons logged yet.")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94A3B8; font-size: 0.85rem;">
    <strong>SignaMatch</strong> • Handwritten Signature Verification Platform • Powered by Longest Common Subsequence (LCS) Dynamic Programming
</div>
""", unsafe_allow_html=True)
