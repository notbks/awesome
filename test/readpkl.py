import pickle
from base64 import decode

with open('session.pkl', 'rb') as f:
    print(f.read(100))
    # print(f.get('search_url', params= params))
