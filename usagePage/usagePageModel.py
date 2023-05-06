from usagePage.data import UsageData
from usagePage.enum import UsageTimeGranularity


class UsagePageModel:
    def __init__(self):
        self._current_app_name = "Instagram"
        self._time_granularity = UsageTimeGranularity.WEEK
        self._view = None

        self.update()

    def get_view(self):
        return self._view

    def set_view(self, view):
        self._view = view

    def get_current_app_name(self):
        return self._current_app_name

    def set_current_app_name(self, app_name):
        self._current_app_name = app_name
        self.update()

    def get_time_granularity(self):
        return self._time_granularity

    def set_time_granularity(self, time_granularity: UsageTimeGranularity):
        self._time_granularity = time_granularity
        self.update()

    def get_all_notification_count(self):
        return self._all_notification_count

    def get_notification_count(self):
        return self._app_notification_count

    def get_pickup_count(self):
        return self._app_pickup_count

    def get_unlock_count(self):
        return self._app_unlock_count

    def get_emotion_emojis(self):
        return self._app_emotion_emojis

    def update(self):
        self._all_notification_count = UsageData.get_all_notification_count(
            self.get_time_granularity()
        )
        self._app_notification_count = UsageData.get_app_notification_count(
            self.get_current_app_name(), self.get_time_granularity()
        )
        self._app_pickup_count = UsageData.get_pick_up_count(
            self.get_current_app_name(), self.get_time_granularity()
        )
        self._app_unlock_count = UsageData.get_unlock_count(
            self.get_current_app_name(), self.get_time_granularity()
        )
        self._app_emotion_emojis = UsageData.get_emotion_emojis(
            self.get_current_app_name(), self.get_time_granularity()
        )

        if self.get_view():
            self.get_view().update()
