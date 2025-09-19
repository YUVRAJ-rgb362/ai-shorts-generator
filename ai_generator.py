import requests
import json
import base64
import io
import os
from PIL import Image
import numpy as np
from moviepy.editor import *
import tempfile
from typing import Dict, List, Optional, Tuple
import time
from datetime import datetime

class AIVideoEngine:
    """Advanced AI-powered video generation engine"""
    
    def __init__(self):
        self.api_keys = {
            'openai': os.getenv('OPENAI_API_KEY', ''),
            'runway': os.getenv('RUNWAY_API_KEY', ''),
            'stability': os.getenv('STABILITY_API_KEY', ''),
            'replicate': os.getenv('REPLICATE_API_TOKEN', ''),
            'leonardo': os.getenv('LEONARDO_API_KEY', '')
        }
        
        self.viral_hooks = {
            'finance': [
                "This ONE secret made me $10k in 30 days",
                "Banks HATE this simple trick",
                "Turn $100 into $1000 (Step by step)",
                "I discovered this at 3 AM and it changed everything",
                "Nobody talks about this money strategy"
            ],
            'lifestyle': [
                "I did this for 30 days and here's what happened",
                "This morning habit changed my entire life",
                "You've been doing this WRONG your whole life",
                "The 1% secret that nobody teaches you",
                "This will be trending everywhere in 2024"
            ],
            'tech': [
                "This AI can do ANYTHING in seconds",
                "Technology that will replace 90% of jobs",
                "This app made me $500/day on autopilot",
                "AI just solved humanity's biggest problem",
                "This tech breakthrough will shock you"
            ],
            'motivation': [
                "From broke to millionaire in 2 years",
                "This mindset shift changed everything",
                "What successful people do at 5 AM",
                "The psychology trick that gets you anything",
                "Why 99% of people never succeed"
            ]
        }
        
        self.engagement_patterns = {
            'retention': [
                "Wait until you see what happens next...",
                "But here's where it gets interesting...",
                "The shocking truth is...",
                "This will blow your mind...",
                "You won't believe what happened..."
            ],
            'cta': [
                "Follow for more secrets like this!",
                "Save this before it gets taken down!",
                "Share this with someone who needs it!",
                "Comment 'YES' if you want part 2!",
                "Double tap if this helped you!"
            ]
        }
    
    def analyze_prompt_category(self, prompt: str) -> str:
        """Intelligently categorize prompt for optimal content generation"""
        prompt_lower = prompt.lower()
        
        finance_keywords = ['money', 'trading', 'crypto', 'investment', 'profit', 'business', 'income']
        tech_keywords = ['ai', 'technology', 'app', 'software', 'digital', 'online', 'automation']
        lifestyle_keywords = ['habit', 'routine', 'health', 'fitness', 'productivity', 'success']
        motivation_keywords = ['motivation', 'inspire', 'mindset', 'goal', 'achieve', 'dream']
        
        scores = {
            'finance': sum(1 for word in finance_keywords if word in prompt_lower),
            'tech': sum(1 for word in tech_keywords if word in prompt_lower),
            'lifestyle': sum(1 for word in lifestyle_keywords if word in prompt_lower),
            'motivation': sum(1 for word in motivation_keywords if word in prompt_lower)
        }
        
        return max(scores, key=scores.get) if max(scores.values()) > 0 else 'lifestyle'
    
    def generate_viral_script(self, prompt: str, category: str = None) -> Dict[str, any]:
        """Generate viral script structure optimized for engagement"""
        if not category:
            category = self.analyze_prompt_category(prompt)
        
        hook = np.random.choice(self.viral_hooks.get(category, self.viral_hooks['lifestyle']))
        retention = np.random.choice(self.engagement_patterns['retention'])
        cta = np.random.choice(self.engagement_patterns['cta'])
        
        # Generate content structure
        script_structure = {
            'hook': hook,
            'opening': f"In today's video, I'll show you {prompt.lower()}",
            'main_points': [
                f"First, understand this key principle...",
                f"Next, apply this proven method...",
                f"Finally, see these incredible results..."
            ],
            'retention_hook': retention,
            'call_to_action': cta,
            'category': category,
            'estimated_engagement': self.calculate_engagement_score(hook, category)
        }
        
        return script_structure
    
    def calculate_engagement_score(self, hook: str, category: str) -> float:
        """Calculate predicted engagement score based on content analysis"""
        engagement_words = ['secret', 'shock', 'amazing', 'incredible', 'proven', 'guaranteed']
        emotional_words = ['hate', 'love', 'obsessed', 'crazy', 'insane', 'unbelievable']
        urgency_words = ['now', 'today', 'limited', 'before', 'urgent', 'immediate']
        
        score = 0.5  # Base score
        
        hook_lower = hook.lower()
        
        # Add points for engagement words
        score += sum(0.1 for word in engagement_words if word in hook_lower)
        score += sum(0.15 for word in emotional_words if word in hook_lower)
        score += sum(0.05 for word in urgency_words if word in hook_lower)
        
        # Category multipliers
        multipliers = {
            'finance': 1.2,
            'tech': 1.1,
            'lifestyle': 1.0,
            'motivation': 1.15
        }
        
        score *= multipliers.get(category, 1.0)
        
        return min(score, 1.0)  # Cap at 1.0
    
    def create_dynamic_background(self, category: str, duration: int = 30) -> VideoClip:
        """Create dynamic animated background based on category"""
        
        color_schemes = {
            'finance': [(34, 139, 34), (0, 100, 0), (50, 205, 50)],  # Green money theme
            'tech': [(0, 191, 255), (138, 43, 226), (75, 0, 130)],   # Blue/purple tech theme
            'lifestyle': [(255, 182, 193), (255, 160, 122), (255, 105, 180)], # Warm lifestyle
            'motivation': [(255, 69, 0), (255, 140, 0), (255, 215, 0)]  # Orange/gold energy
        }
        
        colors = color_schemes.get(category, color_schemes['lifestyle'])
        
        def make_dynamic_frame(t):
            # Create animated gradient with movement
            progress = (t / duration) % 1
            
            # Oscillating color blend
            color_index = int((progress * len(colors)) % len(colors))
            next_color_index = (color_index + 1) % len(colors)
            
            blend_ratio = (progress * len(colors)) % 1
            
            color1 = np.array(colors[color_index])
            color2 = np.array(colors[next_color_index])
            
            base_color = color1 * (1 - blend_ratio) + color2 * blend_ratio
            
            # Create dynamic patterns
            height, width = 720, 720
            y, x = np.ogrid[:height, :width]
            
            # Moving wave pattern
            wave = np.sin((x + y + t * 50) * 0.02) * 0.3 + 0.7
            
            # Apply wave to color channels
            frame = np.zeros((height, width, 3))
            for i in range(3):
                frame[:, :, i] = base_color[i] * wave
            
            # Add subtle noise for texture
            noise = np.random.random((height, width, 1)) * 20 - 10
            frame += noise
            
            return np.clip(frame, 0, 255).astype(np.uint8)
        
        return VideoClip(make_dynamic_frame, duration=duration)
    
    def create_text_with_effects(self, text: str, start_time: float, duration: float, 
                               position: tuple = ('center', 'center'), style: str = 'title') -> TextClip:
        """Create text with advanced effects and animations"""
        
        styles = {
            'title': {
                'fontsize': 50,
                'color': 'white',
                'font': 'Arial-Bold',
                'stroke_color': 'black',
                'stroke_width': 3
            },
            'subtitle': {
                'fontsize': 35,
                'color': 'yellow',
                'font': 'Arial',
                'stroke_color': 'black',
                'stroke_width': 2
            },
            'content': {
                'fontsize': 40,
                'color': 'white',
                'font': 'Arial-Bold',
                'stroke_color': 'red',
                'stroke_width': 2
            },
            'cta': {
                'fontsize': 45,
                'color': 'lime',
                'font': 'Arial-Bold',
                'stroke_color': 'black',
                'stroke_width': 3
            }
        }
        
        style_config = styles.get(style, styles['content'])
        
        # Create text clip
        txt_clip = TextClip(text, **style_config)
        
        # Add entrance animation (scale up)
        txt_clip = txt_clip.set_duration(duration).set_position(position)
        txt_clip = txt_clip.set_start(start_time)
        
        # Add scale animation for emphasis
        if style in ['title', 'cta']:
            txt_clip = txt_clip.resize(lambda t: 1 + 0.1 * np.sin(t * 4))
        
        return txt_clip
    
    def add_viral_elements(self, video_clip: VideoClip) -> VideoClip:
        """Add viral elements like zoom, transitions, and effects"""
        # Add subtle zoom for retention
        zoomed = video_clip.resize(lambda t: 1 + 0.05 * np.sin(t * 0.5))
        
        # Add fade transitions
        with_transitions = zoomed.crossfadein(1.0).crossfadeout(1.0)
        
        # Add slight rotation for dynamic feel
        dynamic = with_transitions.rotate(lambda t: 2 * np.sin(t * 0.3))
        
        return dynamic
    
    def create_shorts_masterpiece(self, prompt: str, style: str = "viral") -> Tuple[VideoClip, Dict]:
        """Create a complete 30-second viral shorts video"""
        
        try:
            # Generate script and analyze
            category = self.analyze_prompt_category(prompt)
            script_data = self.generate_viral_script(prompt, category)
            
            # Create dynamic background (30 seconds)
            bg_video = self.create_dynamic_background(category, 30)
            
            # Create text elements with perfect timing
            text_clips = []
            
            # Hook (0-3 seconds)
            hook_clip = self.create_text_with_effects(
                script_data['hook'],
                start_time=0,
                duration=3,
                position=('center', 150),
                style='title'
            )
            text_clips.append(hook_clip)
            
            # Opening (3-6 seconds)
            opening_clip = self.create_text_with_effects(
                script_data['opening'],
                start_time=3,
                duration=3,
                position=('center', 350),
                style='subtitle'
            )
            text_clips.append(opening_clip)
            
            # Main content points (6-24 seconds)
            for i, point in enumerate(script_data['main_points']):
                start_time = 6 + i * 6
                point_clip = self.create_text_with_effects(
                    point,
                    start_time=start_time,
                    duration=5,
                    position=('center', 400 + i * 50),
                    style='content'
                )
                text_clips.append(point_clip)
            
            # Retention hook (24-27 seconds)
            retention_clip = self.create_text_with_effects(
                script_data['retention_hook'],
                start_time=24,
                duration=3,
                position=('center', 200),
                style='subtitle'
            )
            text_clips.append(retention_clip)
            
            # Call to action (27-30 seconds)
            cta_clip = self.create_text_with_effects(
                script_data['call_to_action'],
                start_time=27,
                duration=3,
                position=('center', 600),
                style='cta'
            )
            text_clips.append(cta_clip)
            
            # Add viral effects to background
            enhanced_bg = self.add_viral_elements(bg_video)
            
            # Compose final video
            final_video = CompositeVideoClip([enhanced_bg] + text_clips)
            
            # Ensure perfect 720p vertical format
            final_video = final_video.resize((720, 720))
            
            # Add metadata
            metadata = {
                'script': script_data,
                'category': category,
                'duration': 30,
                'resolution': '720x720',
                'engagement_score': script_data['estimated_engagement'],
                'created_at': datetime.now().isoformat(),
                'optimization': 'viral_shorts'
            }
            
            return final_video, metadata
            
        except Exception as e:
            print(f"Error in video creation: {str(e)}")
            return None, None
    
    def optimize_for_platform(self, video: VideoClip, platform: str) -> VideoClip:
        """Optimize video for specific social media platforms"""
        
        platform_specs = {
            'instagram': {'size': (720, 720), 'fps': 30, 'duration': 30},
            'tiktok': {'size': (720, 1280), 'fps': 30, 'duration': 30},
            'youtube_shorts': {'size': (720, 1280), 'fps': 30, 'duration': 60},
            'facebook': {'size': (720, 720), 'fps': 30, 'duration': 30}
        }
        
        spec = platform_specs.get(platform, platform_specs['instagram'])
        
        # Resize and adjust
        optimized = video.resize(spec['size'])
        
        # Adjust duration if needed
        if video.duration > spec['duration']:
            optimized = optimized.subclip(0, spec['duration'])
        
        return optimized
    
    def generate_thumbnail(self, video: VideoClip, timestamp: float = 2.0) -> np.ndarray:
        """Generate an engaging thumbnail from the video"""
        # Get frame at specified timestamp
        frame = video.get_frame(timestamp)
        
        # Add thumbnail enhancements (brightness, contrast)
        enhanced = np.clip(frame * 1.2 + 20, 0, 255).astype(np.uint8)
        
        return enhanced
    
    def add_background_music(self, video: VideoClip, music_type: str = 'upbeat') -> VideoClip:
        """Add background music based on category"""
        # This would integrate with music APIs or local files
        # For now, return video as-is
        # In production, you'd add actual audio processing here
        return video

# Usage example and testing
if __name__ == "__main__":
    # Initialize the AI engine
    engine = AIVideoEngine()
    
    # Test prompt
    test_prompt = "How to make money with AI in 2024"
    
    # Generate video
    video, metadata = engine.create_shorts_masterpiece(test_prompt)
    
    if video and metadata:
        print(f"Video created successfully!")
        print(f"Category: {metadata['category']}")
        print(f"Engagement Score: {metadata['engagement_score']:.2f}")
        print(f"Script Hook: {metadata['script']['hook']}")
    else:
        print("Failed to create video")