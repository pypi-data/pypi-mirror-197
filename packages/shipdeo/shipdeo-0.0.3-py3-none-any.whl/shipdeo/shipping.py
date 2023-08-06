import json
import requests
from auth import ShipdeoAuth
from dto import BaseAddressDto, DestinationDto, ItemDto, OriginDto

client_id = '7jgf8StrQRbuE8kJ'
client_secret = 'Eylh4kRbvz3PQNm1'

ShipdeoAuth(client_id=client_id, client_secret=client_secret)


class IShipping:

    def get_tariff(self, origin, destination, couriers=[], is_cod=False, items=None):
        pass

    def get_airwaybill_info(self, airwaybill: str):
        pass


class ShipdeoService(IShipping):

    def __init__(self, token, BASE_URL='https://main-api-production.shipdeo.com', request=None) -> None:
        self.__token = token
        self.__base_url = BASE_URL
        self.__requests = request or requests
        self.__headers = {
            'Authorization': 'Bearer ' + self.__token,
            'Content-Type': 'application/json'
        }
        super().__init__()
        

    def __build_payload_tariff(self, origin: BaseAddressDto, destination: BaseAddressDto, couriers, is_cod, items=None):
        return {
            "couriers": couriers,
            "is_cod": is_cod,
            "origin_lat": origin.lat,
            "origin_long": origin.long,
            "origin_province_name": origin.province_name,
            "origin_subdistrict_code": origin.subdistrict_code,
            "origin_subdistrict_name": origin.subdistrict_name,
            "origin_city_code": origin.city_code,
            "origin_city_name": origin.city_name,
            "origin_postal_code": origin.postal_code,
            "destination_lat": destination.lat,
            "destination_long": destination.long,
            "destination_province_name": destination.province_name,
            "destination_subdistrict_code": destination.subdistrict_code,
            "destination_subdistrict_name": destination.subdistrict_name,
            "destination_city_code": destination.city_code,
            "destination_city_name": destination.city_name,
            "destination_postal_code": destination.postal_code,
            "items": items,
            "isCallWeight": False
        }


    def get_tariff(self, origin: BaseAddressDto, destination: BaseAddressDto, couriers, is_cod, items=None):
       
        payload =  self.__build_payload_tariff(origin, destination, couriers, is_cod, items=items)
        respond = self.__requests.post(self.__base_url + '/v1/couriers/pricing', data=json.dumps(payload), headers=self.__headers)
        
        if respond.status_code == 200:
            return respond.json()
        else:
            raise Exception(respond.json())
        

if __name__ == '__main__':
    auth = ShipdeoAuth(client_id=client_id, client_secret=client_secret)
    # print(auth.get_token())
    token = "3bec2a11ae1222cb7f2264f0aa25dffc6126c621"
    shipdeo = ShipdeoService(token)

    origin = OriginDto()
    origin.subdistrict_code = "32.77.01"
    origin.subdistrict_name = "CIMAHI SELATAN"
    origin.city_code = "32.77"
    origin.city_name = "CIMAHI"
    origin.province_code = "32"
    origin.province_name = "JAWA BARAT"
    origin.postal_code = "40532"


    destination = DestinationDto()
    destination.subdistrict_code = "32.77.01"
    destination.subdistrict_name = "CIMAHI SELATAN"
    destination.city_code = "32.77"
    destination.city_name = "CIMAHI"
    destination.province_code = "32"
    destination.province_name = "JAWA BARAT"
    destination.postal_code = "40532"

    items = []
    item = ItemDto()
    item.weight = 10
    item.description = 'baju'
    item.dimension_uom = 'cm'
    item.height = 0 
    item.width = 0 
    item.is_wood_package = False
    item.length = 0
    item.name = 'SKU001'
    item.qty = 10
    item.value = 10000
    item.weight = 8
    item.weight_uom = 'gram'
    
    

    items.append(item.__dict__)
    result = shipdeo.get_tariff(origin=origin, destination=destination, couriers=["sap"], is_cod=False, items=items)
    print(result['data'])
