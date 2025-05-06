# 📊 YouTube Trending Video Analytics Project

This project analyzes trending YouTube videos across different countries (India, US, GB) to uncover insights on content performance, viewer preferences, sentiment patterns, and category-wise trends.

## 📁 Project Structure

```
youtube_analysis_project/
│
├── yt_analysis.py                # Main Python script for data analysis
│
├── data/
│   ├── raw data/                 # Original unprocessed datasets (CSV & JSON)
│   │   ├── IN_youtube_trending_data.csv
│   │   ├── US_youtube_trending_data.csv
│   │   ├── GB_youtube_trending_data.csv
│   │   ├── IN_category_id.json
│   │   ├── US_category_id.json
│   │   └── GB_category_id.json
│   └── cleaned data/             # Cleaned and processed datasets
│       ├── IN_cleaned.csv
│       └── IN_with_analysis.csv
│
├── insights/
│   ├── youtube_analysis_report.pdf    # Summary of findings and insights
│   └── *.png                          # Visualization charts saved as images
```

## 🧠 Project Objectives

- 📈 Understand trends in YouTube video popularity across regions.
- 🎯 Analyze engagement metrics (views, likes, comments).
- 🧹 Clean and standardize datasets from multiple countries.
- 🗂️ Map category IDs to category names.
- 🧠 Perform sentiment analysis on video titles and tags.
- 📊 Visualize patterns in viewer preferences and category-wise performance.
- ⏱️ Analyze trending duration and publishing trends over time.

## 🚀 Features

- Country-wise trend analysis
- Sentiment analysis using `TextBlob`
- Top-performing categories by average views
- Engagement comparison using bar plots
- Time-series visualizations for publish day and trend duration

## 🛠️ Technologies Used

- **Python 3**
- **Pandas**, **NumPy**
- **Matplotlib**, **Seaborn**
- **TextBlob** (for sentiment analysis)
- **VS Code** (development)
- **GitHub** (version control)

## 📊 Sample Visualizations

Visualizations are saved in the `insights/` folder, including:

- Likes vs Comments by Category
- Views vs Likes by Category
- Sentiment Distribution
- Trending Duration vs Views
- Publish Day Distribution

## 📌 How to Run the Project

1. **Clone this repository**:
   ```bash
   git clone https://github.com/your-username/youtube_analysis_project.git
   cd youtube_analysis_project
   ```

2. **Install dependencies**:
   ```bash
   pip install pandas numpy matplotlib seaborn textblob
   python -m textblob.download_corpora
   ```

3. **Run the script**:
   ```bash
   python yt_analysis.py
   ```

4. **Check outputs**:
   - Cleaned data: `data/cleaned data/`
   - Visualizations and reports: `insights/`

## 📄 Sample Insights

- **Most Viewed Category in India**: Entertainment
- **Sentiment Analysis**: Majority of video titles had neutral sentiment.
- **Peak Publish Days**: Tuesdays and Fridays had more trending videos.
- **Engagement**: High correlation between views and likes.

## 📦 Raw Data

Due to size constraints, raw data files are hosted externally.  
📥 [Download Raw Data from Google Drive](https://drive.google.com/file/d/1OTbk1vt6Xs5Kikv_9gOkTgatHSkr660j/view?usp=sharing

## 👤 Author

**Rohit Sonawane**  

Feel free to ⭐ the repo if you find this helpful!
