# DoNotDisturb

## Website structure

The website is composed of two pages: Goal Tracking and Usage Statistics.

### Goal Tracking 

Purpose of this page is for user to access, set and track their 'goals' for app usage. 
First graph represents the actual app usage vs the set usage, with color coding representing good and bad habits. 
Next widget helps user to find an appropriate time limit for an app, and last widget visualizes the time limit based on pre-existing usage of that app. 

### Usage Statistics

First graph on the page represents day or week in review, where users phone usage data is analyzed and visualized against their schedule. Colors of the heatmap represent good or bad habits of the user (ex. using phone in class is bad, watching youtube in free time is okay). 
Next three widgets inform the user about their habits regarding notifications, and last one represents their most frequent feelings when using that app.

## Code overview

The app runs based on app.py that includes html components of _Goal Tracking_ and _Usage Statistics_ and its callbacks. 
_usagePage_ includes files related to _Usage Statistics_ page, including changing the data based on the callbacks (updating granularity of data in _usagePageModel.py_ and updating the widget view in _usagePageView.py_).
To control header and switching between two pages, we implemented _header.py_. 

## Access

Check out https://donotdisturb-dataviz.herokuapp.com/