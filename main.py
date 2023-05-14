import os
import subprocess

from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
from anki.hooks import addHook
from aqt import editor

def get_key():
    conf = mw.addonManager.getConfig(__name__)
    return conf.get("hotkey", "") if conf else ""

def format_key(k):
    return QKeySequence(k).toString(QKeySequence.NativeText)

def anki_vosk(editor):
    sent_audio_field = "SentAudio"
    sent_target_field = "SentTarget"

    # Get the content of the 'SentAudio' field
    sent_audio_content = editor.note[sent_audio_field]

    # Call the ankivosk.py script with the 'SentAudio' field content as an argument
    ankivosk_path = os.path.join(os.path.dirname(__file__), "ankivosk.py")
    result = subprocess.check_output(["python", ankivosk_path, sent_audio_content])

    # Set the 'SentTarget' field content with the result
    editor.note[sent_target_field] = result.decode("utf-8")

    # Update the editor UI with the new content
    editor.loadNote()

def setupEditorButtonsFilter(buttons, editor):
    key = get_key()
    b = editor.addButton(
            os.path.join(os.path.dirname(__file__), "ankivosk.png"),
            "ankivosk_button",
            anki_vosk,
            tip=f"AnkiVosk ({format_key(key)})",
            keys=key
        )
    buttons.append(b)
    return buttons

addHook("setupEditorButtons", setupEditorButtonsFilter)

