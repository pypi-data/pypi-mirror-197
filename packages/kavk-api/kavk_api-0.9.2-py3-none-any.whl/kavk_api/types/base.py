from pydantic import BaseModel as BM

class BaseMethod:
    def __init__(self, vk):
        self.vk = vk

    async def method(self, method:str, **params):
        try:
            params.pop('self')
        except: pass
        return await self.vk.call_method(method, **params)


class BaseList(BM):
    __root__:list

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
