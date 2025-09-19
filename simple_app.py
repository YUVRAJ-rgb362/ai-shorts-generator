import streamlit as st
import time
import base64
from datetime import datetime
import tempfile
import os
from moviepy.editor import *
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Page configuration - Mobile friendly
st.set_page_config(
    page_title="🎬 AI Shorts Maker",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for mobile-friendly design
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* Header styling */
    .app-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .app-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .app-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 25px;
        width: 100%;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Success messages */
    .success-box {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Progress styling */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Input styling */
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        font-size: 1.1rem;
        padding: 1rem;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .app-title {
            font-size: 2rem;
        }
        .app-subtitle {
            font-size: 1rem;
        }
        .feature-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

class SimpleVideoMaker:
    def __init__(self):
        self.viral_templates = {
            'money': [
                "💰 This ONE trick made me $1000 in 24 hours!",
                "🚨 Banks don't want you to know this SECRET!",
                "💸 Turn $50 into $500 in 7 days (PROVEN!)"
            ],
            'motivation': [
                "✨ This morning routine CHANGED MY LIFE!",
                "🔥 Why 99% of people NEVER succeed!",
                "💪 The mindset that creates millionaires!"
            ],
            'tech': [
                "🤖 This AI tool will replace your job!",
                "⚡ The future is HERE and it's INSANE!",
                "🚀 This app made me $500/day automatically!"
            ],
            'lifestyle': [
                "🌟 I tried this for 30 days... SHOCKING results!",
                "😱 You've been doing this WRONG your whole life!",
                "🎯 This habit will make you UNSTOPPABLE!"
            ]
        }
    
    def detect_category(self, text):
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['money', 'cash', 'profit', 'income', 'rich', 'wealthy']):
            return 'money'
        elif any(word in text_lower for word in ['ai', 'tech', 'app', 'software', 'digital']):
            return 'tech'
        elif any(word in text_lower for word in ['motivation', 'success', 'goal', 'achieve', 'mindset']):
            return 'motivation'
        else:
            return 'lifestyle'
    
    def create_simple_video(self, user_prompt, selected_template=None):
        try:
            # Determine category and template
            category = self.detect_category(user_prompt)
            
            if selected_template:
                hook = selected_template
            else:
                hook = np.random.choice(self.viral_templates[category])
            
            # Create colorful background
            def make_gradient_frame(t):
                colors = {
                    'money': [(34, 139, 34), (0, 100, 0)],    # Green
                    'tech': [(0, 191, 255), (138, 43, 226)],   # Blue-Purple
                    'motivation': [(255, 69, 0), (255, 140, 0)], # Orange
                    'lifestyle': [(255, 182, 193), (255, 160, 122)] # Pink-Orange
                }
                
                color1, color2 = colors[category]
                
                # Smooth color transition
                ratio = (np.sin(t * 0.5) + 1) / 2
                final_color = tuple(int(c1 * (1-ratio) + c2 * ratio) for c1, c2 in zip(color1, color2))
                
                frame = np.full((720, 720, 3), final_color, dtype=np.uint8)
                return frame
            
            # Create 30-second background
            bg_clip = VideoClip(make_gradient_frame, duration=30)
            
            # Create text clips with perfect timing
            texts = [
                {"text": hook, "start": 0, "duration": 8, "size": 45, "pos": (360, 200)},
                {"text": f"Here's what you need to know about:", "start": 6, "duration": 6, "size": 35, "pos": (360, 350)},
                {"text": user_prompt, "start": 10, "duration": 8, "size": 40, "pos": (360, 450)},
                {"text": "This will CHANGE everything!", "start": 16, "duration": 6, "size": 38, "pos": (360, 300)},
                {"text": "Follow for more tips! 👆", "start": 20, "duration": 10, "size": 42, "pos": (360, 550)}
            ]
            
            text_clips = []
            for text_info in texts:
                txt_clip = TextClip(
                    text_info["text"],
                    fontsize=text_info["size"],
                    color='white',
                    font='Arial-Bold',
                    stroke_color='black',
                    stroke_width=3,
                    size=(680, None),
                    method='caption'
                ).set_duration(text_info["duration"]).set_start(text_info["start"]).set_position('center')
                
                # Add subtle animation
                txt_clip = txt_clip.resize(lambda t: 1 + 0.05 * np.sin(t * 2))
                text_clips.append(txt_clip)
            
            # Combine everything
            final_video = CompositeVideoClip([bg_clip] + text_clips)
            
            return final_video, hook, category
            
        except Exception as e:
            st.error(f"Error creating video: {str(e)}")
            return None, None, None

def main():
    # Header
    st.markdown("""
    <div class="app-header">
        <div class="app-title">🎬 AI Shorts Maker</div>
        <div class="app-subtitle">Create viral 30-second videos instantly!</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize video maker
    if 'video_maker' not in st.session_state:
        st.session_state.video_maker = SimpleVideoMaker()
    
    video_maker = st.session_state.video_maker
    
    # Simple 3-step process
    st.markdown("""
    <div class="feature-card">
        <h3>🚀 3 Simple Steps to Viral Content:</h3>
        <p><strong>Step 1:</strong> Enter your idea below</p>
        <p><strong>Step 2:</strong> Choose a viral template</p>
        <p><strong>Step 3:</strong> Click "Create My Viral Short!"</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Step 1: User input
    st.markdown("### 📝 Step 1: What's your video about?")
    user_prompt = st.text_area(
        "",
        placeholder="Example: How to make money with AI, Morning routine for success, Best trading strategy...",
        height=100,
        help="Describe what you want your video to be about. The AI will create engaging content around this topic!"
    )
    
    # Step 2: Template selection
    if user_prompt:
        category = video_maker.detect_category(user_prompt)
        st.markdown("### 🎯 Step 2: Choose your viral hook:")
        
        templates = video_maker.viral_templates[category]
        
        # Show templates as buttons
        selected_template = None
        cols = st.columns(1)
        
        for i, template in enumerate(templates):
            if st.button(f"🔥 {template}", key=f"template_{i}"):
                selected_template = template
        
        # Step 3: Generate video
        st.markdown("### 🚀 Step 3: Create your viral short!")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎬 CREATE MY VIRAL SHORT!", key="generate_main"):
                # Show loading animation
                with st.spinner("✨ Creating your viral masterpiece..."):
                    
                    # Progress bar with fun messages
                    progress_bar = st.progress(0)
                    status_messages = [
                        "🤖 AI analyzing your idea...",
                        "🎨 Designing viral graphics...",
                        "✨ Adding engagement hooks...",
                        "🔥 Optimizing for maximum views...",
                        "🎬 Finalizing your masterpiece..."
                    ]
                    
                    for i in range(100):
                        time.sleep(0.05)  # Faster progress
                        progress_bar.progress(i + 1)
                        
                        if i % 20 == 0 and i < 80:
                            st.write(status_messages[i // 20])
                    
                    # Create the video
                    video, hook, detected_category = video_maker.create_simple_video(user_prompt, selected_template)
                    
                    if video:
                        st.markdown("""
                        <div class="success-box">
                            <h2>🎉 SUCCESS! Your viral short is ready!</h2>
                            <p>Get ready to go viral! 🚀</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Video info
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("📱 Format", "720p Vertical")
                            st.metric("⏱️ Duration", "30 seconds")
                        with col2:
                            st.metric("🎯 Category", detected_category.title())
                            st.metric("🔥 Hook Used", "Custom")
                        
                        # Save and display video
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                            video_path = tmp_file.name
                            video.write_videofile(video_path, fps=30, audio=False, verbose=False, logger=None)
                        
                        # Display video
                        st.markdown("### 🎬 Your Viral Short:")
                        st.video(video_path)
                        
                        # Download section
                        st.markdown("### 📥 Download Your Video:")
                        with open(video_path, "rb") as video_file:
                            video_bytes = video_file.read()
                            
                        filename = f"viral_short_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
                        
                        st.download_button(
                            label="📱 Download for Instagram/TikTok",
                            data=video_bytes,
                            file_name=filename,
                            mime="video/mp4",
                            help="Download your video and upload to Instagram Reels, TikTok, YouTube Shorts!"
                        )
                        
                        # Social media tips
                        st.markdown("""
                        <div class="feature-card">
                            <h4>📈 Tips to Go Viral:</h4>
                            <p>✅ Post between 7-9 PM for maximum engagement</p>
                            <p>✅ Use trending hashtags in your niche</p>
                            <p>✅ Respond to comments within first hour</p>
                            <p>✅ Cross-post on all platforms (Instagram, TikTok, YouTube)</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Cleanup
                        os.unlink(video_path)
                        
                    else:
                        st.error("❌ Something went wrong. Please try again!")
    
    # Quick examples section
    if not user_prompt:
        st.markdown("### 💡 Need inspiration? Try these:")
        
        examples = [
            "How to make $1000 with AI in 2024",
            "Morning routine that changed my life",
            "Secret trading strategy that actually works",
            "This productivity hack will shock you",
            "Why successful people wake up at 5 AM"
        ]
        
        for example in examples:
            if st.button(f"💡 {example}", key=f"example_{example}"):
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <h4>🎬 Made with ❤️ for Content Creators</h4>
        <p>Create unlimited viral shorts • No watermarks • Commercial use allowed</p>
        <p><small>Built by <a href="https://github.com/YUVRAJ-rgb362" target="_blank">YUVRAJ-rgb362</a></small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()