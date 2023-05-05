from enum import Enum

class Emotion(Enum):
    Unknown = 0
    Excited = 1
    Delighted = 2
    Happy = 3
    Pleased = 4
    Relaxed = 5
    Sleepy = 6
    Tense = 7
    Angry = 8
    Frustrated = 9
    Depressed = 10
    Bored = 11
    Tired = 12

def calc_emotion(valence: int, arousal: int) -> Emotion:
    if valence > 0:
        if arousal == 3:
            return Emotion.Excited
        elif arousal == 2:
            return Emotion.Delighted
        elif arousal == 1:
            return Emotion.Happy
        elif arousal == -1:
            return Emotion.Pleased
        elif arousal == -2:
            return Emotion.Relaxed
        elif arousal == -3:
            return Emotion.Sleepy
    elif valence < 0:
        if arousal == 3:
            return Emotion.Tense
        elif arousal == 2:
            return Emotion.Angry
        elif arousal == 1:
            return Emotion.Frustrated
        elif arousal == -1:
            return Emotion.Depressed
        elif arousal == -2:
            return Emotion.Bored
        elif arousal == -3:
            return Emotion.Tired

    return Emotion.Unknown

def get_emoji_from_emotion(emotion: Emotion) -> str:
    match emotion:
        case Emotion.Unknown:
            return "❓"
        case Emotion.Excited:
            return "🤩"
        case Emotion.Delighted:
            return "😁"
        case Emotion.Happy:
            return "😊"
        case Emotion.Pleased:
            return "🙂"
        case Emotion.Relaxed:
            return "😌"
        case Emotion.Sleepy:
            return "😴"
        case Emotion.Tense:
            return "😤"
        case Emotion.Angry:
            return "😡"
        case Emotion.Frustrated:
            return "😫"
        case Emotion.Depressed:
            return "😞"
        case Emotion.Bored:
            return "😒"
        case Emotion.Tired:
            return "😪"
