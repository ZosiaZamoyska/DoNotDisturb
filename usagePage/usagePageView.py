from dash import html, dcc
from usagePage.data import UsageData
from usagePage.emotion import to_emoji
import pandas as pd
import plotly.express as px
import matplotlib
import statistics
import datetime

class UsagePageView:
    def get_model(self):
        return self._model

    def set_model(self, model):
        self._model = model
        self._html_component = self._build_html_component()

    def get_html_component(self) -> html.Div:
        return self._html_component

    def _build_html_component(self) -> html.Div:
        controller_widget = self._build_controller()

        review = self._build_review_widget()
        notification_widget = self._build_notification_widget()
        pickup_widget = self._build_pickup_widget()
        unlock_widget = self._build_unlock_widget()
        emotion_emojis_widget = self._build_emotion_emojis_widget()

        usage_stat_container = self._wrap_to_card(
            "stat-container",
            [
                controller_widget,
                review,
                html.Div(
                    className="d-flex justify-content-center",
                    children=html.Img(
                        id="scaleImg",
                        className="inline-block",
                        src="assets/scale.png",
                        width="200",
                    ),
                    style={"margin-bottom": "2em"},
                ),
                notification_widget,
                pickup_widget,
                unlock_widget,
                emotion_emojis_widget,
            ],
        )

        page = html.Div(
            id="stat-page-container",
            className="col-lg-6",
            children=[usage_stat_container],
        )

        return page

    def _build_controller(self):
        div = html.Div(
            id="controller-container",
            children=[
                html.H1("Usage Statistics", className="card-title"),
                dcc.Dropdown(
                    id="app-dropdown",
                    options=UsageData.get_all_app_names(),
                    value=self.get_model().get_current_app_name(),
                ),
                dcc.Dropdown(
                    id="time-granularity-dropdown",
                    options=["week", "month"],
                    value=self.get_model().get_time_granularity().value,
                ),
            ],
        )

        return div

    def _build_review_widget(self):
        schedule = pd.read_csv("schedule.csv")
        schedule['Start'] = pd.to_datetime(schedule[['From Hour', 'From Min']].astype(str).apply(':'.join, axis=1) + ':00', format='%H:%M:%S').dt.time
        schedule['End'] = pd.to_datetime(schedule[['To Hour', 'To Min']].astype(str).apply(':'.join, axis=1) + ':00', format='%H:%M:%S').dt.time
        # for the first day 
        phoneUsage_day1 = pd.read_csv("review_entries_day1.csv")
        phoneUsage_day1['startTime'] = pd.to_datetime(phoneUsage_day1['startTime']).dt.time
        phoneUsage_day1['endTime'] = pd.to_datetime(phoneUsage_day1['endTime']).dt.time
        phoneUsage_day1['timestamp'] = pd.to_datetime(phoneUsage_day1['timestamp'], unit='ms').dt.date
        work=["Samsung Notes"]
        leisure = ['전화', '메시지', 'Messenger', 'Instagram', 'YouTube', 'AfreecaTV', 'Facebook', '카카오톡']
        ratings = []
        final_rating = []
        date = phoneUsage_day1['timestamp'].iloc[0]
        date = date.strftime('%Y-%m-%d')
        schedule_day1 = schedule[schedule['Date'] == date]
        for index_s, row_s in schedule_day1.iterrows():
            for index_p, row_p in phoneUsage_day1.iterrows():
                if row_s["Start"] < row_p["endTime"] < row_s["End"]:
                    if row_s["Category"] == "Sleep":
                        rating = 0
                    elif row_s["Category"] == "Work":
                        if row_p["name"] in work:
                            rating = 1
                        elif row_p["name"] in leisure:
                            rating = 0.33
                        else:
                            rating = 0.66
                    elif row_s["Category"] == "Leisure":
                        if row_p["name"] in leisure:
                            rating = 1
                        elif row_p["name"] in work:
                            rating = 0.33
                        else:
                            rating = 0.66
                    ratings.append(rating)
            if len(ratings) > 0:
                if statistics.mode(ratings) == 1:
                    final_rating.append(1)
                elif statistics.mode(ratings) == 0.66:
                    final_rating.append(0.66)
                elif statistics.mode(ratings) == 0.33:
                    final_rating.append(0.33)
                elif statistics.mode(ratings) == 0:
                    final_rating.append(0)
            else:
                final_rating.append(1)
            ratings = []

        schedule_day1["Ratings"] = final_rating

        # for the second day 
        phoneUsage_day2 = pd.read_csv("review_entries_day2.csv")
        phoneUsage_day2['startTime'] = pd.to_datetime(phoneUsage_day2['startTime']).dt.time
        phoneUsage_day2['endTime'] = pd.to_datetime(phoneUsage_day2['endTime']).dt.time
        phoneUsage_day2['timestamp'] = pd.to_datetime(phoneUsage_day2['timestamp'], unit='ms').dt.date
        work=["Samsung Notes"]
        leisure = ['전화', '메시지', 'Messenger', 'Instagram', 'YouTube', 'AfreecaTV', 'Facebook', '카카오톡']
        ratings = []
        final_rating = []
        date = phoneUsage_day2['timestamp'].iloc[0]
        date = date.strftime('%Y-%m-%d')
        schedule_day2 = schedule[schedule['Date'] == date]
        for index_s, row_s in schedule_day2.iterrows():
            for index_p, row_p in phoneUsage_day2.iterrows():
                if row_s["Start"] < row_p["endTime"] < row_s["End"]:
                    if row_s["Category"] == "Sleep":
                        rating = 0
                    elif row_s["Category"] == "Work":
                        if row_p["name"] in work:
                            rating = 1
                        elif row_p["name"] in leisure:
                            rating = 0.33
                        else:
                            rating = 0.66
                    elif row_s["Category"] == "Leisure":
                        if row_p["name"] in leisure:
                            rating = 1
                        elif row_p["name"] in work:
                            rating = 0.33
                        else:
                            rating = 0.66
                    ratings.append(rating)
            if len(ratings) > 0:
                if statistics.mode(ratings) == 1:
                    final_rating.append(1)
                elif statistics.mode(ratings) == 0.66:
                    final_rating.append(0.66)
                elif statistics.mode(ratings) == 0.33:
                    final_rating.append(0.33)
                elif statistics.mode(ratings) == 0:
                    final_rating.append(0)
            else:
                final_rating.append(1)
            ratings = []

        schedule_day2["Ratings"] = final_rating

        # for day 3
        phoneUsage_day3 = pd.read_csv("review_entries_day3.csv")
        phoneUsage_day3['startTime'] = pd.to_datetime(phoneUsage_day3['startTime']).dt.time
        phoneUsage_day3['endTime'] = pd.to_datetime(phoneUsage_day3['endTime']).dt.time
        phoneUsage_day3['timestamp'] = pd.to_datetime(phoneUsage_day3['timestamp'], unit='ms').dt.date
        work=["Samsung Notes"]
        leisure = ['전화', '메시지', 'Messenger', 'Instagram', 'YouTube', 'AfreecaTV', 'Facebook', '카카오톡']
        ratings = []
        final_rating = []
        date = phoneUsage_day3['timestamp'].iloc[0]
        date = date.strftime('%Y-%m-%d')
        schedule_day3 = schedule[schedule['Date'] == date]
        for index_s, row_s in schedule_day3.iterrows():
            for index_p, row_p in phoneUsage_day3.iterrows():
                if row_s["Start"] < row_p["endTime"] < row_s["End"]:
                    if row_s["Category"] == "Sleep":
                        rating = 0
                    elif row_s["Category"] == "Work":
                        if row_p["name"] in work:
                            rating = 1
                        elif row_p["name"] in leisure:
                            rating = 0.33
                        else:
                            rating = 0.66
                    elif row_s["Category"] == "Leisure":
                        if row_p["name"] in leisure:
                            rating = 1
                        elif row_p["name"] in work:
                            rating = 0.33
                        else:
                            rating = 0.66
                    ratings.append(rating)
            if len(ratings) > 0:
                if statistics.mode(ratings) == 1:
                    final_rating.append(1)
                elif statistics.mode(ratings) == 0.66:
                    final_rating.append(0.66)
                elif statistics.mode(ratings) == 0.33:
                    final_rating.append(0.33)
                elif statistics.mode(ratings) == 0:
                    final_rating.append(0)
            else:
                final_rating.append(1)
            ratings = []

        schedule_day3["Ratings"] = final_rating

        # for day 4
        phoneUsage_day4 = pd.read_csv("review_entries_day4.csv")
        phoneUsage_day4['startTime'] = pd.to_datetime(phoneUsage_day4['startTime']).dt.time
        phoneUsage_day4['endTime'] = pd.to_datetime(phoneUsage_day4['endTime']).dt.time
        phoneUsage_day4['timestamp'] = pd.to_datetime(phoneUsage_day4['timestamp'], unit='ms').dt.date
        work=["Samsung Notes"]
        leisure = ['전화', '메시지', 'Messenger', 'Instagram', 'YouTube', 'AfreecaTV', 'Facebook', '카카오톡']
        ratings = []
        final_rating = []
        date = phoneUsage_day4['timestamp'].iloc[0]
        date = date.strftime('%Y-%m-%d')
        schedule_day4 = schedule[schedule['Date'] == date]
        for index_s, row_s in schedule_day4.iterrows():
            for index_p, row_p in phoneUsage_day4.iterrows():
                if row_s["Start"] < row_p["endTime"] < row_s["End"]:
                    if row_s["Category"] == "Sleep":
                        rating = 0
                    elif row_s["Category"] == "Work":
                        if row_p["name"] in work:
                            rating = 1
                        elif row_p["name"] in leisure:
                            rating = 0.33
                        else:
                            rating = 0.66
                    elif row_s["Category"] == "Leisure":
                        if row_p["name"] in leisure:
                            rating = 1
                        elif row_p["name"] in work:
                            rating = 0.33
                        else:
                            rating = 0.66
                    ratings.append(rating)
            if len(ratings) > 0:
                if statistics.mode(ratings) == 1:
                    final_rating.append(1)
                elif statistics.mode(ratings) == 0.66:
                    final_rating.append(0.66)
                elif statistics.mode(ratings) == 0.33:
                    final_rating.append(0.33)
                elif statistics.mode(ratings) == 0:
                    final_rating.append(0)
            else:
                final_rating.append(1)
            ratings = []

        schedule_day4["Ratings"] = final_rating

        # for day 5
        phoneUsage_day5 = pd.read_csv("review_entries_day5.csv")
        phoneUsage_day5['startTime'] = pd.to_datetime(phoneUsage_day5['startTime']).dt.time
        phoneUsage_day5['endTime'] = pd.to_datetime(phoneUsage_day5['endTime']).dt.time
        phoneUsage_day5['timestamp'] = pd.to_datetime(phoneUsage_day5['timestamp'], unit='ms').dt.date
        work=["Samsung Notes"]
        leisure = ['전화', '메시지', 'Messenger', 'Instagram', 'YouTube', 'AfreecaTV', 'Facebook', '카카오톡']
        ratings = []
        final_rating = []
        date = phoneUsage_day5['timestamp'].iloc[0]
        date = date.strftime('%Y-%m-%d')
        schedule_day5 = schedule[schedule['Date'] == date]
        for index_s, row_s in schedule_day5.iterrows():
            for index_p, row_p in phoneUsage_day5.iterrows():
                if row_s["Start"] < row_p["endTime"] < row_s["End"]:
                    if row_s["Category"] == "Sleep":
                        rating = 0
                    elif row_s["Category"] == "Work":
                        if row_p["name"] in work:
                            rating = 1
                        elif row_p["name"] in leisure:
                            rating = 0.33
                        else:
                            rating = 0.66
                    elif row_s["Category"] == "Leisure":
                        if row_p["name"] in leisure:
                            rating = 1
                        elif row_p["name"] in work:
                            rating = 0.33
                        else:
                            rating = 0.66
                    ratings.append(rating)
            if len(ratings) > 0:
                if statistics.mode(ratings) == 1:
                    final_rating.append(1)
                elif statistics.mode(ratings) == 0.66:
                    final_rating.append(0.66)
                elif statistics.mode(ratings) == 0.33:
                    final_rating.append(0.33)
                elif statistics.mode(ratings) == 0:
                    final_rating.append(0)
            else:
                final_rating.append(1)
            ratings = []

        schedule_day5["Ratings"] = final_rating

        # for day 6
        phoneUsage_day6 = pd.read_csv("review_entries_day6.csv")
        phoneUsage_day6['startTime'] = pd.to_datetime(phoneUsage_day6['startTime']).dt.time
        phoneUsage_day6['endTime'] = pd.to_datetime(phoneUsage_day6['endTime']).dt.time
        phoneUsage_day6['timestamp'] = pd.to_datetime(phoneUsage_day6['timestamp'], unit='ms').dt.date
        work=["Samsung Notes"]
        leisure = ['전화', '메시지', 'Messenger', 'Instagram', 'YouTube', 'AfreecaTV', 'Facebook', '카카오톡']
        ratings = []
        final_rating = []
        date = phoneUsage_day6['timestamp'].iloc[0]
        date = date.strftime('%Y-%m-%d')
        schedule_day6 = schedule[schedule['Date'] == date]
        for index_s, row_s in schedule_day6.iterrows():
            for index_p, row_p in phoneUsage_day6.iterrows():
                if row_s["Start"] < row_p["endTime"] < row_s["End"]:
                    if row_s["Category"] == "Sleep":
                        rating = 0
                    elif row_s["Category"] == "Work":
                        if row_p["name"] in work:
                            rating = 1
                        elif row_p["name"] in leisure:
                            rating = 0.33
                        else:
                            rating = 0.66
                    elif row_s["Category"] == "Leisure":
                        if row_p["name"] in leisure:
                            rating = 1
                        elif row_p["name"] in work:
                            rating = 0.33
                        else:
                            rating = 0.66
                    ratings.append(rating)
            if len(ratings) > 0:
                if statistics.mode(ratings) == 1:
                    final_rating.append(1)
                elif statistics.mode(ratings) == 0.66:
                    final_rating.append(0.66)
                elif statistics.mode(ratings) == 0.33:
                    final_rating.append(0.33)
                elif statistics.mode(ratings) == 0:
                    final_rating.append(0)
            else:
                final_rating.append(1)
            ratings = []

        schedule_day6["Ratings"] = final_rating

        # for day 7
        phoneUsage_day7 = pd.read_csv("review_entries_day7.csv")
        phoneUsage_day7['startTime'] = pd.to_datetime(phoneUsage_day7['startTime']).dt.time
        phoneUsage_day7['endTime'] = pd.to_datetime(phoneUsage_day7['endTime']).dt.time
        phoneUsage_day7['timestamp'] = pd.to_datetime(phoneUsage_day7['timestamp'], unit='ms').dt.date
        work=["Samsung Notes"]
        leisure = ['전화', '메시지', 'Messenger', 'Instagram', 'YouTube', 'AfreecaTV', 'Facebook', '카카오톡']
        ratings = []
        final_rating = []
        date = phoneUsage_day7['timestamp'].iloc[0]
        date = date.strftime('%Y-%m-%d')
        schedule_day7 = schedule[schedule['Date'] == date]
        for index_s, row_s in schedule_day7.iterrows():
            for index_p, row_p in phoneUsage_day7.iterrows():
                if row_s["Start"] < row_p["endTime"] < row_s["End"]:
                    if row_s["Category"] == "Sleep":
                        rating = 0
                    elif row_s["Category"] == "Work":
                        if row_p["name"] in work:
                            rating = 1
                        elif row_p["name"] in leisure:
                            rating = 0.33
                        else:
                            rating = 0.66
                    elif row_s["Category"] == "Leisure":
                        if row_p["name"] in leisure:
                            rating = 1
                        elif row_p["name"] in work:
                            rating = 0.33
                        else:
                            rating = 0.66
                    ratings.append(rating)
            if len(ratings) > 0:
                if statistics.mode(ratings) == 1:
                    final_rating.append(1)
                elif statistics.mode(ratings) == 0.66:
                    final_rating.append(0.66)
                elif statistics.mode(ratings) == 0.33:
                    final_rating.append(0.33)
                elif statistics.mode(ratings) == 0:
                    final_rating.append(0)
            else:
                final_rating.append(1)
            ratings = []

        schedule_day7["Ratings"] = final_rating
        combined_df = pd.concat([schedule_day1, schedule_day2, schedule_day3, schedule_day4, schedule_day5, schedule_day6, schedule_day7])
        combined_df.reset_index(drop=True, inplace=True)
        # heat map
        heatmap_df = combined_df.pivot(index='Date', columns='Start', values='Ratings')
        heatmap_df = heatmap_df.reset_index().melt(id_vars=['Date'], var_name='Start', value_name='Ratings')
        def fill_ratings(row):
            matching_rows = combined_df[(combined_df['Start'] <= row['Start']) & (combined_df['End'] >= row['Start'])]
            if not matching_rows.empty:
                return matching_rows['Ratings'].iloc[0]
            else:
                return row['Ratings']
        heatmap_df['Ratings'] = heatmap_df.apply(lambda row: fill_ratings(row) if pd.isnull(row['Ratings']) else row['Ratings'], axis=1)
        heatmap_df = heatmap_df.pivot(index='Date', columns='Start', values='Ratings')
        color_scale = [
            [0, "#D9D9D9"],
            [0.33, "#E16060"],
            [0.66, "#FBD167"],
            [1, "#65C089"],
        ]
        fig = px.imshow(
            heatmap_df,
            color_continuous_scale=color_scale,
            labels=dict(x="Time", y="Date", color="Ratings"),
        )
        fig.layout.coloraxis.showscale = False
        fig.update_layout(height=400)
        fig.update_layout(yaxis={'type': 'category'})

        # fig.update_layout(xaxis_range=[0,24])
        return html.Div(children = [
            html.H6(style={"padding-top": "1em", "font-size":"1.2em"},children=["Week in review"]),
            dcc.Graph(id="graph", figure=fig)])

    def _build_notification_widget(self):
        try:
            notification_percent = int(
                self.get_model().get_notification_count()
                * 100
                / self.get_model().get_all_notification_count()
            )

            widget = self._build_usage_widget(
                "notification-widget",
                f"notified you",
                f"{self.get_model().get_notification_count()} times",
                f"That is {notification_percent}% of all notifications.",
            )

            return widget
        except Exception:
            return self._build_no_data_usage_widget()

    def _build_pickup_widget(self):
        try:
            pickup_percent = int(
                self.get_model().get_pickup_count()
                * 100
                / self.get_model().get_notification_count()
            )

            widget = self._build_usage_widget(
                "pickup-widget",
                f"made you pick up the phone",
                f"{self.get_model().get_pickup_count()} times",
                f"That is {pickup_percent}% of the time it has notified you.",
            )

            return widget
        except Exception:
            return self._build_no_data_usage_widget()

    def _build_unlock_widget(self):
        try:
            unlock_percent = int(
                self.get_model().get_unlock_count()
                * 100
                / self.get_model().get_pickup_count()
            )

            widget = self._build_usage_widget(
                "unlock-widget",
                f"made you unlock the phone",
                f"{self.get_model().get_unlock_count()} times",
                f"That is {unlock_percent}% of the time it has made you pick up the phone.",
            )

            return widget
        except Exception:
            return self._build_no_data_usage_widget()

    def _build_usage_widget(
        self, id: str, title: str, number_times_occured: int, description: str
    ) -> html.Div:
        div = self._wrap_to_card(
            id,
            [
                html.P(title, className="card-title"),
                html.H1(number_times_occured, className="usage-widget-number"),
                html.P(description, className="usage-widget-desc"),
            ],
        )
        return div

    def _build_no_data_usage_widget(self) -> html.Div:
        div = html.Div(
            className="no-data-usage-widget",
            children=[html.H2("Something went wrong")],
        )
        return div

    def _build_emotion_emojis_widget(self) -> html.Div:
        div = self._wrap_to_card(
            "emotion-emojis-widget",
            [
                html.P(
                    className="card-title",
                    children=f"While you are using {self.get_model().get_current_app_name()}, you mostly felt...",
                ),
                html.Div(
                    className="d-flex align-items-center flex-wrap justify-content-around",
                    children=list(
                        map(
                            lambda e: html.Div(
                                className="d-inline-block",
                                children=[
                                    html.P(
                                        style={"font-size": "6em"},
                                        children=to_emoji(e),
                                    ),
                                    html.H5(className="text-center", children=e.value),
                                ],
                            ),
                            self.get_model().get_emotions(),
                        )
                    ),
                ),
            ],
        )
        return div

    def _wrap_to_card(self, id, divs) -> html.Div:
        return html.Div(
            id=id,
            className="card",
            children=[
                html.Div(
                    className="card-body",
                    children=divs,
                )
            ],
        )

    def update(self):
        self._html_component = self._build_html_component()
