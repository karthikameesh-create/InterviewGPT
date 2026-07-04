import os
import tempfile

from google import genai
from google.genai import types
from streamlit_mic_recorder import mic_recorder


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def speech_to_text():
    """
    Records audio from the browser and returns the transcript using Gemini.
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

        # Save browser recording
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".webm"
        ) as f:

            f.write(audio["bytes"])
            audio_path = f.name

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "Transcribe this audio. Return ONLY the spoken text. Do not add explanations.",
                types.Part.from_bytes(
                    data=audio_bytes,
                    mime_type="audio/webm"
                )
            ]
        )

        os.remove(audio_path)

        if response.text:
            return response.text.strip()

        return "ERROR: No transcript returned."

    except Exception as e:
        return f"ERROR: {e}"