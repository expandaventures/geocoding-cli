import csv
import os
import re
import requests
import time

API_KEY = os.getenv("GOOGLE_API_KEY", False)
LIMIT_LON = tuple(map(float, os.getenv("LIMIT_LON", "-117.12776,14.5388286402").split(',')))
LIMIT_LAT = tuple(map(float, os.getenv("LIMIT_LAT", "-86.811982388,32.72083").split(',')))


def clean_and_format(string):
    return "+".join(string.strip().split(" ")).replace("++", "")


def extract_cp(string):
    cp_str = ""
    cp_search = re.search("C.P.[0-9]{5}", string)
    if cp_search:
        cp_str = cp_search.group(0)
        cp_str = cp_str.replace("C.P.", "")
    return cp_str


def get_location_by_address(state, city, address_string=None, dry_run=False):
    if address_string:
        address_string = re.sub(r'ENTRE\s(.*)\sY\s(.*)\sCOLONIA:', 'COLONIA:', address_string)
        address_string = address_string.replace("C.P.", "postal_code=")
        address_string = address_string.replace("COLONIA:  postal_code=", "postal_code=")
        address_string = clean_and_format(address_string)
        address_string = "{}+{}+{}".format(clean_and_format(state), clean_and_format(city), address_string)
    else:
        address_string = "{}+{}".format(clean_and_format(state), clean_and_format(city))

    url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&region=mx&key={}".format(address_string,
                                                                                                 API_KEY)
    if dry_run:
        print(url)
        return None, None
    response = requests.get(url)
    try:
        if response.status_code == 200:
            json_response = response.json()
            results = json_response.get("results", [])
            for result in results[:1]:
                for key, data in result.items():
                    if "geometry" in key:
                        location = data.get("location", {})
                        return location.get("lat"), location.get("lng")
    except Exception as e:
        print("Exception", e)
    return None, None


def process_file(file_path, output_name, dry_run=False):
    if not API_KEY and not dry_run:
        raise ValueError("Environment Variable GOOGLE_API_KEY must be set")
    start = time.time()
    with open(file_path) as f:
        csv_data = csv.reader(f, delimiter=',', quotechar='"')
        rows = list(csv_data)
        rows[0].append("Latitud")
        rows[0].append("Longitud")
        for row in rows[1:]:
            address = row[-1]
            cp = extract_cp(address)
            lat, lng = get_location_by_address(row[1], row[3], address_string=address, dry_run=dry_run)
            if (not lat and not lng) or (
                    (LIMIT_LAT[0] > lat > LIMIT_LAT[1]) and (LIMIT_LON[0] > lng > LIMIT_LON[1])):
                lat, lng = get_location_by_address(row[1], row[3], address_string=cp, dry_run=dry_run)
            row.append(lat)
            row.append(lng)
            print(row[0], lat, lng)
            if dry_run:
                return 0

    with open(output_name, 'w', newline='') as csvfile:
        csv_file = csv.writer(csvfile, delimiter=',',
                              quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_file.writerows(rows)
    end = time.time()
    print(end - start)
    return len(rows)
