from streamlit_mic_recorder import mic_recorder
import tempfile
import speech_recognition as sr


def speech_to_text():
    """
    Records audio in the user's browser and converts it to text.
    Returns:
        str | None
    """

    audio = mic_recorder(
        start_prompt="🎙 Start Recording",
        stop_prompt="⏹ Stop Recording",
        just_once=True,
        use_container_width=True,
        key="browser_mic"
    )

    if audio is None:
        return None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio["bytes"])
            audio_path = f.name

        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_path) as source:
            recorded = recognizer.record(source)

        return recognizer.recognize_google(recorded)

    except Exception as e:
        return f"ERROR: {e}"