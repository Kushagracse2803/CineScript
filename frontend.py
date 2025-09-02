import streamlit as st
from generate_video import generate_video_from_prompt
import os
import time

# Access the API key securely from Streamlit secrets
GEMINI_KEY = st.secrets["GEMINI_KEY"]

# Inject the key into environment variables if your generate_video depends on it
os.environ["GEMINI_KEY"] = GEMINI_KEY


# Set page configuration
st.set_page_config(
    page_title="Gemini Video Generator",
    layout="wide"
)

# Custom CSS for styling the left-side panel
st.markdown("""
    <style>
        .prompt-panel {
            background: #23232a;
            border-radius: 16px;
            padding: 2.5rem 2rem 2rem 2rem;
            margin-bottom: 2rem;
            color: #FFF;
            box-shadow: 0 4px 32px 0 #00000030;
        }
        .stButton > button {
            border-radius: 12px;
            font-size: 1.1rem;
            padding: 0.6rem 1.7rem;
            margin-top: 1.2rem;
            background: #feae34;
            color: #23232a;
            font-weight: bold;
            border: none;
            box-shadow: 0 2px 8px 0 #0002;
        }
    </style>
""", unsafe_allow_html=True)


def get_latest_video():
    try:
        videos = [f for f in os.listdir("Videos") if f.endswith(".mp4")]
        if videos:
            videos.sort(key=lambda x: os.path.getmtime(os.path.join("Videos", x)), reverse=True)
            return os.path.join("Videos", videos[0])
    except Exception:
        return None
    return None


col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="prompt-panel">', unsafe_allow_html=True)
    st.markdown("#### Enter Prompt:")
    prompt = st.text_input(
        "Enter your video prompt:",
        key="video_prompt",
        placeholder="Visualize a futuristic city at sunset",
        label_visibility="collapsed"
    )
    generate = st.button("Generate Video")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("### Preview")
    video_path = get_latest_video()
    if video_path:
        st.video(video_path)
        st.caption(f"Latest: {os.path.basename(video_path)}")
    else:
        st.info("No videos found. Generate your first visual!")

if generate:
    if not prompt.strip():
        st.error("Please enter a prompt.")
    else:
        with st.spinner("Generating video, please wait..."):
            try:
                generate_video_from_prompt(prompt)
                st.success("Video generated! Preview updated.")
                
                # Small delay to ensure video file is saved
                time.sleep(3)
                
                # Force Streamlit to reload and show the latest video
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
