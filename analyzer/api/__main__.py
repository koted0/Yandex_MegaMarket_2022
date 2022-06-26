import uvicorn
import os

def main():
    port = int(os.environ['analyzer_port'])
    uvicorn.run('analyzer.api.app:app', host='localhost', port=port, reload=True)


if __name__ == '__main__':
    main()