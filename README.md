# Detecting Pausing through Network Data
[Project Report](https://github.com/Bravo-Luis/detecting_pauses/files/13675292/Detecting_Pauses.pdf)

## Overview

This project focuses on detecting playback states (Playing, Paused, Buffering) in YouTube videos by analyzing network packet traces. We developed a data collection pipeline using the Netunicorn library, Selenium for simulating real-world user interactions, and machine learning models for state detection.

## Pipeline Objective

The primary goal is to capture detailed packet trace data while simulating real-world interactions with YouTube videos. This involves using Selenium to randomly pause and unpause videos, mimicking user actions and collecting critical data points during these interactions.

## Data Collection

- **Packet Trace**: Network packet information during different video playback states.
- **Video State**: Real-time status of the YouTube video (Playing, Paused, Buffering).
- **Latency**: Network response delay measurements.
- **YouTube Stats for Nerds**: Advanced metrics from YouTube for deeper insight into video and network performance.

## Data Combiner and Pausing Simulator

- `DataCombiner` Task: Combines pcap and json files into a csv, focusing on relevant data fields.
- `PausingSimulator` Task: Simulates user behavior by pausing and unpausing videos at random intervals. Collects YouTube metrics and latency data.

## Experiment Setup

- RemoteClient setup with login and node selection.
- Capture tasks (`StartCapture` and `StopNamedCapture`) to gather packet traces.
- `PausingSimulator` to simulate video playback and collect data.
- `DataCombiner` to merge and process data.
- Pipeline and experiment execution using DockerImage and Experiment API.

## Data Preparation and Analysis

- Data cleaning, feature extraction, and balancing.
- Feature importance analysis and model training using RandomForestClassifier.
- Testing against a separate dataset to validate model performance.

## Key Features and Insights

- Critical features: `ratio_time_since_last_DNS`, `rolling_median_time_since_last_DNS`.
- RandomForestClassifier trained with parameters tuned for best performance.
- Model's proficiency in differentiating between buffering and non-buffering states, with challenges in differentiating between playing and paused states.

## Model Evaluation

- Accuracy and classification report on training and testing datasets.
- Feature importance analysis to understand key predictors.
- Trustee analysis for model explanation and global fidelity.

## Conclusion

The project successfully demonstrates the use of machine learning models to differentiate between various states of video playback based on network packet traces. While effective in buffering detection, it highlights the need for further refinement in distinguishing between playing and paused states.
