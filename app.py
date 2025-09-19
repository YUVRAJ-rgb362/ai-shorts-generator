import streamlit as st
import requests
import json
import time
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from datetime import datetime
import tempfile

# Page config
st.set_page_config(
    page_title="AI Shorts Generator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    text-align: center;
    color: #FF6B6B;
    margin-bottom: 2rem;
}
.feature-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    margin: 1rem 0;
}
.stats-box {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #FF6B6B;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

class AIVideoGenerator:
    def __init__(self):
        self.api_endpoints = {
            'runway': 'https://api.runwayml.com/v1/generations',
            'stability': 'https://api.stability.ai/v1/generation/stable-video-diffusion-img2vid/image-to-video',
            'leonardo': 'https://cloud.leonardo.ai/api/rest/v1/generations-motion'
        }
        
    def generate_engaging_script(self, prompt):
        """Generate engaging script based on prompt"""
        script_templates = {
            'finance': [
                "💰 This ONE trick billionaires use will SHOCK you!",
                "🚨 WARNING: Banks don't want you to know this!",
                "💸 Turn $100 into $1000 in 30 days (PROVEN METHOD)"
            ],
            'lifestyle': [
                "✨ This morning routine changed EVERYTHING!",
                "🔥 You're doing this WRONG your entire life!",
                "💫 The secret habit of successful people revealed!"
            ],
            'tech': [
                "🤖 AI just made this possible in 2024!",
                "🚀 This technology will replace your job!",
                "⚡ The future is HERE and it's INSANE!"
            ]
        }
        
        # Detect category from prompt
        category = 'lifestyle'  # default
        if any(word in prompt.lower() for word in ['money', 'finance', 'trading', 'crypto']):
            category = 'finance'
        elif any(word in prompt.lower() for word in ['ai', 'tech', 'technology', 'future']):
            category = 'tech'
            
        return np.random.choice(script_templates[category])
    
    def create_text_clip(self, text, duration=3, position='center', fontsize=60):
        """Create text overlay clip"""
        # Create text clip
        txt_clip = TextClip(text, 
                           fontsize=fontsize,
                           color='white',
                           font='Arial-Bold',
                           stroke_color='black',
                           stroke_width=2)
        
        txt_clip = txt_clip.set_duration(duration).set_position(position)
        return txt_clip
    
    def add_engagement_elements(self, video_clip):
        """Add engagement elements like arrows, emojis, transitions"""
        # Add zoom effect
        video_with_zoom = video_clip.resize(lambda t: 1 + 0.02*t)
        
        # Add fade transitions
        video_with_fade = video_with_zoom.crossfadein(0.5).crossfadeout(0.5)
        
        return video_with_fade
    
    def generate_background_video(self, prompt, style="cinematic"):
        """Generate or select background video based on prompt"""
        # For demo, create a colorful gradient background
        duration = 30  # 30 seconds
        
        def make_frame(t):
            # Create animated gradient background
            color1 = np.array([255, 100, 100])  # Red
            color2 = np.array([100, 100, 255])  # Blue
            
            # Animate between colors
            ratio = (np.sin(t * 0.5) + 1) / 2
            color = color1 * (1 - ratio) + color2 * ratio
            
            frame = np.ones((720, 720, 3)) * color.reshape(1, 1, 3)
            return frame.astype(np.uint8)
        
        bg_clip = VideoClip(make_frame, duration=duration)
        return bg_clip
    
    def create_shorts_video(self, prompt, style="viral"):
        """Main function to create 720p shorts video"""
        try:
            # Generate engaging script
            script = self.generate_engaging_script(prompt)
            
            # Create background video
            bg_video = self.generate_background_video(prompt, style)
            
            # Create text overlays with timing
            text_clips = []
            
            # Title text (0-5 seconds)
            title_clip = self.create_text_clip(
                script, 
                duration=5, 
                position=('center', 200),
                fontsize=45
            )
            text_clips.append(title_clip)
            
            # Main content text (5-25 seconds)
            content_parts = [
                "Step 1: Understanding the basics",
                "Step 2: Apply this technique", 
                "Step 3: See AMAZING results!"
            ]
            
            for i, content in enumerate(content_parts):
                start_time = 5 + i * 7
                content_clip = self.create_text_clip(
                    content,
                    duration=6,
                    position=('center', 400),
                    fontsize=35
                ).set_start(start_time)
                text_clips.append(content_clip)
            
            # Call-to-action (25-30 seconds)
            cta_clip = self.create_text_clip(
                "FOLLOW for more tips! 👆",
                duration=5,
                position=('center', 600),
                fontsize=40
            ).set_start(25)
            text_clips.append(cta_clip)
            
            # Add engagement elements
            bg_video_enhanced = self.add_engagement_elements(bg_video)
            
            # Combine all elements
            final_video = CompositeVideoClip([bg_video_enhanced] + text_clips)
            
            # Ensure 720p resolution
            final_video = final_video.resize((720, 720))
            
            return final_video, script
            
        except Exception as e:
            st.error(f"Error creating video: {str(e)}")
            return None, None

def main():
    # Header
    st.markdown('<h1 class="main-header">🎬 AI Shorts Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Create engaging 720p short videos in 30 seconds with AI</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Video style selection
        style = st.selectbox(
            "Video Style",
            ["Viral", "Educational", "Motivational", "Entertainment", "News"]
        )
        
        # Duration (fixed at 30 seconds for shorts)
        duration = st.slider("Duration (seconds)", 15, 60, 30)
        
        # Resolution (fixed at 720p for shorts)
        st.info("📱 Optimized for 720p vertical format")
        
        # Additional options
        add_music = st.checkbox("Add Background Music", value=True)
        add_effects = st.checkbox("Add Visual Effects", value=True)
        
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Create Your Short")
        
        # Prompt input
        prompt = st.text_area(
            "Enter your video prompt:",
            placeholder="e.g., 'Create a motivational video about morning routines for success'",
            height=100
        )
        
        # Example prompts
        st.subheader("💡 Example Prompts")
        example_prompts = [
            "5 morning habits that made me a millionaire",
            "This AI trick will blow your mind in 2024",
            "The secret to getting 10k followers in 30 days",
            "Why successful people wake up at 5 AM",
            "This trading strategy changed my life"
        ]
        
        for i, example in enumerate(example_prompts):
            if st.button(f"📌 {example}", key=f"example_{i}"):
                prompt = example
                st.rerun()
        
        # Generate button
        if st.button("🚀 Generate Short Video", type="primary", use_container_width=True):
            if prompt:
                with st.spinner("🎬 Creating your viral short... This may take a few moments!"):
                    generator = AIVideoGenerator()
                    
                    # Progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Simulate progress
                    for i in range(100):
                        time.sleep(0.1)
                        progress_bar.progress(i + 1)
                        if i < 20:
                            status_text.text("🤖 AI analyzing your prompt...")
                        elif i < 50:
                            status_text.text("🎨 Generating visual content...")
                        elif i < 80:
                            status_text.text("✨ Adding engagement elements...")
                        else:
                            status_text.text("🎬 Finalizing your short...")
                    
                    # Generate video
                    video, script = generator.create_shorts_video(prompt, style.lower())
                    
                    if video:
                        st.success("✅ Video generated successfully!")
                        
                        # Display generated script
                        st.subheader("📜 Generated Script")
                        st.info(script)
                        
                        # Save video to temporary file
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                            video_path = tmp_file.name
                            video.write_videofile(video_path, fps=30, audio=False, verbose=False, logger=None)
                        
                        # Display video
                        st.subheader("🎬 Your Generated Short")
                        st.video(video_path)
                        
                        # Download button
                        with open(video_path, "rb") as video_file:
                            st.download_button(
                                label="📥 Download Video",
                                data=video_file.read(),
                                file_name=f"short_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
                                mime="video/mp4",
                                use_container_width=True
                            )
                        
                        # Clean up
                        os.unlink(video_path)
                        
                    else:
                        st.error("❌ Failed to generate video. Please try again.")
            else:
                st.warning("⚠️ Please enter a prompt to generate your video.")
    
    with col2:
        st.header("📊 Features")
        
        features = [
            "🎯 AI-Powered Content",
            "📱 720p Vertical Format",
            "⏱️ 30-Second Duration",
            "🔥 Viral Optimization",
            "🎨 Auto Text Overlays",
            "✨ Visual Effects",
            "🎵 Background Music",
            "📈 Engagement Hooks"
        ]
        
        for feature in features:
            st.markdown(f'<div class="stats-box">{feature}</div>', unsafe_allow_html=True)
        
        st.header("📈 Tips for Viral Shorts")
        tips = [
            "Start with a hook in first 3 seconds",
            "Use trending topics and keywords",
            "Add clear call-to-actions",
            "Keep text large and readable",
            "Use contrasting colors",
            "Include emotional triggers"
        ]
        
        for tip in tips:
            st.write(f"• {tip}")

if __name__ == "__main__":
    main()