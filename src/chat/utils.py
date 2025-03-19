"""Chapiana chat helpers."""
import pycountry

def get_country_name_choices():
    """
    Gives a sorted list of tuples (country_code, country_name).
    """
    countries = [(country.alpha_2, country.name) for country in pycountry.countries]
    return sorted(countries, key=lambda x: x[1])

def get_country_code_by_name(country_name):
    """
    Gives the ISO Alpha-2 country code given a country name.
    """
    country = pycountry.countries.get(name=country_name)
    if country:
        return country.alpha_2
    
    # If direct lookup fails
    matches = [c for c in pycountry.countries if country_name.lower() in c.name.lower()]
    if matches:
        return matches[0].alpha_2
    
    return None
