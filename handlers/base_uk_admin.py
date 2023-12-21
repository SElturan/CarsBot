import aiohttp
from config import rest_api


async def message_street(user_id,street,house_number):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{rest_api}/address_uk/?user__user_id={user_id}&address__address={street}&house_number={house_number}') as resp:

            data = await resp.json()
            user_id = [response['user_id'] for response in data]

            # if user_id:
            return user_id
            # else:
            #     return False


async def get_addres_uk(street, house_number):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{rest_api}/address/?address={street}&house_number={house_number}') as resp:

            data = await resp.json()
            user_id = [response['user_id'] for response in data]

            # if user_id:
            return user_id
            # else:
            #     return False

async def get_template_text(template_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{rest_api}/template/?template_id={template_id}') as resp:

            data = await resp.json()
            text = [response['template'] for response in data]

            return text

async def message_house(user_id,house):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{rest_api}/address_uk/?user__user_id={user_id}&address__house_number={house}') as resp:

            data = await resp.json()
            user_id = [response['user_id'] for response in data]

            # if user_id:
            return user_id
            # else:
            #     return False


async def get_house_uk(house):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{rest_api}/address/?house_number={house}') as resp:

            data = await resp.json()
            user_id = [response['user_id'] for response in data]

            # if user_id:
            return user_id
            # else:
            #     return False



async def get_address_list(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{rest_api}/address_uk/?user__user_id={user_id}') as resp:

            data = await resp.json()
            adress_uk = [response['address'] for response in data] 

            if adress_uk:
                return adress_uk
            else:
                return False
            
async def get_all_user():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{rest_api}/user/") as resp:
            data =  await resp.json()
            user_id = [response['user_id'] for response in data]
            return user_id


async def get_uk_nick(user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{rest_api}/address_uk/?user__user_id={user_id}") as resp:
            data =  await resp.json()
            nick = [response['nick'] for response in data]
            
            if nick and nick == None:
                return nick
            else:
                return False
        
