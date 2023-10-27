import pdfplumber
import pandas as pd
import PyPDF2

file_path = "statement.pdf"

with pdfplumber.open(file_path) as pdf:
    tables = [page.extract_tables() for page in pdf.pages]

dfs = []
dfs.extend([pd.DataFrame(table[1:], columns=table[0]) for page_tables in tables for table in page_tables])

combined_df = pd.concat(dfs, ignore_index=True)
combined_df.head(5)

with open('statement.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

keys = [
    'Account Name',
    'Address',
    'Date',
    'Account Number',
    'Account Description',
    'Branch',
    'Drawing Power',
    'Interest Rate(% p.a.)',
    'MOD Balance',
    'CIF No.',
    'IFS Code',
    'MICR Code'
]

extracted_data = {}
for key in keys:
    start_idx = text.find(key)
    if start_idx != -1:
        start_idx = text.find(':', start_idx) + 1
        end_idx = text.find('\n', start_idx)
        value = text[start_idx:end_idx].strip()
        extracted_data[key] = value
    else:
        extracted_data[key] = 'Not found'

address_start_idx = text.find('Address') + len('Address')
address_end_idx = text.find('Txn', address_start_idx)
address_value = text[address_start_idx:address_end_idx].strip().replace('\n', ' ')
extracted_data['Address'] = address_value

df = pd.DataFrame([extracted_data])
json_data = df.to_json(orient='records')

print(json_data)