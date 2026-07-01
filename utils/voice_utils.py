import speech_recognition as sr


def speech_to_text():

    try:

        recognizer = sr.Recognizer()

        with sr.Microphone() as source:

            print("Listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                timeout=10
            )

        text = recognizer.recognize_google(
            audio
        )

        return text

    except Exception as e:

        return f"ERROR: {str(e)}"