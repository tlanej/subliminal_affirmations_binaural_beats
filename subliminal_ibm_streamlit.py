import streamlit as st
from pydub import AudioSegment
from pydub.generators import Sine
from io import BytesIO
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import tempfile
import os
import numpy as np
import matplotlib.pyplot as plt
import sys

# -----------------------------
# Initialize Session State
# -----------------------------
if 'looped_files' not in st.session_state:
    st.session_state.looped_files = {}
if 'voices' not in st.session_state:
    st.session_state.voices = []
if 'tts_service' not in st.session_state:
    st.session_state.tts_service = None
if 'selected_voice_id' not in st.session_state:
    st.session_state.selected_voice_id = None
if 'base_freq' not in st.session_state:
    st.session_state.base_freq = 440  # Default base frequency
if 'beat_freq' not in st.session_state:
    st.session_state.beat_freq = 2  # Default beat frequency
if 'binaural_volume' not in st.session_state:
    st.session_state.binaural_volume = -15  # Default binaural volume

# -----------------------------
# Define Helper Functions
# -----------------------------

def loop_audio(audio, loop_count=None, loop_duration=None, fade_duration=1000):
    """
    Loops the audio either by count or duration and applies fading between loops.

    Parameters:
    - audio: pydub.AudioSegment
    - loop_count: int, number of times to loop
    - loop_duration: int, total duration in milliseconds
    - fade_duration: int, duration of fade in milliseconds

    Returns:
    - pydub.AudioSegment
    """
    if loop_count:
        # Create the looped audio by repeating
        looped = audio
        for _ in range(loop_count - 1):
            looped = looped.append(audio, crossfade=fade_duration)
    elif loop_duration:
        # Loop until the total duration is met
        looped = AudioSegment.empty()
        while len(looped) < loop_duration:
            looped = looped.append(audio, crossfade=fade_duration)
        looped = looped[:loop_duration]
    else:
        # If neither is specified, return the original audio
        looped = audio

    return looped

def initialize_tts(ibm_api_key, ibm_url):
    """
    Initializes the IBM Watson Text-to-Speech service.

    Parameters:
    - ibm_api_key: str, IBM Watson API Key
    - ibm_url: str, IBM Watson service URL

    Returns:
    - tts_service: ibm_watson.TextToSpeechV1 object
    """
    try:
        authenticator = IAMAuthenticator(ibm_api_key)
        tts_service = TextToSpeechV1(authenticator=authenticator)
        tts_service.set_service_url(ibm_url)
        return tts_service
    except Exception as e:
        st.error(f"Failed to initialize IBM Watson TTS service: {e}")
        return None

def get_voices(tts_service):
    """
    Retrieves available voices from IBM Watson Text-to-Speech service.

    Parameters:
    - tts_service: ibm_watson.TextToSpeechV1 object

    Returns:
    - List of tuples containing voice identifiers and descriptions
    """
    try:
        voices = tts_service.list_voices().get_result()['voices']
        if not voices:
            st.error("No voices available from IBM Watson TTS service.")
            return []
        # Use 'name' as the unique identifier
        return [(voice['name'], f"{voice['name']} ({voice['language']})") for voice in voices]
    except Exception as e:
        st.error(f"Error fetching voices: {e}")
        return []

def generate_binaural_beats(base_freq, beat_freq, duration_ms, volume_adjustment_db):
    """
    Generates binaural beats by creating two sine waves at slightly different frequencies
    and overlaying them into a stereo audio segment.

    Parameters:
    - base_freq (int): The base frequency in Hz for the left ear.
    - beat_freq (int): The beat frequency in Hz to be added to the base frequency for the right ear.
    - duration_ms (int): Duration of the audio in milliseconds.
    - volume_adjustment_db (int): Volume adjustment in decibels (dB) for the binaural beats.

    Returns:
    - AudioSegment: A stereo audio segment containing the binaural beats.
    """
    try:
        left_tone = Sine(base_freq).to_audio_segment(duration=duration_ms)
        right_tone = Sine(base_freq + beat_freq).to_audio_segment(duration=duration_ms)
        binaural_beat = AudioSegment.from_mono_audiosegments(left_tone, right_tone)
        
        # Adjust the volume of the binaural beats
        binaural_beat = binaural_beat + volume_adjustment_db  # dBFS adjustment
        
        return binaural_beat
    except Exception as e:
        st.error(f"Error generating binaural beats: {e}")
        return AudioSegment.silent(duration=duration_ms)  # Return silence if there's an error

