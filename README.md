# Reddit Data Scraper

## Overview
This script fetches posts from Reddit using the `requests` library and stores the data in a CSV file. It allows users to gather information from the top 1000 safe-for-work (SFW) subreddits, such as post titles, scores, number of comments, and more. The data is pulled based on specified parameters, including subreddit name, listing type (e.g., top, hot), and timeframe (e.g., day, week).

## Features
- Fetches data from over 1000 subreddits
- Allows customization of timeframe and listing type
- Handles Reddit's rate limiting dynamically
- Outputs data to a CSV file with detailed post information
- Includes robust error handling

## Usage
1. Clone or download this repository to your local machine
2. Ensure the required libraries are installed
3. Customize the script parameters as needed:
   * `timeframe`: Set the time range for posts (e.g., `hour`, `day`, `week`, `month`, `year`, `all`)
   * `listing`: Choose the type of listing (e.g., `top`, `hot`, `new`, `rising`)
   * `subreddits`: Add or remove subreddit names in the list to tailor the data collection
4. Run the script:
```bash
python reddit_scraper.py
```
5. The script will save the data as a CSV file named `reddit_top_posts.csv` in the current directory

## Key Functions

### `get_reddit(subreddit, listing, timeframe, after=None)`
Fetches data from a specific subreddit using Reddit's JSON API.

**Parameters:**
* `subreddit`: The subreddit name to fetch data from
* `listing`: The type of post listing to retrieve (e.g., `top`, `hot`)
* `timeframe`: The time range for posts (e.g., `year`, `month`)
* `after`: ID of the last post from the previous batch for pagination

**Returns:** JSON response containing post data

### `get_results(r)`
Processes the JSON response and extracts relevant post information into a DataFrame.

**Returns:** Pandas DataFrame with columns:
* `subreddit`: Subreddit name
* `title`: Post title
* `upvotes`: Number of upvotes
* `downvotes`: Number of downvotes
* `score`: Post score
* `upvote_ratio`: Ratio of upvotes to total votes
* `comments`: Number of comments
* `views`: Post view count (if available)
* `created_date`: Post creation timestamp
* `url`: Post URL

## How It Works
1. The script iterates over a list of subreddits
2. For each subreddit, it fetches up to 10 batches of posts (100 posts per batch)
3. Handles Reddit's rate limits by monitoring headers and applying dynamic sleep times
4. Combines all data into a single DataFrame
5. Exports the DataFrame to a CSV file named `reddit_top_posts.csv`

## Output
* **File Name:** `reddit_top_posts.csv`
* **File Format:** CSV
* **Columns:**
  * `subreddit`
  * `title`
  * `upvotes`
  * `downvotes`
  * `score`
  * `upvote_ratio`
  * `comments`
  * `views`
  * `created_date`
  * `url`
