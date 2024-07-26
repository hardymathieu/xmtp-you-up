#!/home/hymath/xmtp-you-up/xmtppy/bin/python
#-*- coding: utf-8 -*- 


import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime
import logging
import ollama

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='/home/hymath/xmtp-you-up/rtbf_scraper.log', filemode='a')
logger = logging.getLogger()

# Initialize Ollama client
ollama_client = ollama.Client(host='http://localhost:11434')

def scrape_rtbf_headlines():
    try:
        logger.info("Starting to scrape RTBF headlines.")
        url = "https://www.rtbf.be/info"
        response = requests.get(url)
        response.raise_for_status()
        logger.info("Successfully fetched RTBF website content.")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Debug: print out some of the HTML content to ensure we're scraping the right part
        print(soup.prettify()[:3000])  # Print first 3000 characters of the HTML for inspection
        
        # Modify the selector based on the actual HTML structure of the page
        headlines_elements = soup.find_all('h3')
        
        if not headlines_elements:
            logger.warning("No headlines elements found.")
            print("No headlines elements found.")  # Added print statement
        
        headlines = [element.get_text(strip=True) for element in headlines_elements[:5]]
        logger.info(f"Scraped headlines: {headlines}")
        print("Scraped headlines:", headlines)  # Added print statement
        return headlines
    except requests.RequestException as e:
        logger.error(f"Request error occurred during scraping: {e}")
        print(f"Request error occurred during scraping: {e}")  # Added print statement
        return []
    except Exception as e:
        logger.error(f"An error occurred during scraping: {e}")
        print(f"An error occurred during scraping: {e}")  # Added print statement
        return []

def summarize_headlines(headlines):
    try:
        logger.info("Starting to summarize headlines.")
        prompt = f"Summarize the following top 5 news headlines from RTBF in a paragraph:\n\n" + "\n".join(headlines)
        response = ollama_client.generate(model='phi3', prompt=prompt)
        logger.info(f"Received response: {response}")
        print(f"Received response: {response}")  # Added print statement to debug response structure
        
        summary = response.get('response', '').strip()
        logger.info(f"Generated summary: {summary}")
        print("Generated summary:", summary)  # Added print statement
        return summary
    except Exception as e:
        logger.error(f"An error occurred during summarization: {e}")
        print(f"An error occurred during summarization: {e}")  # Added print statement
        return ""

def main():
    logger.info("Main process started.")
    print("Main process started.")  # Added print statement
    
    # Scrape RTBF headlines
    headlines = scrape_rtbf_headlines()
    if not headlines:
        logger.error("Failed to scrape headlines.")
        print("Failed to scrape headlines.")  # Added print statement
        return
    
    # Summarize headlines
    summary = summarize_headlines(headlines)
    if not summary:
        logger.error("Failed to summarize headlines.")
        print("Failed to summarize headlines.")  # Added print statement
        return
    
    # Connect to SQLite database
    try:
        logger.info("Connecting to SQLite database.")
        print("Connecting to SQLite database.")  # Added print statement
        conn = sqlite3.connect('/home/hymath/xmtp-you-up/rtbf_news.db')
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        logger.info("Creating table if not exists.")
        print("Creating table if not exists.")  # Added print statement
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_news_summary
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             summary TEXT NOT NULL,
             timestamp DATE DEFAULT CURRENT_DATE)
        ''')
        
        # Insert into database
        logger.info("Inserting summary into the database.")
        print("Inserting summary into the database.")  # Added print statement
        cursor.execute('''
            INSERT INTO daily_news_summary (summary)
            VALUES (?)
        ''', (summary,))
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        logger.info("Database operation completed. Daily news summary added to the database.")
        print("Daily news summary added to the database.")  # Added print statement
    except Exception as e:
        logger.error(f"An error occurred with the database operation: {e}")
        print(f"An error occurred with the database operation: {e}")  # Added print statement

if __name__ == "__main__":
    main()
