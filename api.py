import csv
from queue import Queue
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")

SERVER = 'https://www.googleapis.com'
API_VERSION = 'v1beta'
DISCOVERY_URL_SUFFIX = '/discovery/v1/apis/trends/' + API_VERSION + '/rest'
DISCOVERY_URL = SERVER + DISCOVERY_URL_SUFFIX
service = build('trends', API_VERSION,
                  developerKey=API_KEY,
                  discoveryServiceUrl=DISCOVERY_URL)
#this is the node class that we will create the tree from 
class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)
    def has_children(self):
        return len(self.children) > 0
    

def build_tree(keyword, depth=2):
    if depth == 0:
        return Node(keyword)

    # Fetch related queries for the keyword
    req = service.getTopQueries(term=keyword)
    res = req.execute()
    related_queries = []
    for item in res['item']:
        related_queries.append(item['title'])
        
    print(related_queries)
    # Create a new node for the keyword
    node = Node(keyword)

    # Recursively build children nodes
    for query in related_queries:
        child_node = build_tree(query, depth - 1)
        node.add_child(child_node)

    return node

def breadth_first_traversal(root):
    keyword_list = []
    if not root:
        return
    queue = Queue()
    queue.put(root)
    while not queue.empty():
        node = queue.get()
        keyword_list.append(node.data)
        for child in node.children:
            queue.put(child)
            
    with open("keywords.csv", "w") as out:
        writer = csv.writer(out)
        writer.writerow(keyword_list)

root  = build_tree('flu')
breadth_first_traversal(root)