def ibm_watson_tts(tts_service, text, voice_name='en-US_AllisonV3Voice', audio_file='output.wav'):
    """
    Converts text to speech using IBM Watson Text-to-Speech service.

    Parameters:
    - tts_service: ibm_watson.TextToSpeechV1 object
    - text: str, text to convert
    - voice_name: str, selected voice
    - audio_file: str, path to save the output WAV file

    Returns:
    - audio_file: str, path to the saved WAV file
    """
    try:
        response = tts_service.synthesize(
            text=text,
            voice=voice_name,
            accept='audio/wav'
        ).get_result()

        # Save the response content as a WAV file
        with open(audio_file, 'wb') as audio:
            audio.write(response.content)
        # st.write(f"🎤 Audio content written to **{audio_file}**")
        return audio_file
    except Exception as e:
        st.error(f"Error during TTS synthesis: {e}")
        return None

def loop_subliminal_audio(subliminal_audio, duration_ms):
    """
    Loops and trims subliminal audio to match the duration of the main audio.

    Parameters:
    - subliminal_audio: pydub.AudioSegment
    - duration_ms: int, duration in milliseconds

    Returns:
    - subliminal_audio: pydub.AudioSegment
    """
    try:
        # Loop the subliminal audio to match or exceed the duration of the main audio
        loops_needed = duration_ms // len(subliminal_audio) + 1
        looped_audio = subliminal_audio * loops_needed

        # Trim the looped audio to the exact duration of the main audio
        trimmed_audio = looped_audio[:duration_ms]
        return trimmed_audio
    except Exception as e:
        st.error(f"Error during subliminal audio looping: {e}")
        return subliminal_audio

def plot_waveform(audio_segment, title="Audio Waveform"):
    """
    Plots the waveform of an AudioSegment.

    Parameters:
    - audio_segment: pydub.AudioSegment
    - title: str, title of the plot

    Returns:
    - None
    """
    # Extract raw data as a NumPy array
    data = np.array(audio_segment.get_array_of_samples())
    
    # If stereo, take one channel
    if audio_segment.channels == 2:
        data = data[::2]
    
    # Create time axis in seconds
    time = np.linspace(0, len(audio_segment) / 1000, num=len(data))
    
    # Plot waveform
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(time, data, color='skyblue')
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title(title)
    ax.set_xlim(0, len(audio_segment) / 1000)
    ax.set_ylim(-32768, 32767)
    ax.axis('off')  # Remove axes for a cleaner look
    st.pyplot(fig)

def process_audio(input_wav, subliminal_text, base_freq, beat_freq, selected_voice, tts_service, binaural_volume_db):
    """
    Processes the audio by overlaying binaural beats and subliminal messages.

    Parameters:
    - input_wav: str, path to the input WAV file
    - subliminal_text: UploadedFile or None, subliminal text file
    - base_freq: int, base frequency for binaural beats
    - beat_freq: int, beat frequency for binaural beats
    - selected_voice: str, selected TTS voice
    - tts_service: ibm_watson.TextToSpeechV1 object
    - binaural_volume_db: int, volume adjustment for binaural beats

    Returns:
    - output_audio_path: str, path to the processed WAV file
    """
    try:
        # Load original audio and generate binaural beats with volume control
        original_audio = AudioSegment.from_wav(input_wav)
        duration = len(original_audio)  # Duration in milliseconds
        binaural_audio = generate_binaural_beats(base_freq, beat_freq, duration, binaural_volume_db)

        # Overlay original audio with binaural beats
        output_audio = original_audio.overlay(binaural_audio)

        # Check if a subliminal text file is loaded for TTS
        if subliminal_text:
            subliminal_text.seek(0)  # Reset file pointer
            affirmations = subliminal_text.read().decode("utf-8")  # Read and decode the file

            # Convert affirmations to speech using IBM Watson TTS
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_tts_file:
                tts_wav_file = ibm_watson_tts(tts_service, affirmations, selected_voice, temp_tts_file.name)

            if tts_wav_file:
                # Load the IBM Watson-generated speech and use it
                subliminal_audio = AudioSegment.from_wav(tts_wav_file)

                # Adjust subliminal message volume (reduce to -30 dB)
                subliminal_audio = subliminal_audio - 30

                # Loop and trim subliminal audio to match the duration of the main audio
                subliminal_audio = loop_subliminal_audio(subliminal_audio, duration)

                # Overlay subliminal TTS onto the final output
                output_audio = output_audio.overlay(subliminal_audio)

        # Export the final audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_output_file:
            output_audio.export(temp_output_file.name, format="wav")
            return temp_output_file.name

    except Exception as e:
        st.error(f"An error occurred during processing: {str(e)}")
        return None

