# FIR API CLI

FIR API CLI is a command line interface tool for exploring and downloading
Sentinel satellite images from the FIR API service.

The tool can be used to explore and download dataset based on product 
id or metadata filtering.

In order to use the package, users must have a
valid FIR eFöld registration.

More information at: https://efold.gov.hu/

## Installation

```bash
pip install fir-cli
```


## Usage

Get some help:

```bash
fir-cli --help
```

Save username and password to config file (if executed, no need to support username and password to commands):

```bash
fir-cli config <username> <password>
```

Get information about individual product based on product id:

```bash
fir-cli -u <username> -pw <password> query-id -i <product_id>
```

Download individual product based on product id:

```bash
fir-cli -u <username> -pw <password> query-id -i <product_id> -d <path/to/folder>
```

Get information about products based on query:

```bash
fir-cli -u <username> -pw <password> query -p Sentinel-2 -dt 2021-01-01 2021-01-05 -c 1
```

Download products based on query and save product list to csv:

```bash
fir-cli -u <username> -pw <password> query -p Sentinel-2 -dt 2021-01-01 2021-01-05 -c 1 -d <path/to/folder> -o <path/to/csv_file.csv>
```
*Note: username and password can be automatically supplied by setting the FIR_API_USERNAME and FIR_API_PASSWORD environment variables or by running the config command.*
