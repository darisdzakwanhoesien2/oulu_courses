import streamlit as st
import cv2
import numpy as np
from PIL import Image

from core.imaging import apply_bokeh, apply_vignette
from core.color import white_balance
from core.segmentation import otsu_segment
from core.texture import lbp_texture
from core.geometry import detect_circles

st.set_page_config(page_title="🧠 Machine Vision Lab", layout="wide")
st.title("🧠 Machine Vision Interactive Lab")

uploaded = st.file_uploader("Upload an image", type=["jpg","png","jpeg"])

module = st.sidebar.selectbox(
    "Select Module",
    ["Original", "Bokeh", "Vignette", "White Balance",
     "Segmentation", "Texture (LBP)", "Hough Circles"]
)

if uploaded:
    image = Image.open(uploaded).convert("RGB")
    img = np.array(image)

    result = img.copy()

    if module == "Bokeh":
        k = st.sidebar.slider("Blur Kernel", 5, 51, 15, step=2)
        result = apply_bokeh(img, k)

    elif module == "Vignette":
        s = st.sidebar.slider("Strength", 0.0001, 0.01, 0.002)
        result = apply_vignette(img, s)

    elif module == "White Balance":
        result = white_balance(img)

    elif module == "Segmentation":
        mask = otsu_segment(img)
        result = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

    elif module == "Texture (LBP)":
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        lbp = lbp_texture(gray)
        result = cv2.applyColorMap(lbp, cv2.COLORMAP_JET)

    elif module == "Hough Circles":
        result = detect_circles(img)

    col1, col2 = st.columns(2)
    col1.image(img, caption="Original", use_container_width=True)
    col2.image(result, caption=module, use_container_width=True)

else:
    st.info("Upload an image to start.")