# House Age Search

This repository uses open data such as [Price Paid Data](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads#single-file) from HM Land Registry to provide a searchable, visualised dataset of houses in England.

For postcodes and latitudes/longitudes, this repository uses combined postcode data from [GeoNames](https://download.geonames.org/) as well as [Doogal](https://www.doogal.co.uk/).

The combined data is approximately 4.5 GB in size, holding almost 27 million records.

## Docker Script
```
docker build -t house-age-search-api:latest . -f api.dockerfile
docker build -t house-age-search-website:latest . -f website.dockerfile
docker-compose -p "house-age-search-stack" up -d 
```