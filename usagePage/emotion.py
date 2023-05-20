from enum import Enum
import sys

class Emotion(Enum):
    UNKNOWN = "<<Unknown>>"
    EXCITED = "Excited"
    DELIGHTED = "Delighted"
    HAPPY = "Happy"
    PLEASED = "Pleased"
    RELAXED = "Relaxed"
    SLEEPY = "Sleepy"
    TENSE = "Tense"
    ANGRY = "Angry"
    FRUSTRATED = "Frustrated"
    DEPRESSED = "Depressed"
    BORED = "Bored"
    TIRED = "Tired"


def calc_emotion(valence: int, arousal: int) -> Emotion:
    if valence > 0:
        if arousal == 3:
            return Emotion.EXCITED
        elif arousal == 2:
            return Emotion.DELIGHTED
        elif arousal == 1:
            return Emotion.HAPPY
        elif arousal == -1:
            return Emotion.PLEASED
        elif arousal == -2:
            return Emotion.RELAXED
        elif arousal == -3:
            return Emotion.SLEEPY
    elif valence < 0:
        if arousal == 3:
            return Emotion.TENSE
        elif arousal == 2:
            return Emotion.ANGRY
        elif arousal == 1:
            return Emotion.FRUSTRATED
        elif arousal == -1:
            return Emotion.DEPRESSED
        elif arousal == -2:
            return Emotion.BORED
        elif arousal == -3:
            return Emotion.TIRED

    return Emotion.UNKNOWN


def to_emoji(emotion: Emotion) -> str:
    if emotion == Emotion.UNKNOWN:
            return "❓"
    elif emotion == Emotion.EXCITED:
            return "🤩"
    elif emotion == Emotion.DELIGHTED:
            return "😁"
    elif emotion == Emotion.HAPPY:
            return "😊"
    elif emotion == Emotion.PLEASED:
            return "🙂"
    elif emotion == Emotion.RELAXED:
            return "😌"
    elif emotion == Emotion.SLEEPY:
            return "😴"
    elif emotion == Emotion.TENSE:
            return "😤"
    elif emotion == Emotion.ANGRY:
            return "😡"
    elif emotion == Emotion.FRUSTRATED:
            return "😫"
    elif emotion == Emotion.DEPRESSED:
            return "😞"
    elif emotion == Emotion.BORED:
            return "😒"
    elif emotion == Emotion.TIRED:
            return "😪"
