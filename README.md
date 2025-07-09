# MusicSynth
End-to-end sheet music converter that transforms sheet music into visual piano roll animations.

## Overview
MusicSynth is a powerful tool that can:
- Convert sheet music images (PNG, JPG, JPEG) to MusicXML format using OMR (Optical Music Recognition)
- Process MusicXML files directly
- Generate beautiful piano roll visualizations of the music
- Provide a user-friendly web interface for easy interaction

## Features
- Support for both MusicXML files and sheet music images
- Real-time processing with progress tracking
- Detailed processing statistics
- Clean and intuitive web interface
- Automatic cleanup of temporary files

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Oemer (Optical Music Recognition tool)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/MusicSynth.git
cd MusicSynth
```

### 2. Set Up Python Virtual Environment
```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Oemer
Oemer is required for processing sheet music images. Follow these steps:

1. Install Oemer using pip:
```bash
pip install oemer==0.1.5
```

2. Ensure Oemer is in your system PATH

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Upload your file:
   - Supported formats: MusicXML (.musicxml, .xml) or image files (.png, .jpg, .jpeg)
   - The application will process your file and generate a video visualization
   - Processing statistics will be displayed after completion

4. Use the "Clean Up Temporary Files" button to remove temporary files when done

## Dependencies
- numpy: Numerical computing
- pillow: Image processing
- moviepy: Video generation
- streamlit: Web interface
- oemer: Optical Music Recognition
- onnx & onnxruntime: Neural network inference
- tensorflow & keras: Deep learning framework
- pandas: Data manipulation

## License
This project is licensed under the terms of the included LICENSE file.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
