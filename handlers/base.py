import aiohttp
from config import rest_api


async def is_user_registered(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{rest_api}/user/?user_id={user_id}') as resp:
            data = await resp.json()
            if data:
                return data
            else:
                return False
            
async def is_address_registered(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{rest_api}/address/?user__user_id={user_id}') as resp:
            data = await resp.json()
            if data:
                return data
            else:
                return False
            

async def add_user(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{rest_api}/user/', json=data) as resp:
            if resp.status == 201:
                return True
            else:
                return False
            
async def add_address(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{rest_api}/address/', data=data) as resp:
            if resp.status == 201:
                return True
            else:
                return False
            

            

async def add_num_car(data_car):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{rest_api}/number_car/', data=data_car) as resp:
            if resp.status == 201:
                return True
            else:
                return False
            

async def message_car_num(car_num):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{rest_api}/number_car/?car_num={car_num}') as resp:

            data = await resp.json()
            user_id = [response['user_id'] for response in data]

            # if user_id:
            return user_id
            # else:
            #     return False


async def get_number_car(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{rest_api}/number_car/?user__user_id={user_id}') as resp:
            data = await resp.json()
            car_number = [response['car_num'] for response in data]

            if car_number:
                return car_number
            else:
                return False

async def get_number_car_check(user_id, car_numbers):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{rest_api}/number_car/?user__user_id={user_id}&car_num={car_numbers}') as resp:
            data = await resp.json()
            car_number = [response['car_num'] for response in data]

            if car_number:
                return car_number
            else:
                return False
            

async def get_address(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{rest_api}/address/?user__user_id={user_id}') as resp:
            data = await resp.json()
            address = [response for response in data]

            if address:
                return address
            else:
                return False




async def deleted_num_car(user_id, car_num):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{rest_api}/number_car/?user__user_id={user_id}&car_num={car_num}') as resp:
            data = await resp.json()
            id_car = [response['id'] for response in data]
            if id_car:
                async with session.delete(f'{rest_api}/number_car/{id_car[0]}/') as resp:
                    if resp.status == 204:
                        return True
                    else:
                        return False
                    
                    
async def deleted_address(id_address, user_id):
    async with aiohttp.ClientSession() as session:
        async with session.delete(f'{rest_api}/address/{id_address}/?user__user_id={user_id}') as resp:
            if resp.status == 204:
                return True
            else:
                return False
                    


            
async def post_dadata(headers, url, data):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data=data) as resp:
            if resp.status == 200:
                result = await resp.json()
                suggestions = result.get('suggestions', [])
                if len(suggestions) > 0:
                    suggested_address = suggestions[0]['data']
                    city = suggested_address.get('city')
                    return city
                else:
                    return False
            else:
                return False


async def post_dadata_street(headers, url, data):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data=data) as resp:
            if resp.status == 200:
                result = await resp.json()
                suggestions = result.get('suggestions', [])
                if len(suggestions) > 0:
                    suggested_address = suggestions[0]['data']
                    street = suggested_address.get('street')
                    print(street)
                    return street
                else:
                    return False
            else:
                return False
            