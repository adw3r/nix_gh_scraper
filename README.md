# GitHub parser


## Installation

### pip
```bash
pip install -r requirements.txt
pip install -e .
```
OR
### UV
```bash
uv sync
```

## How to use

Script requires full path to the input file. The structure of the input_file.json should be like this
```json
{
  "keywords": [
    "openstack",
    "nova",
    "css"
  ],
  "proxies": [
    "eu3030339:hKjxGgrgkt@194.61.9.17:7952",
    "eu3030339:hKjxGgrgkt@46.8.202.81:7952"
  ],
  "type": "Repositories"
}
```


```bash
python main.py --file=input_file.json
# or
python main.py -f input_file.json
```
