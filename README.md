# MusicSynth
Transform Sheet Music into Visual Magic - Experience the future of music learning with secure authentication and beautiful visualizations.

## Overview
MusicSynth revolutionizes music education by transforming traditional sheet music into engaging visual experiences. Built with passion by a high school student who believes in making music learning more accessible and exciting for everyone.

**Key Features:**
- Convert sheet music images to MusicXML using advanced Optical Music Recognition
- Transform MusicXML files into stunning visual piano roll animations
- Create beautiful music visualizations for educational purposes
- Secure user authentication with email/password registration
- Modern, responsive interface designed for musicians and educators
- Production-ready deployment with Docker and cloud support

## Features

### 🎼 **Optical Music Recognition**
- Upload sheet music images (PNG, JPG, JPEG) and watch them transform into digital scores
- Advanced image processing for accurate music transcription
- Support for various sheet music layouts and styles

### 🎹 **Visual Piano Roll**
- See your music come alive with stunning piano roll animations
- Smooth visual transitions and beautiful color schemes
- Educational focus for enhanced music learning

### 🎨 **Music Visualization**
- Create beautiful visual representations of your musical compositions
- High-quality video export for sharing and presentation
- Multiple visualization styles and themes

### 🔐 **Secure Authentication**
- Supabase-powered user registration and login system
- Email verification and password reset functionality
- Secure session management and user data protection

### 🌓 **Modern Interface**
- Light and dark theme support with seamless switching
- Custom color palette designed for music education
- Space Grotesk and Inter fonts for professional typography
- Responsive design optimized for all devices

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Oemer (Optical Music Recognition tool)
- Supabase account for authentication
- Docker (optional, for production deployment)

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/MusicSynth.git
cd MusicSynth
```

### 2. Set Up Supabase Authentication
1. Create a Supabase account at [https://supabase.com](https://supabase.com)
2. Create a new project
3. Go to **Settings** → **API**
4. Copy your **Project URL** and **anon/public key**

### 3. Configure Environment Variables
Create a `.env` file in your project root:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
STREAMLIT_SERVER_ENVIRONMENT=local
```

### 4. Set Up Python Virtual Environment
```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Install Oemer (for local image processing)
```bash
pip install oemer==0.1.5
```

### 7. Run the Application
```bash
streamlit run app.py
```

## Usage

### Authentication Flow
1. Open your web browser and navigate to http://localhost:8501
2. **Get Started**: Create a new account with email and password
   - Password must be at least 8 characters with uppercase, lowercase, and digit
3. **Sign In**: Use your credentials to access MusicSynth
4. **Password Reset**: Use "Forgot Your Password?" if needed

### Creating Musical Magic
1. **Upload**: Choose your MusicXML file or sheet music image
2. **Process**: Watch the magic happen as we transform your music
3. **Preview**: See your beautiful piano roll visualization
4. **Download**: Get your creation to share with others
5. **Clean Up**: Remove temporary files when done

### Features by Environment
- **Desktop Version**: Full Optical Music Recognition with image processing
- **Cloud Version**: MusicXML processing with secure authentication
- **Educational Focus**: Designed specifically for music learning and teaching

## MusicSynth Design System

### 🎨 **Color Palette**
- **Primary**: Purple (#8B5CF6) - Musical creativity and innovation
- **Secondary**: Cyan (#06B6D4) - Technology and precision
- **Accent**: Amber (#F59E0B) - Energy and learning
- **Success**: Green (#10B981) - Achievement and progress

### 🎯 **Typography**
- **Headings**: Space Grotesk - Modern, geometric font for impact
- **Body Text**: Inter - Highly readable font optimized for interfaces
- **Code**: JetBrains Mono - Technical elements and statistics

### 🌓 **Theme System**
- **Light Theme**: Clean, professional appearance for focused work
- **Dark Theme**: Comfortable viewing for extended sessions
- **Seamless Toggle**: Switch themes without losing progress
- **Educational Focus**: Colors and contrasts optimized for learning

## Production Deployment

### Docker (Recommended)
```bash
# Build and run with Docker
docker build -t musicsynth .
docker run -p 8501:8501 --env-file .env musicsynth

# Or use Docker Compose
docker-compose up -d
```

### Streamlit Cloud
1. Push your code to GitHub
2. Deploy on [Streamlit Cloud](https://share.streamlit.io)
3. Add environment variables in the dashboard

### VPS/Server Deployment
See `DEPLOYMENT.md` for detailed production deployment instructions including:
- systemd service configuration
- Nginx reverse proxy setup
- SSL/TLS certificate installation
- Monitoring and scaling

## Dependencies

### Core Technologies
- **Python**: Core application logic and processing
- **Streamlit**: Modern web interface framework
- **Supabase**: Authentication and user management
- **MuseScore**: Music notation processing

### Music Processing
- **Oemer**: Optical Music Recognition engine
- **TensorFlow**: Machine learning for music analysis
- **NumPy**: Numerical computing for audio processing
- **MoviePy**: Video generation and animation

### User Interface
- **Google Fonts**: Space Grotesk, Inter, JetBrains Mono
- **Custom CSS**: Modern design system with animations
- **Responsive Design**: Mobile-first approach

## File Structure
```
MusicSynth/
├── app.py                 # Main Streamlit application
├── auth.py               # Authentication system
├── config.py             # Configuration management
├── file_processor.py     # Music file processing
├── synthesia.py          # Video generation engine
├── theme_manager.py      # Modern theme system
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Multi-container setup
├── .streamlit/          # Streamlit configuration
│   └── config.toml      # MusicSynth theme colors
├── temp/               # Temporary processing files
├── xml_files/          # Processed music files
└── DEPLOYMENT.md       # Production deployment guide
```

## Educational Impact

### 🎓 **For Students**
- Visual learning through piano roll animations
- Better understanding of musical notation
- Engaging way to study music theory
- Accessible learning for different learning styles

### 👨‍🏫 **For Educators**
- Create engaging visual lessons
- Demonstrate musical concepts clearly
- Share professional-quality materials
- Enhance traditional music education

### 🎵 **For Musicians**
- Visualize compositions for analysis
- Create promotional materials
- Share music in accessible formats
- Enhance practice and performance

## Developer Story

MusicSynth was created by a passionate high school student who recognized the need for better music education tools. Combining a love for music with programming skills, this project represents the intersection of technology and education.

**Mission**: Make music learning more accessible and exciting for everyone through innovative visualization technology.

**Vision**: A world where every student can experience the joy of music through engaging, visual learning experiences.

## Contributing

We welcome contributions from developers, musicians, and educators! Please ensure you:

1. **Follow the Design System**: Use MusicSynth colors, fonts, and styling
2. **Focus on Education**: Consider the learning impact of new features
3. **Test Thoroughly**: Verify functionality across different music files
4. **Document Changes**: Update documentation for new features
5. **Maintain Quality**: Follow code quality standards and best practices

## License
This project is licensed under the terms of the included LICENSE file.

## Support

### Getting Help
1. Check the [DEPLOYMENT.md](DEPLOYMENT.md) guide for setup issues
2. Review `config.py` for configuration requirements
3. Ensure Supabase is properly configured
4. Verify Oemer installation for image processing

### Community
- **Issues**: Report bugs and request features on GitHub
- **Discussions**: Share ideas and get help from the community
- **Educational Use**: Special support for schools and educational institutions

---

**🎵 Ready to transform your music education experience?**

Visit [MusicSynth.github.io](https://musicsynth.github.io/) • Built with Python, Streamlit, MuseScore, and ❤️
