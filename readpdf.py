inputDir = '/Users/pax/devbox/gov2/data/declaratii.integritate.eu/'
# fileName = '14540094_2571954_a'
fileName = '14982713_2774302_a'

import PyPDF2
import json

def extract_pdf_metadata(pdf_path):
    pdf_data = []

    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        # Extract document-level metadata
        document_metadata = pdf_reader.metadata

        for page_number, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()

            page_data = {
                "page_number": page_number + 1,
                "text": page_text,
                "metadata": document_metadata,
            }

            pdf_data.append(page_data)

    return pdf_data

pdf_data = extract_pdf_metadata(inputDir + fileName + '.pdf')

output_json_path = inputDir + fileName + '.json'

with open(output_json_path, "w") as json_file:
    json.dump(pdf_data, json_file, indent=4)