import gzip, shutil, json, os

def extract_data(zip:str, file:str):
    """
    Extract data if not available
    """
    try:
        open(file)
    except OSError:
        print("DATA NOT FOUND: Extracting...")
        with gzip.open(zip, 'rb') as f_in:
            with open(file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

def get_data(page:int, rows:int) -> list[dict]:
    """
    Grabs paginated data from extracted JSONL file
    """
    data = []
    with open('data.jsonl') as file:
        for _ in range(page * rows):
            file.readline()
        for _ in range(rows):
            data.append(json.loads(file.readline()))
    return data

def output_sample(data):
    """
    Creates file with first datapoint for reference
    """
    with open('sample.json', 'w') as file:
        json.dump(data[0], file)

def map_citations(data:list[dict]):
    """
    Creates map of data based on citations
    """
    citation_map:dict[str,list] = dict()
    keyword_map:dict[str,list] = dict()

    for item in data:
        id = item['lens_id']

        # Ignores datapoints with no citations or keywords
        if 'keywords' not in item:
            print(id, item['title'])
            continue

        if 'scholarly_citations' in item:
            citation_map[id] = item['scholarly_citations']
        
        for word in item['keywords']:
            word = word.strip()
            if word not in keyword_map:
                keyword_map[word] = list()
            keyword_map[word].append(id)

    return citation_map, keyword_map

def export_mappings(citations, keywords):
    os.makedirs('output', exist_ok=True)
    with open('output/citation_map.json', 'w') as file:
        json.dump(citations, file, indent=2)
    with open('output/keyword_map.json', 'w') as file:
        json.dump(keywords, file, indent=2)

if __name__ == "__main__":
    extract_data('data.jsonl.gz', 'data.jsonl')
    data = get_data(0, 1_000)
    output_sample(data)
    cite, keys = map_citations(data)
    export_mappings(cite, keys)