# -----------------------------
# Streamlit App Layout
# -----------------------------

# Uncomment the following line if you have 'banner.jpg' in your directory
# st.image("banner.jpg", use_column_width=True)

# App Title and Description
st.markdown("""
# 🎧 Binaural Beats Audio Converter with Subliminal Messaging

Enhance your audio experience by overlaying binaural beats and subliminal affirmations.
""")

# Define Tabs
tab_upload, tab_looper, tab_settings, tab_preview, tab_convert = st.tabs(["📤 Upload", "🌀 Looper", "⚙️ Settings", "🎙️ Preview Voice", "🔄 Convert"])

# -----------------------------
# Upload Tab
# -----------------------------
with tab_upload:
    st.header("📤 1. Upload Main WAV File")
    uploaded_wav = st.file_uploader("Choose a WAV file", type=["wav"], help="Upload the main audio file you want to enhance with binaural beats.")
    
    if uploaded_wav:
        st.success(f"✅ Loaded: {uploaded_wav.name}")
        # Display waveform
        original_audio = AudioSegment.from_wav(uploaded_wav)
        st.subheader("🎵 Original Audio Waveform")
        plot_waveform(original_audio, title="Original Audio Waveform")
    else:
        st.info("ℹ️ No file uploaded yet.")

    st.markdown("---")

    # Upload Subliminal Text File
    st.header("📄 2. Upload Subliminal Affirmations Text File (Optional)")
    uploaded_text = st.file_uploader("Choose a Text file with subliminal affirmations", type=["txt"], help="Upload a text file containing subliminal messages to embed into your audio.")
    
    if uploaded_text:
        st.success(f"✅ Loaded: {uploaded_text.name}")
    else:
        st.info("ℹ️ No subliminal text file uploaded.")

# -----------------------------
# Looper Tab
# -----------------------------
with tab_looper:
    st.header("🌀 2. Loop Your WAV File")
    uploaded_loop_file = st.file_uploader("Choose a WAV file to loop", type=["wav"], key="loop_wav", help="Upload a WAV file you wish to loop.")
    
    if uploaded_loop_file:
        # Load audio file
        audio_to_loop = AudioSegment.from_wav(uploaded_loop_file)
        st.audio(uploaded_loop_file)
        
        st.sidebar.header("🔄 Loop Settings")
        
        loop_method = st.sidebar.radio("🔄 Loop by:", ("Number of Loops", "Total Duration"), help="Choose to loop by specifying the number of repeats or the total duration.")
        
        loop_count = None
        loop_duration = None
        
        if loop_method == "Number of Loops":
            loop_count = st.sidebar.number_input("🔢 Number of Loops", min_value=1, value=2, step=1)
        else:
            loop_duration_min = int(len(audio_to_loop) / 1000)  # Minimum duration in seconds
            loop_duration = st.sidebar.number_input(
                "⏲️ Total Duration (seconds)",
                min_value=loop_duration_min,
                value=loop_duration_min * 2,
                step=1,
                help="Specify the total duration for the looped audio in seconds."
            )
            loop_duration = loop_duration * 1000  # Convert to milliseconds
        
        fade_duration = st.sidebar.slider(
            "🔉 Fade Duration (ms)",
            min_value=0,
            max_value=5000,
            value=1000,
            step=100,
            help="Duration of fade transition between loops in milliseconds."
        )
        
        if st.sidebar.button("🔁 Process Audio"):
            with st.spinner("🔄 Processing..."):
                looped_audio = loop_audio(
                    audio_to_loop,
                    loop_count=loop_count,
                    loop_duration=loop_duration,
                    fade_duration=fade_duration
                )
                
                # Export to WAV in memory
                buf = BytesIO()
                looped_audio.export(buf, format="wav")
                buf.seek(0)
                
                # Generate a unique name for the looped file
                loop_name = f"Looped_{uploaded_loop_file.name}"
                
                # Store in session_state
                st.session_state.looped_files[loop_name] = buf.getvalue()
                
                st.success("✅ Audio looping complete!")
                
                # Display looped audio waveform
                st.subheader("🎵 Looped Audio Waveform")
                plot_waveform(looped_audio, title="Looped Audio Waveform")
                
                # Play looped audio
                st.audio(buf, format="audio/wav")
                
                # Download button
                st.download_button(
                    label="💾 Download Looped Audio",
                    data=buf,
                    file_name=loop_name,
                    mime="audio/wav"
                )
    else:
        st.info("ℹ️ No loop file uploaded yet.")

