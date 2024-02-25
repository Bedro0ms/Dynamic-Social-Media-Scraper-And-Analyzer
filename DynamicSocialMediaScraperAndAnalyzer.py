# Further enhanced Python script for comprehensive web scraping, data processing, analysis, and visualization
# tailored for bed.social, including dynamic pagination and sentiment analysis.

# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging
from textblob import TextBlob  # For sentiment analysis
import matplotlib.pyplot as plt  # For data visualization

# Enhanced logging setup
logging.basicConfig(filename='advanced_scraping_log.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Define a function to dynamically scrape data until all pages are covered
def dynamic_scrape_bed_social(base_url):
    all_data = []
    page = 1
    while True:
        try:
            url = f"{base_url}/page/{page}"
            response = requests.get(url, timeout=10)  # Added timeout for requests
            if response.status_code != 200:
                logging.warning(f"Finished scraping or failed to retrieve data from {url}")
                break  # Exit loop if page not found or end of pages reached
            
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article')
            if not articles:  # Break if no articles found
                break
            
            for article in articles:
                title = article.find('h2').text.strip()
                description = article.find('p', class_='description').text.strip()
                user_comments = [comment.text.strip() for comment in article.find_all('div', class_='comment')]
                all_data.append({
                    'title': title,
                    'description': description,
                    'comments': user_comments
                })
            page += 1  # Move to the next page
        except Exception as e:
            logging.error(f"Error scraping {url}: {e}")
            break  # Exit loop in case of an error
    return all_data

# Function for sentiment analysis on comments
def analyze_sentiment(comments):
    sentiments = []
    for comment in comments:
        blob = TextBlob(comment)
        sentiments.append(blob.sentiment.polarity)  # Appending sentiment score
    return sentiments

# Enhanced analysis including sentiment
def enhanced_social_media_analysis(df):
    # Applying sentiment analysis on comments
    df['comment_sentiments'] = df['comments'].apply(analyze_sentiment)
    df['average_sentiment'] = df['comment_sentiments'].apply(lambda x: sum(x) / len(x) if x else 0)
    return df

# Visualization of data analysis results
def visualize_data(df):
    # Visualize comment length
    comment_lengths = df['comments'].apply(lambda x: [len(comment) for comment in x]).explode()
    plt.figure(figsize=(10, 6))
    plt.hist(comment_lengths, bins=20, color='blue')
    plt.title('Distribution of Comment Lengths')
    plt.xlabel('Length of comments')
    plt.ylabel('Number of comments')
    plt.show()

    # Visualize average sentiment scores
    plt.figure(figsize=(10, 6))
    plt.hist(df['average_sentiment'], bins=20, color='green')
    plt.title('Distribution of Average Comment Sentiments')
    plt.xlabel('Average Sentiment Score')
    plt.ylabel('Number of Posts')
    plt.show()

# Example usage:
# Comment out the following lines when running in the actual script to avoid immediate execution.

# base_url = 'https://bed.social'
# raw_data = dynamic_scrape_bed_social(base_url)
# normalized_data = enhanced_normalize_data(raw_data)
# analyzed_data = enhanced_social_media_analysis(normalized_data)
# visualize_data(analyzed_data)
