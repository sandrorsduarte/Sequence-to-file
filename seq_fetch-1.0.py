import sys
import requests

def entrez_search(database, term):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": database,
        "term": term,
        "retmax": 10,
        "usehistory": "y",
        "retmode": "json"
    }
    response = requests.get(base_url, params=params)
    return response.json()

def fetch_sequences(database, ids):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": database,
        "id": ",".join(ids),
        "rettype": "fasta",
        "retmode": "text"
    }
    response = requests.get(base_url, params=params)
    return response.text

def save_to_fasta(filename, sequences):
    with open(filename, "w") as f:
        f.write(sequences)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("How to use: python seq_fetch-1.0.py <database> <search_term> <output_file>")
        sys.exit(1)
    
    database = sys.argv[1]
    term = sys.argv[2]
    output_file = sys.argv[3]

    search_results = entrez_search(database, term)
    ids = search_results["esearchresult"]["idlist"]

    sequences = fetch_sequences(database, ids)
    save_to_fasta(output_file, sequences)
    print("Sequences saved to", output_file)

