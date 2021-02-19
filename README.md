### Geocoding CLI

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

requirements:
* requests

To run script first you need to set the API_KEY environment variable, like this:

```
export API_KEY='YOUR_API_KEY'
```

and next use

```
python3 geocoding_imss.py file.csv output_name
```

where ```file.csv``` is the file that you want to read and parse address to coordinates and ```output_name``` is the file name that will saved after the script runs
