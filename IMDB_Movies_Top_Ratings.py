from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.imdb.com/chart/top'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(url, headers=headers)
response.raise_for_status
#print(response.content)
soup = BeautifulSoup(response.text,'html.parser')

# Find the main container div using data-testid attribute
main_div = soup.find('div', {'data-testid': 'chart-layout-parent'})

movie_list_items = main_div.find_all('li', class_='ipc-metadata-list-summary-item')

if main_div:
    # Find all <li> elements within the main div directly
    movie_list_items = main_div.find_all('li', class_='ipc-metadata-list-summary-item')

    titles = []
    years = []
    ratings = []
    ranks = []

    for index, item in enumerate(movie_list_items, start=1):
        # Extract title
        title_element = item.find('h3', class_='ipc-title__text')
        title = title_element.text.strip() if title_element else ''
        
        # Split index number from title
        title = title.split('. ', 1)[-1]  # Splitting at the first occurrence of '. '
        
        titles.append(title)

        # Extract year (first span in metadata list)
        year_element = item.find('span', class_='sc-b0691f29-8')  # Assuming this is the year span
        year = year_element.text.strip() if year_element else ''
        years.append(year)

        # Extract rating
        rating_element = item.find('span', class_='sc-b0691f29-1 grHDBY')
        rating = rating_element.text.strip().split()[0] if rating_element else ''
        ratings.append(rating)
        
        # Add rank
        ranks.append(index)

    # Create a dataframe from the lists
    data = {'Rank': ranks, 'Title': titles, 'Year': years, 'Rating': ratings}
    df = pd.DataFrame(data)

    # Display or further process the dataframe
    print(df)

    df.to_csv('IMDB_TOP_MOVIES_RATINGS.csv', index=False, encoding='utf-8')  # Remove the index column from the CSV

else:
    print(f"Failed to retrieve content, status code: {response.status_code}")
