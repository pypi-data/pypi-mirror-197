# Acodis API Handler
This package provides easy to use python classes and functions to communicate with Acodis API (https://acodis.io).
Acodis is an IDP solution that focuses on extracting and structuring complex documents (PDFs, Images)

## Installation
```bash
pip install AcodisApiHandler
```

## Usage
This package is particularly useful for programmatic access, since ACODIS' API structure requires a different 
**user** and **password** for every export step. Hence, if you have to manage multiple exports 
(e.g. multiple workflows), you just need to update the main class `user` and `password` attribute,
and call the `authenticate()` method.
```python
from AcodisApiHandler import AcodisApiHandler

# Set up your credentials
ACODIS_BASE_URL = "https://<YOUR-ACOIDS-INSTANCE-URL>/workbench/api/transaction"
ACODIS_USER = "<YOUR-EXPORT-USERNAME>"
ACODIS_PASSWORD = "<YOUR-EXPORT-PASSWORD>"

# Create an instance of the AcodisApiHandler class
handler = AcodisApiHandler(ACODIS_BASE_URL)

# Set the credentials
handler.user = ACODIS_USER
handler.password = ACODIS_PASSWORD

# Authenticate with the API
handler.authenticate()

handler.workflow(pdf_path="<PATH-TO-PDF-FILE>")

# The extraction result is an ElementTree XML object stored in the handler.result variable
# You can check it by:
print(handler.result)
```

## Utils
This package also provides some utils to help you with the extraction process.

### Extracting tagged data points
Tags are used to identify the data points that you want to extract from the document.
This function will create a dictionary with the tags as keys and the extracted data as values.
```python
from AcodisApiHandler import extract_tags

tags_list = ["example_tag_1", "example_tag_1", "example_tag_1"]

# Using the precviously created handler instance
tagged_data = extract_tags(handler, tags_list)
```

If we print the `tagged_data` variable we will get:
```python
{
    "example_tag_1": "Example data 1",
    "example_tag_2": "Example data 2",
    "example_tag_3": "Example data 3"
}
```

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Roadmap
- [ ] Additional utils: parsing tables, extracting images, etc.
- [ ] Add unit tests
- [ ] Add batch processing and parallelization