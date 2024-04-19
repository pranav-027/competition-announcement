import json
import requests
import datetime
from bs4 import BeautifulSoup
import pytz

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
    "sq1": "Square1",
    "444bf": "4x4 BLD",
    "555bf": "5x5 BLD",
    "333mbf": "3x3 MBLD",
}

# to generate google maps link for the coordinates
def generate_google_maps_link(latitude, longitude):
    base_url = "https://www.google.com/maps"
    coordinates = f"{latitude},{longitude}"
    maps_link = f"{base_url}/?q={coordinates}"
    return maps_link

def get_competition_message(competition_url):

    api_url = competition_url.replace('/competitions/', '/api/v0/competitions/')

    # takes the json and loads it in comps variable
    req = requests.get(api_url)
    comp = json.loads(req.text)


    # COMPETITION NAME
    compURL = comp["url"]

    # ORGANIZERS
    i = 0
    compOrganizers = ""
    for organizer in comp["organizers"]:
        i += 1
        compOrganizers += organizer["name"]
        if not len(comp["organizers"]) == i:
            compOrganizers += ", "

    # DATE
    startDate = datetime.date.fromisoformat(comp["start_date"])
    endDate = datetime.date.fromisoformat(comp["end_date"])
    compDate = ""
    if startDate == endDate:
        compDate = startDate.strftime("%B %d, %Y | %A")
    else:
            compDate = (
            startDate.strftime("%B %d")
            + endDate.strftime("-%d, %Y")
            + " | "
            + startDate.strftime("%a")
            + "-"
            + endDate.strftime("%a")
        )

    # VENUE
    if not comp["venue_details"] == "":
        compVenueAndDetails = comp["venue_address"] + " | " + comp["venue_details"]
    else:
        compVenueAndDetails = comp["venue_address"]

    compVenueLink = generate_google_maps_link(
            comp["latitude_degrees"], comp["longitude_degrees"]
        )

    # EVENTS
    i = 0
    compEvents = ""
    for event in comp["event_ids"]:
        i += 1
        compEvents += eventsDict[event]
        if not len(comp["event_ids"]) == i:
             compEvents += ", "

    # COMPETITOR LIMIT
    compLimit = comp["competitor_limit"]

    # BASE FEE
    baseFee = comp["base_entry_fee_lowest_denomination"]
    baseFeeInt = int(baseFee/100)

    # REGISTRATION OPENS FROM
    regStartsFrom = datetime.datetime.fromisoformat(comp["registration_open"]).astimezone(pytz.timezone("Asia/Kolkata"))
    compRegStartsFrom = regStartsFrom.strftime("%a | %B %d, %Y at %I:%M %p")

    # CONTACT
    reqComp = requests.get(comp["url"])
    soup = BeautifulSoup(reqComp.text, "html.parser")

    try:
        contactLink = (
            soup.find("dt", string="Contact").find_next_sibling().find("a").get("href")
        )
    except (AttributeError, KeyError, TypeError):
        contactLink = ""

    if contactLink.startswith("/"):
        contactLink = "https://www.worldcubeassociation.org" + contactLink
    elif "mailto:" in contactLink:
        contactLink = contactLink.replace("mailto:", "")
    else:
        contactLink = compURL

    compWhatsAppMessage = (
        "*Competition Announcement*"
        + "\n"
        + str(compURL)
        + "\n\n"
        + "*Organizers:*"
        + "\n"
        + str(compOrganizers)
        + "\n\n"
        + "*Date:*"
        + "\n"
        + str(compDate)
        + "\n\n"
        + "*Venue:*"
        + "\n"
        + str(compVenueAndDetails)
        + "\n"
        + str(compVenueLink)
        + "\n\n"
        + "*Events:*"
        + "\n"
        + str(compEvents)
        + "\n\n"
        + "*Competitor Limit:*"
        + "\n"
        + str(compLimit)
        + "\n\n"
        + "*Base Registration Fee:*"
        + "\n"
        + "\u20B9 "
        + str(baseFeeInt)
        + "\n\n"
        + "*Registration Starts From:*"
        + "\n"
        + str(compRegStartsFrom)
        + "\n\n"
        + "*Contact:*"
        + "\n"
        + str(contactLink)
        + "\n\n\n"
    )
    return compWhatsAppMessage

def get_competition_fb_message(competition_url):

    api_url = competition_url.replace('/competitions/', '/api/v0/competitions/')

    # takes the json and loads it in comps variable
    req = requests.get(api_url)
    comp = json.loads(req.text)


    # COMPETITION NAME
    compName = comp["name"]
    compURL = comp["url"]

    # DATE
    startDate = datetime.date.fromisoformat(comp["start_date"])
    endDate = datetime.date.fromisoformat(comp["end_date"])
    compDate = ""
    if startDate == endDate:
        compDate = startDate.strftime("%B %d, %Y | %A")
    else:
            compDate = (
            startDate.strftime("%B %d")
            + endDate.strftime("-%d, %Y")
            + " | "
            + startDate.strftime("%a")
            + "-"
            + endDate.strftime("%a")
        )

    # VENUE
    if not comp["venue_details"] == "":
        compVenueAndDetails = comp["venue_address"] + " | " + comp["venue_details"]
    else:
        compVenueAndDetails = comp["venue_address"]

    compVenueLink = generate_google_maps_link(
            comp["latitude_degrees"], comp["longitude_degrees"]
        )

    # EVENTS
    i = 0
    compEvents = ""
    for event in comp["event_ids"]:
        i += 1
        compEvents += eventsDict[event]
        if not len(comp["event_ids"]) == i:
             compEvents += ", "

    # COMPETITOR LIMIT
    compLimit = comp["competitor_limit"]

    # REGISTRATION OPENS FROM

    regStartsFrom = datetime.datetime.fromisoformat(comp["registration_open"]).astimezone(pytz.timezone("Asia/Kolkata"))
    compRegStartsFrom = regStartsFrom.strftime("%a | %B %d, %Y at %I:%M %p")

    compFbMessage = (
        "[Competition Announcement]"
        + "\n\n"
        + str(compName)
        + "\n\n"
        + "Date:"
        + "\n"
        + str(compDate)
        + "\n\n"
        + "Venue:"
        + "\n"
        + str(compVenueAndDetails)
        + "\n"
        + str(compVenueLink)
        + "\n\n"
        + "Events:"
        + "\n"
        + str(compEvents)
        + "\n\n"
        + "Competitor Limit:"
        + "\n"
        + str(compLimit)
        + "\n\n"
        + "Registration Starts From:"
        + "\n"
        + str(compRegStartsFrom)
        + "\n\n"
        + "Happy Cubing! 🧩"
        + "\n\n"
        + str(compURL)
        + "\n\n"
    )
    return compFbMessage