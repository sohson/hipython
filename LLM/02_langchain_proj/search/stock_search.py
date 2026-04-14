import os
from dotenv import load_dotenv
load_dotenv()
MEILI_SEARCH_KEY = os.environ['MEILI_SEARCH_KEY']

import meilisearch
client= meilisearch.Client("http://127.0.0.1:7700", MEILI_SEARCH_KEY)

def stock_search(query):
  return client.index('nasdaq').search(query)