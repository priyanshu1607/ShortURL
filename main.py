from fastapi import FastAPI, Request, Response, Depends
app = FastAPI()
from fastapi.responses import RedirectResponse
import secrets
from constants import HOST
from database.models import URL 
from datetime import datetime 
from database.database import URL_collection
from redis_client import setInRedis, getFromRedis
from pymongo.errors import DuplicateKeyError

import string

ALPHABET = string.ascii_letters + string.digits

def generate_unique_slug(length=6):
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


async def init_db():
    await URL_collection.create_index(
        "shortURL",
        unique=True
    )
@app.get("/")
async def apiList():
    return {"message": "Hello World"}

@app.post('/url')
async def shortenURL(item:dict, request: Request):
    try: 
        short_slug = item.get('alies') or generate_unique_slug()
        tinyurl = await URL_collection.find_one({'Longurl': item['url']})
        if tinyurl:
            return (tinyurl['shortURL']) 
        expires_at = datetime.strptime(item['Expires_at'], "%Y-%m-%d %H:%M:%S") if item.get('Expires_at') else None
        url_dict = URL(
                    expires_at = expires_at,
                    Longurl =  item['url'], 
                    shortURL =  'http://' +f'{HOST}/{short_slug}'
        ) 
        result = url_dict.model_dump(mode="json")
        setInRedis(result['shortURL'],result['Longurl'])
        await URL_collection.insert_one(result)
        return {f"{HOST}/{short_slug}"}
    except DuplicateKeyError:
         pass
        
    except Exception as e:
            print(e)
            return Response("Error occured", 502)
    
    
async def analytic():
    pass

 
@app.get('/{URL}')
async def getorignalURL(URL: Request):
    try:
        # host = URL.headers["host"]  
        url = str(URL.url)
        urlcollection = getFromRedis(url)
        if urlcollection:
            await URL_collection.update_one({'shortURL': url}, {"$inc": {"click": 1}} )
            # analytic()
            
            return RedirectResponse(urlcollection, status_code=302)
        
        urlcollection = await URL_collection.find_one({'shortURL': url})
        
        if urlcollection["expires_at"]:
            expires_at = datetime.fromisoformat(urlcollection["expires_at"])
            if expires_at < datetime.now():
                return Response("URL Expierd", status_code=410)
            
        if urlcollection:
            await URL_collection.update_one({'_id': urlcollection['_id']}, {"$inc": {"click": 1}} )
            # analytic()
            return RedirectResponse(urlcollection['Longurl'], status_code=302)
        return Response("URL not found in db", status_code=404)
    except Exception as e:
        return Response("Error occured", status_code=502)
        
    

@app.delete('/deleteURL')
async def deleteSHortURL(item:dict, request: Request):
    try:
        tinyurl = await URL_collection.find_one({'Longurl': item['url']})
        if tinyurl:
            await URL_collection.delete_one({"_id": tinyurl['_id']})
            return Response('URL deleted')
        return Response('URL not deleted', 404)
    except Exception as e:
        return Response('URL not deleted', 502)
    
@app.get('/health')
async def healthcheck():
    try:
        return Response('status: Running', 200)
    except Exception as e:
        return Response('Error encounted', 502)