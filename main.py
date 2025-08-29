from chizhik_api import ChizhikAPI


with ChizhikAPI() as API:
    result = API.Geolocation.cities_list(search_name='ар', page=1)
    #print(result.text)
