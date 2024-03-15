import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_nft.html')



@app.route('/getOwnershipDetails', methods=['POST'])
def get_ownership_details():
    contract_address = request.form.get('contractAddress')

    url = f"https://api.verbwire.com/v1/nft/data/ownershipForContractAddress?contractAddress={contract_address}&limit=25&page=1&sortDirection=DESC"
    headers = {
        "accept": "application/json",
        "X-API-Key": "sk_live_08ea7bc0-db22-41fd-aed8-648aa3e631f4"  # Replace with your actual VerbWire API key
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch ownership details'}), response.status_code

    ownership_data = response.json()

    # Extract the 'results' list from the 'ownership' key
    results = ownership_data.get('ownership', {}).get('results', [])

    # Prepare response in the desired format
    response_data = {
        'ownership': {
            'results': results,
            'page': ownership_data.get('page', 1),
            'limit': ownership_data.get('limit', 25),
            'totalPages': ownership_data.get('totalPages', 1),
            'totalResults': ownership_data.get('totalResults', 0)
        }
    }

    return render_template('index.html', result=response_data)

if __name__ == '__main__':
    app.run(debug=True)
