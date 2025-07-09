import streamlit as st
from file_processor import FileProcessor
import os
import time
from datetime import datetime
import pandas as pd

# Set page config
st.set_page_config(
    page_title="MusicSynth",
    page_icon="🎵",
    layout="wide"
)

# Initialize session state for file processor if it doesn't exist
if 'file_processor' not in st.session_state:
    st.session_state.file_processor = FileProcessor()

st.title("🎵 MusicSynth - Sheet Music Visualizer")

# Add environment info
is_cloud = os.environ.get('STREAMLIT_SERVER_ENVIRONMENT') == 'cloud'
if is_cloud:
    st.info("Running in Streamlit Cloud environment. Image processing is not available. Please upload MusicXML files only.")

# File upload section
st.header("Upload MusicXML or Image File")
uploaded_file = st.file_uploader(
    "Choose a MusicXML file (.musicxml, .xml) or an image file (.png, .jpg, .jpeg)",
    type=['musicxml', 'xml', 'png', 'jpg', 'jpeg'] if not is_cloud else ['musicxml', 'xml']
)

if uploaded_file is not None:
    # Initialize timing statistics
    timing_stats = {
        'start_time': time.time(),
        'steps': {}
    }
    
    # Process the uploaded file
    with st.spinner("Processing your file..."):
        st.info("Starting file processing...")
        
        # Track file processing time
        process_start = time.time()
        success, message, output_path = st.session_state.file_processor.process_uploaded_file(uploaded_file)
        timing_stats['steps']['file_processing'] = time.time() - process_start
        
        if success:
            st.success(message)
            
            # Track video generation time
            video_start = time.time()
            
            # Try to display the video
            try:
                with open(output_path, 'rb') as video_file:
                    video_bytes = video_file.read()
                    st.video(video_bytes)
            except Exception as e:
                st.warning("Video preview is not available. You can download the video file instead.")
            
            # Add download button for the video
            with open(output_path, 'rb') as video_file:
                video_bytes = video_file.read()
                st.download_button(
                    label="Download Video",
                    data=video_bytes,
                    file_name=os.path.basename(output_path),
                    mime="video/mp4"
                )
            
            timing_stats['steps']['video_generation'] = time.time() - video_start
            
            # Calculate total time
            timing_stats['total_time'] = time.time() - timing_stats['start_time']
            
            # Display timing statistics
            st.subheader("Processing Statistics")
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
            st.error(message)

# Add a cleanup button
if st.button("Clean Up Temporary Files"):
    st.session_state.file_processor.cleanup()
    st.success("Temporary files cleaned up successfully!")

# Add footer
st.markdown("---")
st.markdown("### About")
st.markdown("""
MusicSynth is a tool that converts sheet music into visual piano roll animations.
- For local use: Supports both MusicXML files and sheet music images
- For cloud use: Currently supports MusicXML files only
""")