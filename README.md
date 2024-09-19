# 🎧 Binaural Beats Audio Converter with Subliminal Messaging

![App Banner](banner.jpg)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Health Benefits](#health-benefits)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
- [Usage](#usage)
  - [1. Upload Tab 📤](#1-upload-tab)
  - [2. Looper Tab 🌀](#2-looper-tab)
  - [3. Settings Tab ⚙️](#3-settings-tab)
  - [4. Preview Voice Tab 🎙️](#4-preview-voice-tab)
  - [5. Convert Tab 🔄](#5-convert-tab)
  - [Quit Button ❌](#quit-button)
- [Configuration](#configuration)
  - [IBM Watson Credentials](#ibm-watson-credentials)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

Welcome to the **Binaural Beats Audio Converter with Subliminal Messaging** application! This user-friendly Streamlit app allows you to enhance your audio files by overlaying binaural beats and subliminal affirmations. Whether you're looking to improve your mental focus, aid in sleep, or boost overall well-being, this app provides the tools you need to create personalized audio experiences.

## Features

### 📤 Upload
- **Upload Main WAV File:** Upload your primary audio file to enhance with binaural beats and subliminal messages.
- **Upload Subliminal Affirmations:** Optionally upload a text file containing subliminal messages to embed into your audio.

### 🌀 Looper
- **Loop WAV Files:** Upload a WAV file and loop it either by specifying the number of repeats or setting a total duration.
- **Smooth Transitions:** Apply fade transitions between loops for a seamless listening experience.
- **Waveform Visualization:** Visualize the waveform of both original and looped audio files.
- **Download Looped Audio:** Easily download your looped audio files for personal use.

### ⚙️ Settings
- **Customize Frequencies:** Adjust the base frequency and beat frequency for binaural beats to suit your preferences.
- **Volume Control:** Control the volume of the binaural beats to ensure they complement your main audio without overpowering it.

### 🎙️ Preview Voice
- **Voice Selection:** Choose from a variety of voices provided by IBM Watson Text-to-Speech.
- **Voice Preview:** Listen to a sample of the selected voice to ensure it meets your expectations before processing.

### 🔄 Convert
- **Audio Processing:** Overlay binaural beats and subliminal affirmations onto your selected audio file.
- **Waveform Visualization:** View the waveform of your processed audio to understand the enhancements made.
- **Download Processed Audio:** Download the final enhanced audio file for use in meditation, sleep, focus, or relaxation.

### ❌ Quit Button
- **Graceful Exit:** Safely terminate the application when you're done using it.

## Health Benefits

### 🧠 Binaural Beats
Binaural beats are an auditory illusion perceived when two slightly different frequencies are played in each ear. This phenomenon can influence brainwave activity, leading to various mental states:

- **Enhanced Focus:** Promote concentration and cognitive performance.
- **Stress Reduction:** Induce relaxation and alleviate stress.
- **Improved Sleep:** Facilitate better sleep quality and combat insomnia.
- **Meditation Aid:** Deepen meditation practices by guiding the brain into a state of calm.

### 🌟 Subliminal Affirmations
Subliminal affirmations involve embedding positive messages within audio tracks, often below the threshold of conscious perception. Benefits include:

- **Positive Mindset:** Reinforce self-confidence and positive thinking.
- **Habit Formation:** Support the development of healthy habits and behaviors.
- **Emotional Healing:** Aid in overcoming fears, anxieties, and negative emotions.
- **Motivation Boost:** Enhance motivation and goal achievement.

By combining binaural beats with subliminal affirmations, this app offers a comprehensive tool for personal development and mental well-being.

## Installation

### Prerequisites
- **Python 3.7 or higher:** Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- **FFmpeg:** Required by `pydub` for audio processing.
  - **Installation Instructions:**
    - **Windows:** Download the FFmpeg executable from [FFmpeg Downloads](https://ffmpeg.org/download.html) and add it to your system's PATH.
    - **macOS:** Install via Homebrew:
      ```bash
      brew install ffmpeg
      ```
    - **Linux:** Install via package manager (e.g., for Ubuntu/Debian):
      ```bash
      sudo apt-get install ffmpeg
      ```

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/binaural-beats-audio-converter.git
   cd binaural-beats-audio-converter
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   - **Using `requirements.txt`:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Alternatively, install manually:**
     ```bash
     pip install streamlit pydub ibm-watson numpy matplotlib
     ```

4. **Set Up IBM Watson Credentials**
   - **Create a `.streamlit` Directory:**
     ```bash
     mkdir .streamlit
     ```
   - **Create a `secrets.toml` File Inside `.streamlit`:**
     ```toml
     # .streamlit/secrets.toml

     IBM_API_KEY = "your_ibm_api_key"
     IBM_URL = "your_ibm_service_url"
     ```
     > **Note:** Replace `"your_ibm_api_key"` and `"your_ibm_service_url"` with your actual IBM Watson Text-to-Speech credentials. Ensure this file is **never** committed to version control for security reasons.

5. **(Optional) Add a Banner Image**
   - Place a `banner.jpg` image in the root directory of the project.
   - Ensure the image path in the script matches its location. The line in the script is commented out by default:
     ```python
     # st.image("banner.jpg", use_column_width=True)
     ```
   - To enable the banner, uncomment the line:
     ```python
     st.image("banner.jpg", use_column_width=True)
     ```

6. **Run the Streamlit App**
   ```bash
   streamlit run subliminal_ibm_streamlit.py
   ```

   The app should open in your default web browser. If it doesn't, navigate to the URL provided in the terminal (usually `http://localhost:8501`).

## Usage

### 1. Upload Tab 📤

- **Upload Main WAV File:**
  - Click on the **"Choose a WAV file"** button to upload your primary audio file.
  - Upon successful upload, the app will display the audio playback and its waveform for visual confirmation.

- **Upload Subliminal Affirmations (Optional):**
  - Click on the **"Choose a Text file with subliminal affirmations"** button to upload a `.txt` file containing your subliminal messages.
  - The app will notify you upon successful upload.

### 2. Looper Tab 🌀

- **Upload WAV File to Loop:**
  - Click on the **"Choose a WAV file to loop"** button to upload the audio file you wish to loop.

- **Configure Loop Settings:**
  - **Loop Method:** Choose between **"Number of Loops"** or **"Total Duration"**.
    - **Number of Loops:** Specify how many times the audio should repeat.
    - **Total Duration:** Set the total duration in seconds for the looped audio.
  - **Fade Duration:** Adjust the fade transition between loops for smoothness.

- **Process Audio:**
  - Click the **"🔁 Process Audio"** button to generate the looped audio.
  - After processing, the app will display the looped audio's waveform, playback functionality, and a download button.

### 3. Settings Tab ⚙️

- **Adjust Binaural Beat Settings:**
  - **Base Frequency (Hz):** Select the fundamental frequency for the binaural beats.
  - **Beat Frequency (Hz):** Choose the frequency difference to create the desired beat effect.
  - **Binaural Beat Volume (dB):** Control the loudness of the binaural beats to ensure they complement your main audio.

### 4. Preview Voice Tab 🎙️

- **Preview TTS Voice:**
  - Click the **"🔊 Preview Voice"** button to listen to a sample of the selected IBM Watson Text-to-Speech voice.
  - This feature allows you to ensure the voice meets your preferences before processing your audio.

### 5. Convert Tab 🔄

- **Select Audio Source:**
  - **Upload a New WAV File:** Upload a fresh audio file for processing.
  - **Use a Looped WAV File:** Choose from previously looped audio files available in the dropdown menu.

- **Upload Subliminal Affirmations (Optional):**
  - Similar to the Upload tab, you can upload a text file with subliminal messages to embed into your selected audio.

- **Configure Binaural Beat Settings:**
  - Adjust the base frequency, beat frequency, and volume as needed.

- **Process Audio:**
  - Click the **"▶️ Convert Audio"** button to overlay binaural beats and subliminal messages onto your selected audio.
  - The app will display the processed audio's waveform, playback functionality, and provide a download button for the final enhanced audio.

### ❌ Quit Button

- **Exit the App:**
  - Click the **"❌ Quit"** button located at the bottom of the app to gracefully terminate the Streamlit server.
  - **Note:** This action will stop the app immediately. To use the app again, you will need to restart it manually using the `streamlit run` command.

## Configuration

### IBM Watson Credentials

To enable the Text-to-Speech functionality, you need to set up IBM Watson credentials:

1. **Obtain API Credentials:**
   - Sign up or log in to your [IBM Cloud account](https://cloud.ibm.com/).
   - Navigate to the [Text-to-Speech service](https://cloud.ibm.com/catalog/services/text-to-speech).
   - Create a new service instance if you haven't already.
   - Retrieve your **API Key** and **Service URL** from the service credentials.

2. **Store Credentials Securely:**
   - Create a `.streamlit` directory in your project root.
   - Inside `.streamlit`, create a `secrets.toml` file:
     ```toml
     # .streamlit/secrets.toml

     IBM_API_KEY = "your_ibm_api_key"
     IBM_URL = "your_ibm_service_url"
     ```
   - Replace `"your_ibm_api_key"` and `"your_ibm_service_url"` with your actual credentials.
   - **Important:** Ensure this file is **not** added to version control to protect your credentials.

## Contributing

Contributions are welcome! If you'd like to improve this project, please follow these steps:

1. **Fork the Repository**
2. **Create a New Branch**
   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. **Make Your Changes**
4. **Commit Your Changes**
   ```bash
   git commit -m "Add Your Feature"
   ```
5. **Push to Your Fork**
   ```bash
   git push origin feature/YourFeatureName
   ```
6. **Create a Pull Request**

Please ensure your code adheres to the project's coding standards and includes appropriate documentation.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Streamlit](https://streamlit.io/) for providing an easy-to-use framework for building interactive web apps.
- [pydub](https://github.com/jiaaro/pydub) for powerful audio processing capabilities.
- [IBM Watson Text-to-Speech](https://www.ibm.com/cloud/watson-text-to-speech) for enabling high-quality voice synthesis.
- [Matplotlib](https://matplotlib.org/) and [NumPy](https://numpy.org/) for waveform visualization.

---

**Disclaimer:** This application is intended for personal use. Ensure you have the necessary permissions and licenses to use the uploaded audio files and subliminal affirmations.
