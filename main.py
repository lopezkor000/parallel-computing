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
    print(data[:5])

extract_data('data.jsonl.gz', 'data.jsonl')
get_data(0, 50_000)
