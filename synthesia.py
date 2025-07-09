#!/usr/bin/env python3
"""
Synthesia-like app for violin that creates a video visualization
of notes to play on a violin fingerboard from a musicxml file.
"""

import os
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import *

# Violin string notes (G3, D4, A4, E5)
VIOLIN_STRINGS = ["G", "D", "A", "E"]
STRING_COLORS = [(139, 69, 19), (165, 42, 42), (205, 133, 63), (210, 180, 140)]  # Brown colors for strings
NOTE_COLOR = (0, 191, 255)  # Deep sky blue for notes
HIGHLIGHT_COLOR = (255, 0, 0)  # Red for currently playing note

# Define the fingerboard dimensions
FB_WIDTH = 800
FB_HEIGHT = 300
STRING_SPACING = FB_HEIGHT // 5
FRET_SPACING = FB_WIDTH // 16

# Define the note positions on each string
# This is a simplified mapping of notes to finger positions
NOTE_POSITIONS = {
    # G string (G3 to G5)
    "G3": (0, 0), "G#3": (1, 0), "A3": (2, 0), "A#3": (3, 0), 
    "B3": (4, 0), "C4": (5, 0), "C#4": (6, 0), "D4": (7, 0),
    "D#4": (8, 0), "E4": (9, 0), "F4": (10, 0), "F#4": (11, 0),
    "G4": (12, 0), "G#4": (13, 0), "A4": (14, 0), "A#4": (15, 0),
    
    # D string (D4 to D6)
    "D4": (0, 1), "D#4": (1, 1), "E4": (2, 1), "F4": (3, 1),
    "F#4": (4, 1), "G4": (5, 1), "G#4": (6, 1), "A4": (7, 1),
    "A#4": (8, 1), "B4": (9, 1), "C5": (10, 1), "C#5": (11, 1),
    "D5": (12, 1), "D#5": (13, 1), "E5": (14, 1), "F5": (15, 1),
    
    # A string (A4 to A6)
    "A4": (0, 2), "A#4": (1, 2), "B4": (2, 2), "C5": (3, 2),
    "C#5": (4, 2), "D5": (5, 2), "D#5": (6, 2), "E5": (7, 2),
    "F5": (8, 2), "F#5": (9, 2), "G5": (10, 2), "G#5": (11, 2),
    "A5": (12, 2), "A#5": (13, 2), "B5": (14, 2), "C6": (15, 2),
    
    # E string (E5 to E7)
    "E5": (0, 3), "F5": (1, 3), "F#5": (2, 3), "G5": (3, 3),
    "G#5": (4, 3), "A5": (5, 3), "A#5": (6, 3), "B5": (7, 3),
    "C6": (8, 3), "C#6": (9, 3), "D6": (10, 3), "D#6": (11, 3),
    "E6": (12, 3), "F6": (13, 3), "F#6": (14, 3), "G6": (15, 3),
}

