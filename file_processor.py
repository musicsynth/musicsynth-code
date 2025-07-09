import os
import tempfile
import subprocess
import time
from datetime import datetime
import streamlit as st
from synthesia import parse_musicxml, make_video
import shutil
import uuid

class FileProcessor:
    def __init__(self):
        # Get the project root directory (where app.py is located)
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create temp and xml directories in the project folder
        self.temp_dir = os.path.join(self.project_dir, 'temp')
        self.xml_dir = os.path.join(self.project_dir, 'xml_files')
        
        # Create necessary directories with proper permissions
        for directory in [self.temp_dir, self.xml_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory, mode=0o777, exist_ok=True)
            else:
                # Ensure existing directories have proper permissions
                os.chmod(directory, 0o777)
        
        self.timing_stats = {}
        
        # Check if we're running in Streamlit Cloud
        is_streamlit_cloud = os.environ.get('STREAMLIT_SERVER_ENVIRONMENT') == 'cloud'
        
        if is_streamlit_cloud:
            self.use_cloud_omr = True
        else:
            try:
                result = subprocess.run(["which", "oemer"], capture_output=True, text=True)
                if result.returncode != 0:
                    raise RuntimeError("Oemer executable not found. Please ensure it is installed and in your PATH.")
                self.oemer_path = result.stdout.strip()
                self.use_cloud_omr = False
                print(f"Oemer path: {self.oemer_path}")
            except Exception as e:
                print(f"Error setting up Oemer: {str(e)}")
                self.use_cloud_omr = True
    
    def process_uploaded_file(self, uploaded_file):
        """
        Process an uploaded MusicXML or image file and generate a video visualization.
        
        Args:
            uploaded_file: The uploaded file object from Streamlit
            
        Returns:
            tuple: (success, message, output_path)
        """
        if uploaded_file is None:
            return False, "No file uploaded", None
        
        filename = uploaded_file.name.lower()
        is_musicxml = filename.endswith('.musicxml') or filename.endswith('.xml')
        is_image = filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg')
        
        if not (is_musicxml or is_image):
            return False, "Please upload a MusicXML file (.musicxml, .xml) or an image file (.png, .jpg, .jpeg)", None
        
        try:
            # Create a unique session directory using UUID
            session_id = str(uuid.uuid4())
            session_dir = os.path.join(self.temp_dir, f"session_{session_id}")
            os.makedirs(session_dir, mode=0o777, exist_ok=True)
            print(f"Created session directory: {session_dir}")
            
            # Save the uploaded file to the session directory
            save_start = time.time()
            temp_file_path = os.path.join(session_dir, uploaded_file.name)
            print(f"Saving uploaded file to: {temp_file_path}")
            with open(temp_file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            # Ensure file has proper permissions
            os.chmod(temp_file_path, 0o666)
            self.timing_stats['file_save'] = time.time() - save_start
            
            # If image, process it based on environment
            if is_image:
                if self.use_cloud_omr:
                    return False, "Image processing is currently not supported in the cloud environment. Please upload a MusicXML file instead.", None
                else:
                    # Use Oemer for local processing
                    print(f"Running Oemer on image: {temp_file_path}")
                    cmd = [self.oemer_path, "-o", session_dir, "--save-cache", "-d", temp_file_path]
                    oemer_start = time.time()
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode != 0:
                        print(f"Oemer failed with error: {result.stderr}")
                        return False, f"Oemer failed: {result.stderr}", None
                    self.timing_stats['oemer_processing'] = time.time() - oemer_start
                    
                    # Find the output MusicXML file
                    basename = os.path.splitext(os.path.basename(temp_file_path))[0]
                    musicxml_path = os.path.join(session_dir, f"{basename}.musicxml")
                    if not os.path.exists(musicxml_path):
                        musicxml_path = os.path.join(session_dir, f"{basename}.xml")
                        if not os.path.exists(musicxml_path):
                            print(f"Oemer did not produce a MusicXML file for {basename}")
                            return False, f"Oemer did not produce a MusicXML file for {basename}", None
                    
                    # Save a copy of the MusicXML file in the xml_files directory
                    xml_filename = f"{basename}_{session_id}.musicxml"
                    xml_save_path = os.path.join(self.xml_dir, xml_filename)
                    shutil.copy2(musicxml_path, xml_save_path)
                    os.chmod(xml_save_path, 0o666)  # Ensure XML file has proper permissions
                    print(f"Saved MusicXML file to: {xml_save_path}")
                    
                    print(f"Oemer produced MusicXML file: {musicxml_path}")
            else:
                # Use the uploaded MusicXML file
                musicxml_path = temp_file_path
                # Save a copy in the xml_files directory
                xml_filename = f"{os.path.splitext(os.path.basename(musicxml_path))[0]}_{session_id}.musicxml"
                xml_save_path = os.path.join(self.xml_dir, xml_filename)
                shutil.copy2(musicxml_path, xml_save_path)
                os.chmod(xml_save_path, 0o666)  # Ensure XML file has proper permissions
                print(f"Saved MusicXML file to: {xml_save_path}")
                print(f"Using uploaded MusicXML file: {musicxml_path}")
            
            # Parse the MusicXML file
            print(f"Parsing MusicXML file: {musicxml_path}")
            notes = parse_musicxml(musicxml_path)
            
            # Generate output video path
            output_filename = os.path.splitext(os.path.basename(musicxml_path))[0] + '_visualization.mp4'
            output_path = os.path.join(session_dir, output_filename)
            
            # Create the video
            print(f"Generating video: {output_path}")
            video_start = time.time()
            make_video(notes, output_file=output_path)
            os.chmod(output_path, 0o666)  # Ensure video file has proper permissions
            self.timing_stats['video_generation'] = time.time() - video_start
            
            # Log timing statistics
            self._log_timing_stats(uploaded_file.name, session_dir)
            
            return True, "Video generated successfully", output_path
            
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return False, f"Error processing file: {str(e)}", None
        
    def cleanup(self):
        """Clean up temporary files"""
        try:
            # Clean up all session directories
            for item in os.listdir(self.temp_dir):
                item_path = os.path.join(self.temp_dir, item)
                if os.path.isdir(item_path) and item.startswith('session_'):
                    shutil.rmtree(item_path, ignore_errors=True)
            # Recreate the base temp directory with proper permissions
            os.makedirs(self.temp_dir, mode=0o777, exist_ok=True)
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
    
    def _log_timing_stats(self, filename, session_dir):
        """Log timing statistics to a file."""
        log_entry = f"\n{datetime.now()}\n"
        log_entry += f"File: {filename}\n"
        for step, duration in self.timing_stats.items():
            log_entry += f"{step}: {duration:.2f} seconds\n"
        log_entry += "-" * 50
        
        log_path = os.path.join(session_dir, 'processing_stats.log')
        with open(log_path, 'a') as f:
            f.write(log_entry)
        os.chmod(log_path, 0o666)  # Ensure log file has proper permissions 