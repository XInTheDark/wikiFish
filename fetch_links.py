from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup as bs

from BANNED import BANNED

def sample():
    res = requests.get("https://en.wikipedia.org/wiki/List_of_naval_battles")
    soup = bs(res.text, "html.parser")
    links = soup.find_all('a')
    for link in links:
        url = link.get("href", "")
        if url.startswith("/wiki/"):
            print(url)
            
def fetch_links(article, search_arr=None, limit=50):
    """Fetches the first few links from a Wikipedia article, as efficiently as possible.
    @param article: The link of the article to fetch.
    @param limit: The number of links to fetch. (fetched in order of appearance)
    @param search_arr: The array of search terms to be directly found. e.g.
    if a link is in the search_arr, then we do a direct, full-article search for that link, and return
    only the link if it is found. Otherwise, we do nothing special.
    
    @return: A list of links, each pointing to a Wikipedia article.
    Note that the filtering process is also done here, i.e. we guarantee that all links in the
    returned list are Wikipedia links.

    """
    if search_arr is None:
        search_arr = []
        
    # Fetch the article
    res = requests.get(article)
    
    # Parse the HTML
    soup = bs(res.text, 'html.parser')
    
    # Find all links
    links = soup.find_all('a')
    
    # Filter out non-Wikipedia links
    links = [link for link in links if link.has_attr('href') and link['href'].startswith('/wiki/')]
    
    # find all links that are in the search_arr
    find_links = [link for link in links if P(link['href']) in search_arr]
    
    if len(find_links) > 0:
        return find_links
    
    # Remove banned links e.g. 'Main_Page', 'Wikipedia:', 'Special:', 'Talk:', 'Portal:', 'Help:',
    
    links = [link for link in links if not any(x in link['href'] for x in BANNED)]
    
    # Convert to absolute links
    links = [P(link['href']) for link in links]
    
    # Return the first few links
    return links[:limit]

def test():
    print(fetch_links('https://en.wikipedia.org/wiki/Artificial_intelligence'))
    
def P(x):
    """process href url into wiki url."""
    # check if already a url
    if not x.startswith('/wiki/'):
        return None
    return 'https://en.wikipedia.org' + x

if __name__ == '__main__':
    test()