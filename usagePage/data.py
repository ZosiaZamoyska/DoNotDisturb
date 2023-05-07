from usagePage.emotion import Emotion
from usagePage.enum import UsageTimeGranularity


# TODO: replace with real data processing
class UsageData:
    @staticmethod
    def get_all_app_names() -> list[str]:
        return ["Instagram", "GMail"]

    @staticmethod
    def get_all_notification_count(time_granularity: UsageTimeGranularity) -> int:
        if time_granularity == UsageTimeGranularity.WEEK:
            return 431
        elif time_granularity == UsageTimeGranularity.MONTH:
            return 2564

    @staticmethod
    def get_app_notification_count(
        app_name: str, time_granularity: UsageTimeGranularity
    ) -> int:
        if (app_name, time_granularity) == ("Instagram", UsageTimeGranularity.WEEK):
            return 12
        elif (app_name, time_granularity) ==  ("Instagram", UsageTimeGranularity.MONTH):
            return 54
        elif (app_name, time_granularity) == ("GMail", UsageTimeGranularity.WEEK):
            return 124
        elif (app_name, time_granularity) ==  ("GMail", UsageTimeGranularity.MONTH):
            return 599

        return None

    @staticmethod
    def get_all_pick_up_count(time_granularity: UsageTimeGranularity) -> int:
        if time_granularity == UsageTimeGranularity.WEEK:
            return 42
        elif time_granularity == UsageTimeGranularity.MONTH:
            return 235

    @staticmethod
    def get_pick_up_count(app_name: str, time_granularity: UsageTimeGranularity) -> int:
        if (app_name, time_granularity) == ("Instagram", UsageTimeGranularity.WEEK):
            return 2
        elif (app_name, time_granularity) == ("Instagram", UsageTimeGranularity.MONTH):
            return 14
        elif (app_name, time_granularity) == ("GMail", UsageTimeGranularity.WEEK):
            return 12
        elif (app_name, time_granularity) == ("GMail", UsageTimeGranularity.MONTH):
            return 99
        
        return None

    @staticmethod
    def get_all_unlock_count(time_granularity: UsageTimeGranularity) -> int:
        if time_granularity == UsageTimeGranularity.WEEK:
            return 12
        elif time_granularity == UsageTimeGranularity.MONTH:
            return 99

    @staticmethod
    def get_unlock_count(app_name: str, time_granularity: UsageTimeGranularity) -> int:
        if (app_name, time_granularity) == ("Instagram", UsageTimeGranularity.WEEK):
            return 1
        elif (app_name, time_granularity) == ("Instagram", UsageTimeGranularity.MONTH):
            return 10
        elif (app_name, time_granularity) == ("GMail", UsageTimeGranularity.WEEK):
            return 0
        elif (app_name, time_granularity) == ("GMail", UsageTimeGranularity.MONTH):
            return 6

        return None

    @staticmethod
    def get_emotions(
        app_name: str, time_granularity: UsageTimeGranularity) -> list:
        if (app_name, time_granularity) == ("Instagram", UsageTimeGranularity.WEEK):
            return [Emotion.HAPPY, Emotion.DELIGHTED, Emotion.ANGRY]
        elif (app_name, time_granularity) ==  ("Instagram", UsageTimeGranularity.MONTH):
            return [Emotion.HAPPY, Emotion.DEPRESSED, Emotion.ANGRY]
        elif (app_name, time_granularity) ==  ("GMail", UsageTimeGranularity.WEEK):
            return [Emotion.BORED, Emotion.SLEEPY, Emotion.TIRED]
        elif (app_name, time_granularity) == ("GMail", UsageTimeGranularity.MONTH):
            return [Emotion.BORED, Emotion.SLEEPY, Emotion.RELAXED]

        return [Emotion.UNKNOWN, Emotion.UNKNOWN, Emotion.UNKNOWN]
