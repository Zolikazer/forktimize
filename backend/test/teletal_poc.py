import time
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from requests import Session

url = "https://www.teletal.hu/etlap"
headers = {
    "User-Agent": "Mozilla/5.0"
}


def find_static_codes(soup : BeautifulSoup) -> list:
    tr_elements = soup.find_all("tr", attrs={"kod": True})
    codes = []
    for tr in tr_elements:
        kod_value = tr["kod"]
        print("🍜 Found kod:", kod_value)
        codes.append(kod_value)

    return codes



def get_sections(soup : BeautifulSoup) -> list:
    section_elements = soup.find_all("section", attrs={"ewid": True, "ev": True, "het": True, "section": True})
    sections = []
    for section in section_elements:
        section_info = {
            "ewid": section["ewid"],
            "ev": section["ev"],
            "het": section["het"],
            "varname": section["section"],  # this gets used in the AJAX URL
        }
        sections.append(section_info)
        print(f"📦 Found section: {section_info}")

    return sections


def fetch_codes_from_sections(session: Session, sections: list[dict], delay: float = 0.3) -> list[str]:
    ajax_url = "https://www.teletal.hu/ajax/szekcio"
    all_codes = []

    for section in sections:
        try:
            params = {
                "ev": section["ev"],
                "het": section["het"],
                "ewid": section["ewid"],
                "varname": section["varname"],
            }
            full_url = f"{ajax_url}?{urlencode(params)}"
            print(f"🌐 Fetching dynamic section: {full_url}")

            response = session.get(full_url, headers=headers, timeout=30)
            response.raise_for_status()

            section_soup = BeautifulSoup(response.text, "html.parser")
            tr_elements = section_soup.find_all("tr", attrs={"kod": True})

            for tr in tr_elements:
                kod_value = tr["kod"]
                print("🍕 Found dynamic kod:", kod_value)
                all_codes.append(kod_value)

            time.sleep(delay)

        except Exception as e:
            print(f"❌ Failed to fetch section {section['varname']}: {e}")

    return all_codes


def fetch_food_details(session: requests.Session, codes: list[str], year: int, week: int, day: int = 1, delay: float = 0.3) -> list[str]:
    food_url = "https://www.teletal.hu/ajax/kodinfo"
    results = []

    for kod in codes:
        try:
            params = {
                "ev": year,
                "het": week,
                "tipus": 1,  # just keeping it default
                "nap": day,
                "kod": kod
            }

            print(f"🥩 Fetching details for {kod}...")
            res = session.get(food_url, params=params, timeout=30)
            res.raise_for_status()

            html = res.text
            print(f"✅ Got response for {kod} (length={len(html)} chars)")
            results.append(html)
            print(html)

            time.sleep(delay)
        except Exception as e:
            print(f"❌ Failed to fetch details for {kod}: {e}")

    return results



if __name__ == "__main__":
    session = requests.Session()
    session.headers.update(headers)

    res = session.get(url, headers=headers)
    print(res.text)

    soup = BeautifulSoup(res.text, "html.parser")
    static_codes = find_static_codes(soup)
    sections = get_sections(soup)
    dynamic_codes = fetch_codes_from_sections(session, sections)
    print(static_codes)
    print(dynamic_codes)
    all_codes = set(static_codes + dynamic_codes)
    print(all_codes)

    year = 2025
    week = 16
    food_details_html = fetch_food_details(session, all_codes, year, week)

    print(f"🍽️ Successfully fetched {len(food_details_html)} food detail responses.")

