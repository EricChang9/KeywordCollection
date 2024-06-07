from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

API_KEY = 'AIzaSyDdZSF9LalJ31xxU2-F5KjUrEiWK9SrxRs'

SERVER = 'https://www.googleapis.com'
API_VERSION = 'v1beta'
DISCOVERY_URL_SUFFIX = '/discovery/v1/apis/trends/' + API_VERSION + '/rest'
DISCOVERY_URL = SERVER + DISCOVERY_URL_SUFFIX
service = build('trends', API_VERSION,
                  developerKey=API_KEY,
                  discoveryServiceUrl=DISCOVERY_URL)
# try either of the requests 'req'
SEARCH_TERM = 'flu'
ITERATIONS = 2
big_list = []
for i in range(ITERATIONS):
    req = service.getTopQueries(term=SEARCH_TERM)
    # req = service.getTopTopics(term=SEARCH_TERM)
    res = req.execute()

    related_terms_list = []

    for term in res['item']:
        related_terms_list.append(term['title'])
    big_list.append(related_terms_list)

    SEARCH_TERM = related_terms_list[0]
print(big_list)