# -----------------------------
# Settings Tab
# -----------------------------
with tab_settings:
    st.header("⚙️ 3. Settings")
    st.markdown("""
    Adjust the **Base Frequency**, **Beat Frequency**, and **Binaural Beat Volume** to customize your audio experience.
    """)

    # Input fields for IBM Watson TTS API Key and URL
    st.subheader("🔑 IBM Watson Text-to-Speech Credentials")
    ibm_api_key = st.text_input("IBM Watson API Key", type="password", help="Enter your IBM Watson Text-to-Speech API Key.")
    ibm_url = st.text_input("IBM Watson Service URL", help="Enter your IBM Watson Text-to-Speech service URL.")

    # Initialize tts_service when credentials are provided
    if ibm_api_key and ibm_url:
        tts_service = initialize_tts(ibm_api_key, ibm_url)
        if tts_service:
            st.session_state.tts_service = tts_service  # Store in session state
            st.success("✅ IBM Watson TTS service initialized successfully!")

            # Retrieve available voices
            voices = get_voices(tts_service)
            if voices:
                st.session_state.voices = voices
            else:
                st.error("❌ Could not retrieve voices from IBM Watson TTS service.")
        else:
            st.error("❌ Failed to initialize IBM Watson TTS service.")
    else:
        st.info("ℹ️ Please enter your IBM Watson TTS credentials.")

    # Binaural Beat Settings
    st.subheader("🎛️ Binaural Beat Settings")
    base_freq = st.selectbox("🔊 Base Frequency (Hz):", [100, 200, 300, 400, 440, 500, 600], index=4, help="Select the base frequency for binaural beats.")
    beat_freq = st.selectbox("🎶 Beat Frequency (Hz):", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 30, 40], index=1, help="Select the beat frequency for binaural beats.")
    binaural_volume = st.slider(
        "🔉 Binaural Beat Volume (dB):",
        min_value=-30,
        max_value=0,
        value=-15,
        step=1,
        help="Adjust the volume of the binaural beats. Lower values make the beats quieter."
    )

    # Store settings in session_state
    st.session_state.base_freq = base_freq
    st.session_state.beat_freq = beat_freq
    st.session_state.binaural_volume = binaural_volume

# -----------------------------
# Preview Voice Tab
# -----------------------------
with tab_preview:
    st.header("🎙️ 4. Preview Selected Voice")

    if st.session_state.voices:
        # Let the user select a voice
        voice_options = [desc for _, desc in st.session_state.voices]
        selected_voice_desc = st.selectbox("Select a Voice", voice_options)
        # Get the voice ID corresponding to the selected description
        selected_voice_id = next(voice_id for voice_id, desc in st.session_state.voices if desc == selected_voice_desc)
        st.session_state.selected_voice_id = selected_voice_id  # Store in session state

        if st.button("🔊 Preview Voice"):
            try:
                sample_text = "This is a voice preview."
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_preview_file:
                    tts_wav_file = ibm_watson_tts(st.session_state.tts_service, sample_text, selected_voice_id, temp_preview_file.name)
                    if tts_wav_file:
                        st.audio(temp_preview_file.name, format="audio/wav")
                    else:
                        st.error("❌ Failed to generate voice preview.")
                os.unlink(temp_preview_file.name)  # Clean up temporary file
            except Exception as e:
                st.error(f"An error occurred while previewing the voice: {str(e)}")
    else:
        st.info("ℹ️ Please initialize the IBM Watson TTS service and select a voice in the **Settings** tab.")

