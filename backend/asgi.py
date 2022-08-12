import uvicorn

from rest.settings import settings

def start_rest():
    uvicorn.run(
        'rest.main:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
        #workers=4
    )

if __name__ == '__main__':
    pass
    #start_rest()