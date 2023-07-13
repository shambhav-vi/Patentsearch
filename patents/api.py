import requests

def search_patent(query):
    url = "https://global-patent1.p.rapidapi.com/s"

    headers = {
        "X-RapidAPI-Key": "8dbef98c6bmsha9f8672da2bd346p162b37jsn5fc9c497d586",
        "X-RapidAPI-Host": "global-patent1.p.rapidapi.com"
    }
    params = {
        "ds": "all",
        "q": query
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            patents = []
            unique_patent_ids = set()  # Set to store unique patent_ids
            for item in data.get('patents', []):
                patent_id = item.get('id', '')
                # Check if patent_id is unique
                if patent_id not in unique_patent_ids:
                    title = item.get('title', '')
                    inventor = item.get('inventor', '')
                    abstract = item.get('abstract', '')
                    link = item.get('url', '')
                    patents.append({
                        'patent_id': patent_id,
                        'title': title,
                        'inventor': inventor,
                        'abstract': abstract,
                        'link': link
                    })
                    unique_patent_ids.add(patent_id)  # Add patent_id to the set

            return patents
        except KeyError:
            print("Error: Missing 'patents' key in response data")
    else:
        print(f"Error: {response.status_code} - {response.text}")

    return []

def fetch_patent_details(patents):
    for patent in patents:
        if isinstance(patent, dict) and 'link' in patent:
            patent_id = extract_patent_id(patent['link'])
            if patent_id:
                patent_details = fetch_patent_details_from_api(patent_id)
                if patent_details:
                    patent['title'] = patent_details.get('title', '')
                    patent['inventor'] = patent_details.get('inventor', '')
                    patent['abstract'] = patent_details.get('summary', '')  
    return patents

def extract_patent_id(url):
    parts = url.split('/')
    if len(parts) >= 3:
        return parts[-2]
    return None

def fetch_patent_details_from_api(patent_id):
    url = f"https://global-patent1.p.rapidapi.com/s?ds=all&q={patent_id}"
    headers = {
        "X-RapidAPI-Key": "8dbef98c6bmsha9f8672da2bd346p162b37jsn5fc9c497d586",
        "X-RapidAPI-Host": "global-patent1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            patents = data.get('patents', [])
            if patents:
                patent = patents[0]  # Get the first patent in the list
                patent_details = {
                    'title': patent.get('title', ''),
                    'inventor': patent.get('inventor', ''),
                    'summary': patent.get('summary', '')
                }
                return patent_details
            else:
                print("Error: No patents found in the response data")
        except KeyError:
            print("Error: Missing keys in response data")
    else:
        print(f"Error: {response.status_code} - {response.text}")

    return None

