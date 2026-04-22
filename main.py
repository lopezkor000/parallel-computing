"""
Extract data if not available
"""
import gzip, shutil, json
import pandas as pd

try:
    open('data.jsonl')
except OSError:
    print("DATA NOT FOUND: Extracting...")
    with gzip.open('data.jsonl.gz', 'rb') as f_in:
        with open('data.jsonl', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
# finally:
#     with open('data.jsonl') as file:
#         data = pd.read_json("data.jsonl", lines=True, nrows=10_000, )
#         print(data)

def get_data(row, nrows):
    data = []
    with open('data.jsonl') as file:
        for _ in range(row):
            file.readline()
        for _ in range(nrows):
            data.append(json.loads(file.readline()))
    print(data[:5])

get_data(0, 50_000)
