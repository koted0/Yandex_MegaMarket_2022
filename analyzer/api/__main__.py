import uvicorn
import os

if __name__ == '__main__':
    port = int(os.environ['analyzer_port'])
    uvicorn.run('app:app', host='localhost', port=port, reload=True)
