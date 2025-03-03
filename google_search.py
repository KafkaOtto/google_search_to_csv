import requests
import csv
import configparser

# get the API KEY here: https://developers.google.com/custom-search/v1/overview
# # get your Search Engine ID on your CSE control panel

config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config['google']['api_key']
CSE_ID = config['google']['cse_id']
QUERY = config['google']['query']
OR_TERMS = " ".join(config['google']['or_terms'].split(","))  # Convert comma-separated values to space-separated


# Function to perform a Google search
def google_search(query, or_terms, page=1):
    url = f"https://www.googleapis.com/customsearch/v1"
    start = (page - 1) * 10 + 1
    params = {
        'key': API_KEY,
        'cx': CSE_ID,
        'q': query,
        'orTerms': or_terms,
        'start': start
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(f"Error Msg: {response.reason}")
        return None

def save_to_csv(results, filename='google_search_result_0219.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link', 'Snippet'])  # Write header
        for item in results:
            title = item['title']
            link = item['link']
            snippet = item['snippet']
            writer.writerow([title, link, snippet])
    print(f"Results saved to {filename}")

if __name__ == '__main__':
    pages = 11
    all_results = []
    for p in range(1, pages):
        search_results = google_search(QUERY, OR_TERMS, p)
        if search_results and 'items' in search_results:
            all_results.extend(search_results['items'])

    if search_results:
        # Save results to CSV
        save_to_csv(all_results)
    else:
        print("No results found or an error occurred.")