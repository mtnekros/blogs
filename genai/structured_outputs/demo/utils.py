import time
from collections.abc import Callable
from typing import Any

import requests
from bs4 import BeautifulSoup

le_sherpa_url = "https://lesherpa.com.np/about"
restaurant_url = le_sherpa_url

def get_scraped_content(url: str) -> str:
    """Scrape given url & return the text."""
    res = requests.get(url, timeout=100)
    soup = BeautifulSoup(res.content, "html.parser")
    for script_or_style in soup(['script', 'style', 'img']):
        script_or_style.decompose()
    return soup.get_text()


def time_it(func: Callable) -> Callable:
    """Return a wrapper that will log function execution time."""
    def _wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        t1 = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"Time taken by {func.__name__}: {time.perf_counter()-t1:.3f} sec(s).")
        return result
    return _wrapper


scraped_content = """
Commitment to Quality and Taste    Collaborating with international chefs and restaurateur                                                                                               r
s, we have established a new menu and philosophy around supporting local producers in a safe and
sustainable way to encourage the development of standardized and trusted produce in Nepal.

Spread across eight ropanis (approximately one acre), Le Sherpa’s estate
comprises of a variety of f interesting shops supporting creative, local brands
– from coffee and food to crafts. There is an n intimate boutique bed &
breakfast, The Museum with spacious and stylish rooms offering all amenit ties.
This small oasis offers a platform for local artisans, supporting and
sustaining struggling a artists, craftsmen and local products; supporting the
tradition and culture of Nepal.Located away from the hustle and bustle of the
daily commotion of Kathmandu, you can find refuge i in this cozy get away.
Enjoy fresh, organic food in the Le Sherpa Restaurant, while your time away
hanging around the boutique shops, or simply enjoy a fresh cup of Everfresh
–local Nuwa Estate Coffee.

Contact dine@lesherpa.com.np 01-4528604

For Reservation
     Call us at: +977-9801159480,01-4528604

Opening Hour
        Opening Hours: 11 AM - 10 PM (Monday to Friday)
Brunch: 8 AM - 1 PM (Saturday and Sunday)
Prior reservation is required for Breakfast
Location
       Maharajgunj, KTM, Nepal
Opposite of President House
The Le-Sherpa Restaurant • Website by Curves n’ Colors
"""
