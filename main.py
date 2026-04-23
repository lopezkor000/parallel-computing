import gzip, shutil, json

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
    citation_map:dict[str,set] = dict()
    keyword_map:dict[str,set] = dict()

    for item in data[:1]:
        id = item['lens_id']

        # Ignores datapoints with no citations or keywords
        if 'scholarly_citations' not in item or 'keywords' not in item:
            print(id, item['title'])
            continue

        if id not in citation_map:
            citation_map[id] = set()
        for cite in item['scholarly_citations']:
            citation_map[id].add(cite)
        
        for word in item['keywords']:
            if word not in keyword_map:
                keyword_map[word] = set()
            keyword_map[word].add(id)

    return citation_map, keyword_map

if __name__ == "__main__":
    extract_data('data.jsonl.gz', 'data.jsonl')
    data = get_data(0, 1_000)
    # output_sample(data)
    cite, keys = map_citations(data)
    print(list(keys.keys())[0], cite[list(list(keys.values())[0])[0]])