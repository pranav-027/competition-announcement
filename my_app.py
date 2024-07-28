import json
import requests
import datetime
from bs4 import BeautifulSoup
import pytz
from babel.numbers import get_currency_symbol

eventsDict = {
    "333": "3x3",
    "222": "2x2",
    "444": "4x4",
    "555": "5x5",
    "666": "6x6",
    "777": "7x7",
    "333bf": "3x3 BLD",
    "333fm": "3x3 FMC",
    "333oh": "3x3 OH",
    "clock": "Clock",
    "minx": "Megaminx",
    "pyram": "Pyraminx",
    "skewb": "Skewb",
    "sq1": "Square-1",
    "444bf": "4x4 BLD",
    "555bf": "5x5 BLD",
    "333mbf": "3x3 MBLD",
}

# to generate google maps link for the coordinates
def generate_google_maps_link(latitude, longitude):
    return f"https://www.google.com/maps/?q={latitude},{longitude}"

def fetch_competition_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching competition data: {e}")
        return None

def fetch_contact_link(comp_url):
    try:
        response = requests.get(comp_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        contact_link = soup.find("dt", string="Contact").find_next_sibling().find("a").get("href")
        if contact_link.startswith("/"):
            contact_link = "https://www.worldcubeassociation.org" + contact_link
        elif "mailto:" in contact_link:
            contact_link = contact_link.replace("mailto:", "")
        else:
            contact_link = comp_url
        return contact_link
    except (requests.exceptions.RequestException, AttributeError, KeyError, TypeError) as e:
        print(f"Error fetching contact link: {e}")
        return comp_url

def format_date_range(start_date, end_date):
    if start_date == end_date:
        return start_date.strftime("%B %d, %Y | %A")
    return (
        f"{start_date.strftime('%B %d')}-{end_date.strftime('%d, %Y')} | "
        f"{start_date.strftime('%a')}-{end_date.strftime('%a')}"
    )

def get_competition_message(competition_url):
    api_url = competition_url.replace('/competitions/', '/api/v0/competitions/')
    comp = fetch_competition_data(api_url)
    if not comp:
        return ""

    comp_url = comp["url"]
    comp_organizers = ", ".join([organizer["name"] for organizer in comp["organizers"]])
    start_date = datetime.date.fromisoformat(comp["start_date"])
    end_date = datetime.date.fromisoformat(comp["end_date"])
    comp_date = format_date_range(start_date, end_date)
    comp_venue_and_details = f"{comp['venue_address']} | {comp['venue_details']}" if comp["venue_details"] else comp["venue_address"]
    comp_venue_link = generate_google_maps_link(comp["latitude_degrees"], comp["longitude_degrees"])
    comp_events = ", ".join([eventsDict[event] for event in comp["event_ids"]])
    comp_limit = comp["competitor_limit"]
    currency_symbol = get_currency_symbol(comp["currency_code"])
    base_fee_int = int(comp["base_entry_fee_lowest_denomination"] / 100)
    reg_starts_from = datetime.datetime.fromisoformat(comp["registration_open"]).astimezone(pytz.timezone("Asia/Kolkata"))
    comp_reg_starts_from = reg_starts_from.strftime("%a | %B %d, %Y at %I:%M %p")
    contact_link = fetch_contact_link(comp_url)

    comp_whatsapp_message = (
        f"*Competition Announcement*\n"
        f"{comp_url}\n\n"
        f"*Organizers:*\n{comp_organizers}\n\n"
        f"*Date:*\n{comp_date}\n\n"
        f"*Venue:*\n{comp_venue_and_details}\n{comp_venue_link}\n\n"
        f"*Events:*\n{comp_events}\n\n"
        f"*Competitor Limit:*\n{comp_limit}\n\n"
        f"*Base Registration Fee:*\n{currency_symbol} {base_fee_int}\n\n"
        f"*Registration Starts From:*\n{comp_reg_starts_from}\n\n"
        f"*Contact:*\n{contact_link}\n\n\n"
    )
    return comp_whatsapp_message

def get_competition_fb_message(competition_url):
    api_url = competition_url.replace('/competitions/', '/api/v0/competitions/')
    comp = fetch_competition_data(api_url)
    if not comp:
        return ""

    comp_name = comp["name"]
    comp_url = comp["url"]
    start_date = datetime.date.fromisoformat(comp["start_date"])
    end_date = datetime.date.fromisoformat(comp["end_date"])
    comp_date = format_date_range(start_date, end_date)
    comp_venue_and_details = f"{comp['venue_address']} | {comp['venue_details']}" if comp["venue_details"] else comp["venue_address"]
    comp_events = ", ".join([eventsDict[event] for event in comp["event_ids"]])
    comp_limit = comp["competitor_limit"]
    reg_starts_from = datetime.datetime.fromisoformat(comp["registration_open"]).astimezone(pytz.timezone("Asia/Kolkata"))
    comp_reg_starts_from = reg_starts_from.strftime("%a | %B %d, %Y at %I:%M %p")

    comp_fb_message = (
        "[Competition Announcement]\n\n"
        f"{comp_name}\n\n"
        f"Date:\n{comp_date}\n\n"
        f"Venue:\n{comp_venue_and_details}\n\n"
        f"Events:\n{comp_events}\n\n"
        f"Competitor Limit:\n{comp_limit}\n\n"
        f"Registration Starts From:\n{comp_reg_starts_from}\n\n"
        f"Happy Cubing! 🧩\n\n"
        f"{comp_url}\n\n"
    )
    return comp_fb_message
