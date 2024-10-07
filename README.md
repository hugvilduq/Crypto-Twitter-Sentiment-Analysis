# Cryptocurrency Sentiment Analysis and Predictive Model

This project aims to forecast the rising or declining values of various cryptocurrencies by analyzing sentiment from users' tweets. The sentiment analysis results are used to predict cryptocurrency price movements, and the findings are visualized with Tableau for further analysis and conclusions.

## Project Structure
 
The project is organized into four main folders:

### 1. **Data Collection** (`01_Data_collection`)
   - Collects tweets using two methods:
     - **Tweepy**: Utilizing Twitter's official API for real-time tweet collection.
     - **Snscrape**: Web scraping technology for historical tweet collection.
   - Bitcoin values are loaded from a Kaggle dataset and stored in an SQL database.
   - **Bitcoin Event Finder**: Detects abrupt changes in Bitcoin (BTC) values within a given time frame (e.g., 1 hour, 1 day), referred to as "events".

### 2. **Data Exploration** (`02_Data_exploration`)
   - **Data Cleaning**: Prepares the collected tweet data and BTC values for analysis.
   - **Exploratory Data Analysis (EDA)**: Gathers insights from the data and visualizes it using word clouds and statistical techniques.

### 3. **ML Model** (`03_ML_Model`)
   - **Data Preparation**: Cleans the data and stores it in an SQL database.
   - **Sentiment Analysis**: Trains models (Logistic Regression and Support Vector Machines) to classify the sentiment of tweets as positive, neutral, or negative.
   - **Tweets Event Finder**: Detects abrupt changes in the volume of tweets or sentiment within a given time frame, correlating these with cryptocurrency price changes.
   - The results are saved in a database for further analysis.

### 4. **Dashboard** (`04_Dashboard.twb`)
   - **Tableau Visualization**: A dashboard that compares sentiment values of analyzed tweets with cryptocurrency price changes.
   - Events detected (both in BTC prices and tweet sentiment) are marked for easy identification and analysis.
   
## Usage Instructions

1. **Data Collection**: Run the scripts in the `01_Data_collection` folder to collect tweets and store cryptocurrency values.
2. **Data Exploration**: Explore the data by running the scripts in the `02_Data_exploration` folder.
3. **ML Model**: Train and evaluate the sentiment analysis models by running the scripts in the `03_ML_Model` folder. The results will be saved in the database.
4. **Dashboard Visualization**: Open the `04_Dashboard.twb` file in Tableau to view the visualizations of the predictions and events.

## Dependencies

- **Python**: Required for data collection, cleaning, and model training.
- **SQL Database**: Used to store tweet and cryptocurrency data.
- **Tableau**: For visualization and dashboard creation.
- **Tweepy**: Twitter API for real-time tweet collection.
- **Snscrape**: Web scraping for historical tweet collection.
- **scikit-learn**: For training the Logistic Regression and SVM models.
- **Pandas**: For data manipulation and cleaning.
- **Matplotlib/Seaborn**: For EDA and visualizing word clouds.

## Results and Analysis

The model forecasts cryptocurrency price movements by analyzing sentiment from tweets. Abrupt changes in tweet sentiment or volume are identified as events and compared with BTC value changes. This helps to detect patterns between social media sentiment and cryptocurrency prices.

## Contributions

Feel free to contribute to this project by submitting issues or pull requests. Any suggestions for improvements or additional features are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

