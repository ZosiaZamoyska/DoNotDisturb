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
    match emotion:
        case Emotion.UNKNOWN:
            return "❓"
        case Emotion.EXCITED:
            return "🤩"
        case Emotion.DELIGHTED:
            return "😁"
        case Emotion.HAPPY:
            return "😊"
        case Emotion.PLEASED:
            return "🙂"
        case Emotion.RELAXED:
            return "😌"
        case Emotion.SLEEPY:
            return "😴"
        case Emotion.TENSE:
            return "😤"
        case Emotion.ANGRY:
            return "😡"
        case Emotion.FRUSTRATED:
            return "😫"
        case Emotion.DEPRESSED:
            return "😞"
        case Emotion.BORED:
            return "😒"
        case Emotion.TIRED:
            return "😪"
