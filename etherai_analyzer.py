import os
from flask import Flask, render_template, request, jsonify
import openai
import requests
import json

app = Flask(__name__)

# Replace 'YOUR_OPENAI_API_KEY' with your actual key
openai.api_key = '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'

def truncate_text(text, max_length):
    return text[:max_length]

def fetch_contract_info(contract_address):
    try:
        # Call EtherScan API to fetch contract details
        api_url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={contract_address}&apikey="
        response = requests.get(api_url)
        data = response.json()

        if data['status'] == '1':
            contract_info = data['result'][0]
            contract_code = contract_info['SourceCode']
            contract_abi = contract_info['ABI']
            return contract_code, contract_abi
        else:
            return None, None
    except Exception as e:
        return None, None

@app.route('/')
def index():
    return render_template('index_etherai2.html')

@app.route('/convert_to_legal_contract', methods=['POST'])
def convert_to_legal_contract():
    try:
        contract_address = request.json['contractAddress']
        contract_code, contract_abi = fetch_contract_info(contract_address)

        if contract_code and contract_abi:
            # Extract functions from contract ABI
            contract_functions = extract_functions(contract_abi)

            # Construct input text for OpenAI
            input_text = f"Which type of Smart Contract is this - whether ERC20, ERC721, ERC1155 or NFT Contract and which language is it written in? What all powers does the owner have? When can it be transferred?Define its mint, burn and pause function in plain english with line breaks? What are the major functions and what does each function do? Smart Contract Code:\n{contract_code}\n\nFunctions:\n" + '\n'.join(contract_functions)

            # Truncate input text
            input_text = truncate_text(input_text, 11000)

            # Call OpenAI API to convert code and functions to legal contract terms
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use the GPT-3.5 model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": input_text},
                ],
                max_tokens=3097,
                temperature=0.7,
                stop="\n"
            )

            legal_contract_terms = response.choices[0].message['content'].strip()

            return {'legalContractTerms': legal_contract_terms}
        else:
            return {'error': 'Unable to fetch contract information from EtherScan API'}
    except Exception as e:
        return {'error': str(e)}

def extract_functions(contract_abi):
    try:
        # Parse contract ABI and extract function names
        functions = []
        abi_list = json.loads(contract_abi)  # Convert ABI string to list
        for item in abi_list:
            if item['type'] == 'function':
                functions.append(item['name'])
        return functions
    except Exception as e:
        return []

@app.route('/getOwnershipDetails', methods=['POST'])
def get_ownership_details():
    try:
        contract_address = request.form.get('contractAddress')

        url = f"https://api.verbwire.com/v1/nft/data/ownershipForContractAddress?contractAddress={contract_address}&limit=25&page=1&sortDirection=DESC"
        headers = {
            "accept": "application/json",
            "X-API-Key": ""  # Replace with your actual VerbWire API key
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

        return render_template('index_etherai2.html', result=response_data)
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True)
