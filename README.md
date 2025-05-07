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
    "socks5://uiZfffH0iTzj7fEN:mobile;in;;;@proxy.froxy.com:9168",
    "socks5://uiZfffH0iTzj7fEN:mobile;in;;;@proxy.froxy.com:9168"
  ],
  "type": "Repositories"
}
```


```bash
python main.py --file=input_file.json
# or
python main.py -f input_file.json
```
