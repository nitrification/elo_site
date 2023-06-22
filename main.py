import sys
sys.path.insert(0, 'modules/')

from modules import server

if __name__ == "__main__":
    print("Starting server...")
    server.run()

