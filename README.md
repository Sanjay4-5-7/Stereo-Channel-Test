# Headphone Left/Right Channel Tester

This script helps you test if your headphones are working correctly by playing audio tones to specific channels.

## Features

- 🖥️ **GUI Mode** - Easy-to-use graphical interface with sliders
- ⚡ **Simple CLI Mode** - Ultra-lightweight command-line version
- 🎛️ **Custom Settings** - Set any frequency (100-2000Hz) and duration (0.5-5s)
- 🔊 **Audio Device Selection** - Choose and switch between audio outputs
- 🎵 Individual channel testing (left/right/both)
- 🔄 Alternating channel tests
- 📱 Quick preset buttons (220Hz, 440Hz, 880Hz)
- ⏹️ Stop/interrupt functionality

## Requirements

- Python 3.6 or higher
- sounddevice library
- numpy library

## Installation & Usage

### Option 1: Quick GUI Launch (Recommended)
1. Double-click `run_gui.bat`
2. Installs dependencies and opens the GUI

### Option 2: Manual Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the script:
   ```bash
   python headphone_test.py
   ```

## How to Use

1. Connect your headphones
2. Set volume to a comfortable level
3. Run the script
4. Follow the on-screen prompts
5. Choose from the menu options:
   - Full test: Complete automated test sequence
   - Individual channel tests
   - Alternating channel test

## What to Listen For

During the test, you should hear:
- ✅ Sound in BOTH ears during stereo test
- ✅ Sound only in LEFT ear during left channel test
- ✅ Sound only in RIGHT ear during right channel test
- ✅ Sound switching between left and right during alternating test

If you don't hear sound in the expected ear, there may be an issue with:
- Your headphone wiring
- Audio driver settings
- Hardware connections

## Troubleshooting

- **No sound**: Check volume levels and audio device selection
- **Wrong channel**: Your headphones may be worn backwards or have crossed wiring
- **Import errors**: Make sure to install the required packages with `pip install -r requirements.txt`

## Technical Details

- Sample Rate: 44.1 kHz
- Test Frequencies: 220Hz (low), 440Hz (mid), 880Hz (high)
- Duration: 3 seconds per tone (1 second for alternating)
- Fade in/out applied to prevent audio clicks
