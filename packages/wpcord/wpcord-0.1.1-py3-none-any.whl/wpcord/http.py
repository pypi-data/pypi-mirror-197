import aiohttp
import asyncio
from enum import Enum
import json
from typing import Any, Callable, Optional, Union, List
from aiohttp import ClientSession, ClientResponse, TCPConnector

from .enums import WPCordEnum

class HTTPMethod(WPCordEnum):
    delete = "DELETE"
    get    = "GET"
    head   = "HEAD"
    patch  = "PATCH"
    post   = "POST"
    put    = "PUT"
    

class HTTPResponse:
    def __init__(self, client_response: ClientResponse, text: str) -> None:
        self.client_response = client_response
        self.text: str = text
        self.status = client_response.status
        self.ok: bool = client_response.ok
    
    def json(self, decoder: Any = json.loads, **decode_options) -> Optional[Any]:
        try:
            return decoder(self.text, **decode_options)
        except:
            return None

HTTPResults = Union[List[Union[HTTPResponse, Any]], HTTPResponse, Any]

class HTTPClient:
    def __init__(self,
        base_url: Optional[str] = None,
        session: Optional[ClientSession] = None,
        convert_response: Optional[Callable] = None,
    ) -> None:
        self.base_url = base_url
        self.convert_response = convert_response
        self.session: ClientSession = session or ClientSession()
        self.results: List[HTTPResults] = []
        self.last_results: HTTPResults = None

    async def request(self,
        method: str,
        *urls: str,
        convert_response: Optional[Callable] = None, 
        **request_options
    ) -> HTTPResults:
        results = []
        async def _request(url):
            async with self.session.request(str(method), url, **request_options) as response:
                text = await response.read()
                result = HTTPResponse(response, text)
                if convert_response is not None:
                    result = convert_response(result)
                elif self.convert_response is not None:
                    result = self.convert_response(result)
                results.append(result)
                response.close()

        if len(urls) > 1:
            tasks = [
                asyncio.ensure_future(_request((self.base_url or "") + url))
                for url in urls
            ]
            await asyncio.gather(*tasks)
        else:
            await _request((self.base_url or "") + urls[0])
                
        result = results[0] if len(results) == 1 else results
        self.results.append(results)
        self.last_results = results
        return result


        
    async def delete(self, *urls, **kwargs):
        return await self.request("DELETE", *urls, **kwargs)

    async def head(self, *urls, **kwargs):
        return await self.request("HEAD", *urls, **kwargs)

    async def get(self, *urls, **kwargs):
        return await self.request("GET", *urls, **kwargs)

    async def patch(self, *urls, data = None, **kwargs):
        return await self.request("PATCH", *urls, data=data, **kwargs)

    async def post(self, *urls, data = None, **kwargs):
        return await self.request("POST", *urls, data=data, **kwargs)

    async def put(self, *urls, data = None, **kwargs):
        return await self.request("PUT", *urls, data=data, **kwargs)



    async def __aenter__(self):
        return self
    async def __aexit__(self, et, ev, t):
        await self.session.close()