# -----------------------------
# Convert Tab
# -----------------------------
with tab_convert:
    st.header("🔄 5. Convert Audio with Binaural Beats and Subliminal Affirmations")

    # Ensure tts_service and selected_voice_id are initialized
    if 'tts_service' not in st.session_state or st.session_state.tts_service is None:
        st.error("⚠️ Please initialize the IBM Watson TTS service in the **Settings** tab.")
    elif 'selected_voice_id' not in st.session_state or st.session_state.selected_voice_id is None:
        st.error("⚠️ Please select a voice in the **Preview Voice** tab.")
    else:
        # Option to select between uploaded main WAV or looped files
        convert_source = st.radio("📁 Select Audio Source:", ("Upload a New WAV File", "Use a Looped WAV File"), help="Choose whether to upload a new WAV file or use an existing looped file.")

        if convert_source == "Upload a New WAV File":
            main_wav = st.file_uploader("🎧 Choose a WAV file", type=["wav"], key="main_wav_convert", help="Upload the main audio file you want to enhance.")
        else:
            if st.session_state.looped_files:
                looped_options = list(st.session_state.looped_files.keys())
                selected_loop = st.selectbox("🗂️ Select a Looped WAV File:", looped_options, help="Choose a previously looped WAV file to process.")
                main_wav = None  # No new upload
            else:
                st.info("🌀 No looped files available. Please create a looped WAV file in the **🌀 Looper** tab.")
                main_wav = None

        # File upload for subliminal text file
        st.header("📄 6. Upload Subliminal Affirmations Text File (Optional)")
        uploaded_text = st.file_uploader("📄 Choose a Text file with subliminal affirmations", type=["txt"], key="subliminal_text_convert", help="Upload a text file containing subliminal messages to embed into your audio.")

        # Display uploaded text file name
        if uploaded_text:
            st.success(f"✅ Loaded: {uploaded_text.name}")
        else:
            st.info("ℹ️ No subliminal text file uploaded.")

        if st.button("▶️ Convert Audio"):
            if convert_source == "Upload a New WAV File" and not main_wav:
                st.error("⚠️ Please upload a main WAV file to process.")
            elif convert_source == "Use a Looped WAV File" and not st.session_state.looped_files:
                st.error("⚠️ No looped files available. Please create a looped WAV file in the **🌀 Looper** tab.")
            else:
                with st.spinner("🔄 Processing audio..."):
                    try:
                        # Determine the source audio
                        if convert_source == "Upload a New WAV File":
                            # Save uploaded WAV to a temporary file
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_input_file:
                                temp_input_file.write(main_wav.read())
                                temp_input_file_path = temp_input_file.name
                        else:
                            # Use selected looped file
                            looped_data = st.session_state.looped_files[selected_loop]
                            temp_input_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                            temp_input_file.write(looped_data)
                            temp_input_file_path = temp_input_file.name
                            temp_input_file.close()

                        # Process audio
                        output_audio_path = process_audio(
                            input_wav=temp_input_file_path,
                            subliminal_text=uploaded_text,  # Pass UploadedFile object or None
                            base_freq=st.session_state.base_freq,
                            beat_freq=st.session_state.beat_freq,
                            selected_voice=st.session_state.selected_voice_id,
                            tts_service=st.session_state.tts_service,
                            binaural_volume_db=st.session_state.binaural_volume  # Pass volume adjustment
                        )

                        # Clean up input file
                        os.unlink(temp_input_file_path)

                        if output_audio_path:
                            # Read the output audio for download
                            with open(output_audio_path, "rb") as out_f:
                                out_bytes = out_f.read()

                            st.success("✅ Audio processing complete!")

                            # Display processed audio waveform
                            processed_audio = AudioSegment.from_wav(output_audio_path)
                            st.subheader("🎵 Processed Audio Waveform")
                            plot_waveform(processed_audio, title="Processed Audio Waveform")

                            # Play processed audio
                            st.audio(output_audio_path, format="audio/wav")

                            # Download button
                            st.download_button(
                                label="💾 Download Processed Audio",
                                data=out_bytes,
                                file_name="processed_audio.wav",
                                mime="audio/wav"
                            )

                            # Clean up output file
                            os.unlink(output_audio_path)
                    except Exception as e:
                        st.error(f"An error occurred during processing: {str(e)}")

# -----------------------------
# Footer with Quit Button
# -----------------------------
st.markdown("""
---
<p style='text-align: center; color: grey;'>
    Developed by Thomas Lane | 
    https://github.com/tlanej | 
    © 2024 All Rights Reserved
</p>
""", unsafe_allow_html=True)

# -----------------------------
# Quit Button
# -----------------------------
if st.button("❌ Quit"):
    st.warning("⚠️ Exiting the app...")
    sys.exit()
