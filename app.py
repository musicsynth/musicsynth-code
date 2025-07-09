import streamlit as st
from file_processor import FileProcessor
import os
import time
from datetime import datetime
import pandas as pd
from auth import require_auth, render_user_menu
from config import validate_config
from theme_manager import apply_modern_theme, theme_manager

# Validate configuration first
try:
    validate_config()
except ValueError as e:
    st.error(f"Configuration Error: {e}")
    st.info("Please create a .env file in your project root with the required environment variables. Check config.py for details.")
    st.stop()

# Set page config
st.set_page_config(
    page_title="MusicSynth - Transform Sheet Music into Visual Magic",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply MusicSynth theme
apply_modern_theme()

# Check authentication first
if not require_auth():
    st.stop()

# Render user menu in sidebar
render_user_menu()

# Initialize session state for file processor if it doesn't exist
if 'file_processor' not in st.session_state:
    st.session_state.file_processor = FileProcessor()

# MusicSynth header with official branding
st.markdown("""
<div class="main-header musicsynth-fade-in">
    <h1>🎵 MusicSynth</h1>
    <p>Transform Sheet Music into Visual Magic</p>
    <p class="musicsynth-tagline">Experience the future of music learning</p>
</div>
""", unsafe_allow_html=True)

# Features showcase
st.markdown("""
<div class="feature-grid">
    <div class="feature-item musicsynth-fade-in">
        <div class="feature-icon">🎼</div>
        <div class="feature-title">Optical Music Recognition</div>
        <div class="feature-description">Upload sheet music images and watch them transform into digital scores</div>
    </div>
    <div class="feature-item musicsynth-fade-in">
        <div class="feature-icon">🎹</div>
        <div class="feature-title">Visual Piano Roll</div>
        <div class="feature-description">See your music come alive with stunning piano roll animations</div>
    </div>
    <div class="feature-item musicsynth-fade-in">
        <div class="feature-icon">🎨</div>
        <div class="feature-title">Music Visualization</div>
        <div class="feature-description">Create beautiful visual representations of your musical compositions</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Environment info with MusicSynth styling
is_cloud = os.environ.get('STREAMLIT_SERVER_ENVIRONMENT') == 'cloud'
if is_cloud:
    st.markdown("""
    <div class="musicsynth-card" style="background-color: var(--card); border: 1px solid var(--destructive);">
        <h3 style="margin: 0 0 0.5rem 0; color: var(--destructive); font-weight: 600;">☁️ Cloud Environment</h3>
        <p style="margin: 0; color: var(--muted-foreground);">
            Running in cloud mode. Image processing is not available. Please upload MusicXML files for the best experience.
        </p>
    </div>
    """, unsafe_allow_html=True)

# File upload section with MusicSynth styling
st.markdown("""
<div class="musicsynth-card">
    <h3 style="margin: 0 0 0.75rem 0; color: var(--foreground);">📁 Upload Your Music</h3>
    <p style="margin: 0; color: var(--muted-foreground);">
        Choose a MusicXML file or upload a sheet music image to begin the transformation
    </p>
</div>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader(
    "Choose your file",
    type=['musicxml', 'xml', 'png', 'jpg', 'jpeg'] if not is_cloud else ['musicxml', 'xml'],
    help="Upload MusicXML files (.musicxml, .xml) or sheet music images (.png, .jpg, .jpeg)"
)

if uploaded_file is not None:
    # Initialize timing statistics
    timing_stats = {
        'start_time': time.time(),
        'steps': {}
    }
    
    # MusicSynth processing section
    st.markdown("""
    <div class="musicsynth-card">
        <h3 style="margin: 0 0 0.5rem 0; color: var(--foreground);">⚙️ Creating Magic</h3>
        <p style="margin: 0; color: var(--muted-foreground);">Converting your music into a stunning visual experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Process the uploaded file
    with st.spinner("🎼 Creating your musical visualization..."):
        # Track file processing time
        process_start = time.time()
        success, message, output_path = st.session_state.file_processor.process_uploaded_file(uploaded_file)
        timing_stats['steps']['file_processing'] = time.time() - process_start
        
        if success:
            st.success(f"✨ {message}")
            
            # Track video generation time
            video_start = time.time()
            
            # MusicSynth video display section
            st.markdown("""
            <div class="musicsynth-card">
                <h3 style="margin: 0 0 0.75rem 0; color: var(--foreground);">🎥 Your Musical Magic</h3>
                <p style="margin: 0; color: var(--muted-foreground);">Your sheet music has been transformed into a beautiful visual piano roll animation</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Try to display the video
            try:
                with open(output_path, 'rb') as video_file:
                    video_bytes = video_file.read()
                    st.video(video_bytes)
            except Exception as e:
                st.warning("Video preview is not available. You can download the video file instead.")
            
            # MusicSynth download section
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                with open(output_path, 'rb') as video_file:
                    video_bytes = video_file.read()
                    st.download_button(
                        label="⬇️ Download Your Creation",
                        data=video_bytes,
                        file_name=os.path.basename(output_path),
                        mime="video/mp4",
                        use_container_width=True,
                        type="primary"
                    )
            
            timing_stats['steps']['video_generation'] = time.time() - video_start
            
            # Calculate total time
            timing_stats['total_time'] = time.time() - timing_stats['start_time']
            
            # MusicSynth statistics section
            st.markdown("""
            <div class="musicsynth-card">
                <h3 style="margin: 0 0 1rem 0; color: var(--foreground);">📊 Processing Performance</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Create MusicSynth stats display
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="stats-card">
                    <div class="stats-number">{:.2f}s</div>
                    <div class="stats-label">Music Processing</div>
                </div>
                """.format(timing_stats['steps']['file_processing']), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="stats-card">
                    <div class="stats-number">{:.2f}s</div>
                    <div class="stats-label">Visual Generation</div>
                </div>
                """.format(timing_stats['steps']['video_generation']), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="stats-card">
                    <div class="stats-number">{:.2f}s</div>
                    <div class="stats-label">Total Magic Time</div>
                </div>
                """.format(timing_stats['total_time']), unsafe_allow_html=True)
            
            # Detailed statistics table
            with st.expander("📈 Detailed Performance Metrics"):
                stats_df = pd.DataFrame({
                    'Step': list(timing_stats['steps'].keys()),
                    'Time (seconds)': [f"{t:.2f}" for t in timing_stats['steps'].values()]
                })
                stats_df.loc[len(stats_df)] = ['Total Time', f"{timing_stats['total_time']:.2f}"]
                st.table(stats_df)
            
            # Save timing statistics to a log file
            log_entry = f"\n{datetime.now()}\n"
            log_entry += f"File: {uploaded_file.name}\n"
            for step, duration in timing_stats['steps'].items():
                log_entry += f"{step}: {duration:.2f} seconds\n"
            log_entry += f"Total Time: {timing_stats['total_time']:.2f} seconds\n"
            log_entry += "-" * 50
            
            log_path = os.path.join(st.session_state.file_processor.temp_dir, 'processing_stats.log')
            with open(log_path, 'a') as f:
                f.write(log_entry)
        else:
            st.error(f"❌ {message}")

# MusicSynth cleanup section
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🧹 Clean Up Files", use_container_width=True, type="secondary"):
        st.session_state.file_processor.cleanup()
        st.success("✨ Files cleaned up successfully!")

# MusicSynth about section
st.markdown("---")
st.markdown("""
<div class="musicsynth-card">
    <h3 style="margin: 0 0 1rem 0; color: var(--foreground);">🎼 About MusicSynth</h3>
    <p style="margin: 0 0 1rem 0; color: var(--foreground);">
        MusicSynth revolutionizes music education by transforming traditional sheet music into engaging visual experiences. 
        Built with passion by a high school student who believes in making music learning more accessible and exciting for everyone.
    </p>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.25rem; margin-top: 1.25rem;">
        <div>
            <h4 style="margin: 0 0 0.5rem 0; color: var(--foreground); font-size: 1rem;">🎹 Desktop Features</h4>
            <ul style="margin: 0; padding-left: 1.25rem; color: var(--muted-foreground); font-size: 0.875rem;">
                <li>Optical Music Recognition</li>
                <li>Sheet music image processing</li>
                <li>Advanced visualization options</li>
                <li>High-quality video export</li>
            </ul>
        </div>
        <div>
            <h4 style="margin: 0 0 0.5rem 0; color: var(--foreground); font-size: 1rem;">☁️ Cloud Features</h4>
            <ul style="margin: 0; padding-left: 1.25rem; color: var(--muted-foreground); font-size: 0.875rem;">
                <li>MusicXML processing</li>
                <li>Secure user authentication</li>
                <li>Cross-platform accessibility</li>
                <li>Real-time collaboration ready</li>
            </ul>
        </div>
        <div>
            <h4 style="margin: 0 0 0.5rem 0; color: var(--foreground); font-size: 1rem;">🎨 Visual Magic</h4>
            <ul style="margin: 0; padding-left: 1.25rem; color: var(--muted-foreground); font-size: 0.875rem;">
                <li>Piano roll animations</li>
                <li>Beautiful color schemes</li>
                <li>Smooth visual transitions</li>
                <li>Educational focus</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Developer note
st.markdown("""
<div class="developer-note">
    <h4>Built with Passion ❤️</h4>
    <p>Created by a passionate high school student dedicated to revolutionizing music education through technology</p>
</div>
""", unsafe_allow_html=True)

# MusicSynth sidebar information
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="musicsynth-card">
    <h3 style="margin: 0 0 0.5rem 0; color: var(--foreground);">🚀 How to Use</h3>
    <ol style="margin: 0; padding-left: 1.25rem; font-size: 0.875rem; color: var(--muted-foreground);">
        <li>Upload your MusicXML file or sheet music image</li>
        <li>Watch the magic happen as we process your music</li>
        <li>Preview your beautiful piano roll visualization</li>
        <li>Download your creation to share with others</li>
        <li>Clean up files when you're done</li>
    </ol>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="musicsynth-card">
    <h3 style="margin: 0 0 0.5rem 0; color: var(--foreground);">📄 Supported Formats</h3>
    <div style="font-size: 0.875rem; color: var(--muted-foreground);">
        <div style="margin-bottom: 0.75rem;">
            <strong style="color: var(--foreground);">🎼 Music Files:</strong><br>
            <code style="background-color: var(--muted); padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-size: 0.75rem; margin: 0.125rem;">.musicxml</code>
            <code style="background-color: var(--muted); padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-size: 0.75rem; margin: 0.125rem;">.xml</code>
        </div>
        <div>
            <strong style="color: var(--foreground);">📷 Sheet Music Images:</strong><br>
            <code style="background-color: var(--muted); padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-size: 0.75rem; margin: 0.125rem;">.png</code>
            <code style="background-color: var(--muted); padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-size: 0.75rem; margin: 0.125rem;">.jpg</code>
            <code style="background-color: var(--muted); padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-size: 0.75rem; margin: 0.125rem;">.jpeg</code>
            <br><small style="opacity: 0.7; font-size: 0.75rem;">(desktop only)</small>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Theme info with MusicSynth branding
st.sidebar.markdown(f"""
<div class="musicsynth-card">
    <h3 style="margin: 0 0 0.5rem 0; color: var(--foreground);">🎨 Theme</h3>
    <p style="margin: 0; font-size: 0.875rem; color: var(--muted-foreground);">
        Using <strong style="color: var(--foreground);">Dark</strong> theme
    </p>
    <p style="margin: 0.25rem 0 0 0; font-size: 0.75rem; color: var(--muted-foreground);">
        Crafted for musicians and educators
    </p>
</div>
""", unsafe_allow_html=True)