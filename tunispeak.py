import requests
import json
def transform_tun_to_en(text_tun):
    """Translate Tunisian Arabic to English using the TUNISPEAK model"""
    url_tunispeak="http://10.2.1.130:10000/tn_2_en"
    try:
        response = requests.post(f"{url_tunispeak}?text={text_tun}",timeout=500)
        if response.status_code == 200:
                return response.json() 
        else:
                return f"Error: Status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


def transform_en_to_tun(text_en):
    """Translate Tunisian Arabic to English using the TUNISPEAK model"""

    url_tunispeak="http://10.2.1.130:10000/en_2_tn"
    response = requests.post(f"{url_tunispeak}?text={text_en}")
    try:
        response = requests.post(f"{url_tunispeak}?text={text_en}",timeout=500)
        if response.status_code == 200:
                return response.json() 
        else:
                return f"Error: Status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


# res=transform_tun_to_en("شنو أحوالك حنبعل")
# print(res)