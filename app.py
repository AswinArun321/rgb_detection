import streamlit as st
import cv2
import numpy as np
import time

# Set page config for a premium dashboard aesthetic
st.set_page_config(
    page_title="RGB Dominant Color Detector",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling cards, layout, and styling the stream container
st.markdown("""
    <style>
        .title-container {
            text-align: center;
            margin-bottom: 30px;
        }
        .desc-text {
            font-size: 1.1rem;
            color: #6b7280;
            text-align: center;
            max-width: 800px;
            margin: 0 auto 30px auto;
        }
        .card-container {
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin-bottom: 20px;
            background-color: #1f2937;
            color: white;
        }
        .metric-title {
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            opacity: 0.8;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 2.2rem;
            font-weight: 700;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="title-container">
        <h1>🎨 RGB Dominant Color Detector</h1>
        <p class="desc-text">
            A real-time image analysis app that processes frames, computes color channel averages, and dynamically detects the dominant color (Red, Green, or Blue).
        </p>
    </div>
""", unsafe_allow_html=True)

# Helper function to analyze color channels and render metrics dashboard
def analyze_and_display(frame_rgb, frame_placeholder, dominant_color_placeholder, metrics_placeholder):
    # Show the image feed in Streamlit
    frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
    
    # Slice channels and compute mean values
    # frame_rgb shape: (height, width, channels). Index 0 = Red, 1 = Green, 2 = Blue.
    r = frame_rgb[:, :, 0]
    g = frame_rgb[:, :, 1]
    b = frame_rgb[:, :, 2]
    
    r_mean = float(np.mean(r))
    g_mean = float(np.mean(g))
    b_mean = float(np.mean(b))
    
    # Determine dominant color and styling
    if b_mean > g_mean and b_mean > r_mean:
        dominant_color = "Blue"
        bg_color = "#2563eb"  # Vibrant blue
        text_color = "#ffffff"
    elif g_mean > r_mean and g_mean > b_mean:
        dominant_color = "Green"
        bg_color = "#16a34a"  # Vibrant green
        text_color = "#ffffff"
    else:
        dominant_color = "Red"
        bg_color = "#dc2626"  # Vibrant red
        text_color = "#ffffff"
    
    # Display dominant color card
    dominant_color_placeholder.markdown(
        f"""
        <div class="card-container" style="background-color: {bg_color}; color: {text_color}; text-align: center;">
            <div class="metric-title" style="font-size: 1rem; opacity: 0.9;">Dominant Color Channel</div>
            <div style="font-size: 3.5rem; font-weight: 800; margin: 15px 0;">{dominant_color}</div>
            <div style="font-size: 0.9rem; opacity: 0.85;">Based on the highest mean channel intensity</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display individual channel intensity metrics
    metrics_placeholder.markdown(
        f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top: 20px;">
            <div class="card-container" style="border-top: 5px solid #dc2626; text-align: center;">
                <div class="metric-title" style="color: #ef4444;">Red Mean</div>
                <div class="metric-value" style="color: #ef4444;">{r_mean:.1f}</div>
            </div>
            <div class="card-container" style="border-top: 5px solid #16a34a; text-align: center;">
                <div class="metric-title" style="color: #22c55e;">Green Mean</div>
                <div class="metric-value" style="color: #22c55e;">{g_mean:.1f}</div>
            </div>
            <div class="card-container" style="border-top: 5px solid #2563eb; text-align: center;">
                <div class="metric-title" style="color: #3b82f6;">Blue Mean</div>
                <div class="metric-value" style="color: #3b82f6;">{b_mean:.1f}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Sidebar controls
st.sidebar.header("Configuration")
input_method = st.sidebar.radio(
    "Choose Input Method",
    [
        "📸 Take a Photo (Cloud & Local)", 
        "📁 Upload an Image",
        "📹 Live Webcam (Local Only)"
    ]
)

# Placeholders for layouts
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.subheader("Input Stream")
    frame_placeholder = st.empty()

with col2:
    st.subheader("Color Analysis Dashboard")
    dominant_color_placeholder = st.empty()
    metrics_placeholder = st.empty()

# Initialize default empty layout styling
def show_idle_dashboard(message):
    dominant_color_placeholder.markdown(
        f"""
        <div class="card-container" style="background-color: #f3f4f6; border: 2px dashed #d1d5db; color: #4b5563; text-align: center;">
            <div style="font-size: 1.5rem; font-weight: 600; margin-bottom: 8px;">Waiting for Input...</div>
            <div style="font-size: 0.95rem;">{message}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

if input_method == "📹 Live Webcam (Local Only)":
    st.sidebar.markdown("---")
    run_camera = st.sidebar.toggle("📹 Start Camera Feed", value=False)
    
    if run_camera:
        vid = cv2.VideoCapture(0)
        
        if not vid.isOpened():
            st.error("❌ Could not access local webcam. If you are running this app on Streamlit Cloud, local webcam access via OpenCV is not possible. Please use the 'Take a Photo' or 'Upload an Image' options.")
            show_idle_dashboard("Unable to open device webcam")
        else:
            try:
                while run_camera:
                    ret, frame = vid.read()
                    
                    if not ret:
                        st.warning("⚠️ Failed to capture frame. Checking camera connection...")
                        time.sleep(1)
                        continue
                    
                    # Convert BGR (OpenCV) to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    analyze_and_display(frame_rgb, frame_placeholder, dominant_color_placeholder, metrics_placeholder)
                    time.sleep(0.01)
            except Exception as e:
                st.error(f"An unexpected error occurred during streaming: {e}")
            finally:
                vid.release()
    else:
        frame_placeholder.info("📹 Camera is stopped. Toggle 'Start Camera Feed' to begin streaming.")
        show_idle_dashboard("Toggle the camera feed to start the real-time analyzer.")

elif input_method == "📸 Take a Photo (Cloud & Local)":
    frame_placeholder.empty()
    img_file = frame_placeholder.camera_input("Capture an image to analyze")
    
    if img_file is not None:
        # Read image file bytes as OpenCV matrix
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        frame_bgr = cv2.imdecode(file_bytes, 1)
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        
        # Analyze and update dashboard (without rendering st.image in place of the camera widget)
        analyze_and_display(frame_rgb, st.empty(), dominant_color_placeholder, metrics_placeholder)
    else:
        show_idle_dashboard("Please capture a photo using your webcam to begin analysis.")

elif input_method == "📁 Upload an Image":
    uploaded_file = frame_placeholder.file_uploader("Upload an image file (JPG/JPEG/PNG)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        frame_bgr = cv2.imdecode(file_bytes, 1)
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        
        # Display the uploaded image and perform the color channel analysis
        img_display_placeholder = st.empty()
        analyze_and_display(frame_rgb, img_display_placeholder, dominant_color_placeholder, metrics_placeholder)
    else:
        show_idle_dashboard("Upload an image file to begin analysis.")