def parse_musicxml(file_path):
    """Parse musicxml file and extract notes with timing information."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    notes = []
    current_time = 0
    
    # Find divisions (ticks per quarter note)
    divisions = int(root.find('.//divisions').text)
    
    # Process each measure
    for measure in root.findall('.//measure'):
        for note in measure.findall('note'):
            # Skip rests
            if note.find('rest') is not None:
                if note.find('duration') is not None:
                    duration = int(note.find('duration').text)
                    current_time += duration / divisions
                continue
            
            # Get pitch information
            pitch = note.find('pitch')
            if pitch is None:
                continue
                
            step = pitch.find('step').text
            octave = pitch.find('octave').text
            
            # Check for accidentals
            alter_elem = pitch.find('alter')
            alter = 0
            if alter_elem is not None:
                alter = int(alter_elem.text)
            
            # Determine the note name
            accidental = ""
            if alter == 1:
                accidental = "#"
            elif alter == -1:
                accidental = "b"
            
            note_name = f"{step}{accidental}{octave}"
            
            # Get duration
            duration = int(note.find('duration').text)
            duration_in_seconds = duration / divisions
            
            # Add the note to our list
            notes.append({
                "note": note_name,
                "start_time": current_time,
                "duration": duration_in_seconds
            })
            
            current_time += duration_in_seconds
    
    return notes

def create_fingerboard_frame(notes, current_time, frame_size=(1280, 720)):
    """Create a single frame of the fingerboard with the current note highlighted."""
    # Create a blank canvas
    img = Image.new('RGB', frame_size, color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Calculate the position of the fingerboard in the frame
    fb_x = (frame_size[0] - FB_WIDTH) // 2
    fb_y = (frame_size[1] - FB_HEIGHT) // 2
    
    # Draw the fingerboard
    draw.rectangle([fb_x, fb_y, fb_x + FB_WIDTH, fb_y + FB_HEIGHT], fill=(50, 50, 50), outline=(100, 100, 100))
    
    # Draw the strings
    for i, string in enumerate(VIOLIN_STRINGS):
        y = fb_y + (i + 1) * STRING_SPACING
        draw.line([(fb_x, y), (fb_x + FB_WIDTH, y)], fill=STRING_COLORS[i], width=3)
        # Label the strings
        draw.text((fb_x - 30, y - 10), string, fill=(255, 255, 255))
    
    # Draw fret markers and label the positions
    # Label position 0
    draw.text((fb_x - 5, fb_y - 20), "0", fill=(150, 150, 150))
    # Label the rest of the positions
    for i in range(1, 16):
        x = fb_x + i * FRET_SPACING
        draw.line([(x, fb_y), (x, fb_y + FB_HEIGHT)], fill=(100, 100, 100), width=1)
        # Label the positions: 0, -1, 1, 2, 2+, 3, ..., 13
        if i == 1:
            label = "-1"
        elif i == 2:
            label = "1"
        elif i == 3:
            label = "2"
        elif i == 4:
            label = "2+"
        else: # i >= 5
            label = str(i - 2)
        # Adjust x-position for better alignment
        draw.text((x - 5, fb_y - 20), label, fill=(150, 150, 150))
    
    # --- Determine Active Notes --- 
    active_notes_this_frame = []
    for note in notes:
        if note["start_time"] <= current_time < note["start_time"] + note["duration"]:
            active_notes_this_frame.append(note)
    # --- End Determine Active Notes ---

    # --- Draw Inactive Notes (Blue) --- 
    for note in notes:
        if note not in active_notes_this_frame:
            note_name = note["note"]
            base_note = note_name # Reset base_note

            # Handle accidentals
            if "#" in note_name: base_note = note_name.replace("#", "")
            elif "b" in note_name:
                step, octave = note_name[0], note_name[-1]
                if step == "A": base_note = f"G#{octave}"
                elif step == "B": base_note = f"A#{octave}"
                elif step == "C": base_note = f"B{int(octave)-1}"
                elif step == "D": base_note = f"C#{octave}"
                elif step == "E": base_note = f"D#{octave}"
                elif step == "F": base_note = f"E{octave}"
                elif step == "G": base_note = f"F#{octave}"
            
            # Get position
            try:
                note_pos = NOTE_POSITIONS.get(note_name) or NOTE_POSITIONS.get(base_note)
                if note_pos:
                    pos_x, string_idx = note_pos
                    x = fb_x + pos_x * FRET_SPACING
                    y = fb_y + (string_idx + 1) * STRING_SPACING
                    # Draw inactive note
                    draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=NOTE_COLOR, outline=(255, 255, 255))
            except Exception: pass # Ignore errors for inactive notes
    # --- End Draw Inactive Notes ---

    # --- Draw Active Notes (Red) and Labels --- 
    active_note_names = []
    for note in active_notes_this_frame: # Iterate only through active notes
        note_name = note["note"]
        base_note = note_name # Reset base_note

        # Handle accidentals (same logic as above)
        if "#" in note_name: base_note = note_name.replace("#", "")
        elif "b" in note_name:
            step, octave = note_name[0], note_name[-1]
            if step == "A": base_note = f"G#{octave}"
            elif step == "B": base_note = f"A#{octave}"
            elif step == "C": base_note = f"B{int(octave)-1}"
            elif step == "D": base_note = f"C#{octave}"
            elif step == "E": base_note = f"D#{octave}"
            elif step == "F": base_note = f"E{octave}"
            elif step == "G": base_note = f"F#{octave}"

        # Get position
        try:
            note_pos = NOTE_POSITIONS.get(note_name) or NOTE_POSITIONS.get(base_note)
            if note_pos:
                pos_x, string_idx = note_pos
                x = fb_x + pos_x * FRET_SPACING
                y = fb_y + (string_idx + 1) * STRING_SPACING

                # Draw the active note in highlight color (overwriting if necessary)
                draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=HIGHLIGHT_COLOR, outline=(255, 255, 255))

                # Determine the finger position label based on pos_x
                if pos_x == 0:
                    fret_label = "0"
                elif pos_x == 1:
                    fret_label = "-1"
                elif pos_x == 2:
                    fret_label = "1"
                elif pos_x == 3:
                    fret_label = "2"
                elif pos_x == 4:
                    fret_label = "2+"
                else: # pos_x >= 5
                    fret_label = str(pos_x - 2)

                # Display note name above using the finger position label
                step = note["note"][0]  # Get the note letter (e.g., 'E')
                new_label = f"{step}{fret_label}"  # Create the new label (e.g., 'E1', 'C2+')
                draw.text((x - 15, y - 30), new_label, fill=(255, 255, 255))

                active_note_names.append(new_label) # Add the new label to list for title
        except Exception as e:
             # print(f"Warning: Could not process active note {note} at time {current_time}: {e}") # Optional debug
             pass
    # --- End Draw Active Notes ---

    # Add some information at the top
    try:
        font = ImageFont.truetype("Arial", 24)
    except:
        font = ImageFont.load_default()

    # Display active note name(s) at the top, or just the time
    if active_note_names:
        title = f"Now Playing: {', '.join(active_note_names)} (Time: {current_time:.2f}s)"
    else:
        title = f"Time: {current_time:.2f}s"

    draw.text((frame_size[0] // 2 - 150, 30), title, fill=(255, 255, 255), font=font)
    
    return np.array(img, dtype=np.uint8)

def make_video(notes, output_file="violin_tutorial.mp4", fps=30, duration=None):
    """Create a video tutorial of the notes to be played on the violin."""
    if duration is None:
        # Calculate duration from the last note
        last_note = notes[-1]
        duration = last_note["start_time"] + last_note["duration"] + 1  # Add 1 second buffer at the end
    
    # Create a clip using MoviePy
    clip = VideoClip(lambda t: create_fingerboard_frame(notes, t), duration=duration)
    
    # Set the frame rate
    clip = clip.with_fps(fps)
    
    # Write the result to a file
    clip.write_videofile(output_file, codec="libx264", fps=fps)
    
    return output_file

def main():
    """Main function to run the application."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate a Synthesia-like video for violin from a MusicXML file.")
    parser.add_argument("input_file", help="Input MusicXML file")
    parser.add_argument("--output", "-o", default="violin_tutorial.mp4", help="Output video file (default: violin_tutorial.mp4)")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second (default: 30)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        return
    
    print(f"Parsing MusicXML file: {args.input_file}")
    notes = parse_musicxml(args.input_file)
    
    if not notes:
        print("No notes found in the input file.")
        return
    
    print(f"Found {len(notes)} notes. Generating video...")
    output_file = make_video(notes, output_file=args.output, fps=args.fps)
    
    print(f"Video generated: {output_file}")

if __name__ == "__main__":
    main()