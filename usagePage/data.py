from usagePage.emotion import Emotion
from usagePage.enum import UsageTimeGranularity


# TODO: replace with real data processing
class UsageData:
    @staticmethod
    def get_all_app_names() -> list[str]:
        return ["Instagram", "GMail"]

    @staticmethod
    def get_all_notification_count(time_granularity: UsageTimeGranularity) -> int:
        match time_granularity:
            case UsageTimeGranularity.WEEK:
                return 431
            case UsageTimeGranularity.MONTH:
                return 2564

    @staticmethod
    def get_app_notification_count(
        app_name: str, time_granularity: UsageTimeGranularity
    ) -> int:
        match (app_name, time_granularity):
            case ("Instagram", UsageTimeGranularity.WEEK):
                return 12
            case ("Instagram", UsageTimeGranularity.MONTH):
                return 54
            case ("GMail", UsageTimeGranularity.WEEK):
                return 124
            case ("GMail", UsageTimeGranularity.MONTH):
                return 599

        return None

    @staticmethod
    def get_all_pick_up_count(time_granularity: UsageTimeGranularity) -> int:
        match time_granularity:
            case UsageTimeGranularity.WEEK:
                return 42
            case UsageTimeGranularity.MONTH:
                return 235

    @staticmethod
    def get_pick_up_count(app_name: str, time_granularity: UsageTimeGranularity) -> int:
        match (app_name, time_granularity):
            case ("Instagram", UsageTimeGranularity.WEEK):
                return 2
            case ("Instagram", UsageTimeGranularity.MONTH):
                return 14
            case ("GMail", UsageTimeGranularity.WEEK):
                return 12
            case ("GMail", UsageTimeGranularity.MONTH):
                return 99

        return None

    @staticmethod
    def get_all_unlock_count(time_granularity: UsageTimeGranularity) -> int:
        match time_granularity:
            case UsageTimeGranularity.WEEK:
                return 12
            case UsageTimeGranularity.MONTH:
                return 99

    @staticmethod
    def get_unlock_count(app_name: str, time_granularity: UsageTimeGranularity) -> int:
        match (app_name, time_granularity):
            case ("Instagram", UsageTimeGranularity.WEEK):
                return 1
            case ("Instagram", UsageTimeGranularity.MONTH):
                return 10
            case ("GMail", UsageTimeGranularity.WEEK):
                return 0
            case ("GMail", UsageTimeGranularity.MONTH):
                return 6

        return None

    @staticmethod
    def get_emotions(
        app_name: str, time_granularity: UsageTimeGranularity
    ) -> list[str]:
        match (app_name, time_granularity):
            case ("Instagram", UsageTimeGranularity.WEEK):
                return [Emotion.HAPPY, Emotion.DELIGHTED, Emotion.ANGRY]

            case ("Instagram", UsageTimeGranularity.MONTH):
                return [Emotion.HAPPY, Emotion.DEPRESSED, Emotion.ANGRY]

            case ("GMail", UsageTimeGranularity.WEEK):
                return [Emotion.BORED, Emotion.SLEEPY, Emotion.TIRED]

            case ("GMail", UsageTimeGranularity.MONTH):
                return [Emotion.BORED, Emotion.SLEEPY, Emotion.RELAXED]

        return [Emotion.UNKNOWN, Emotion.UNKNOWN, Emotion.UNKNOWN]
