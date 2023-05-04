#!/usr/bin/env python3
"""
pip3 install geoip2
I use mmdb file from https://db-ip.com/db/download/ip-to-country-lite
Make sure that the script is executable (chmod +x /opt/geolocate/geoip_lookup.py )
use example https://allwork.kyiv.ua/2023/05/04/geolocation-for-ip/
print(country_code, end = '') - optimization for exim config file cjmpare stament, because print add symbol '\n'
in line iso_code.strip() - the same purposes
"""
import sys
import geoip2.database

# Replace this with the path to your GeoIP database file
GEOIP_DB_FILE = '/opt/geolocate/ipdb202305.mmdb'

# Open the GeoIP database file
geoip_reader = geoip2.database.Reader(GEOIP_DB_FILE)

# Get the IP address from the command-line arguments
ip_address = sys.argv[1]

try:
    # Look up the IP address in the GeoIP database


    # Get the country code from the GeoIP response
    country_code = geoip_reader.country(ip_address).country.iso_code.strip()  # .name

except geoip2.errors.AddressNotFoundError:
    # IP address not found in the GeoIP database
    country_code = 'unknown'

# Output the country code
print(country_code, end = '')
