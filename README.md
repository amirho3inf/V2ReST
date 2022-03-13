# V2ReST
ReST API based application which runs v2ray server inside and enable you to manage users and limit their usage

## How to run
Clone the repository:
    
    git clone https://github.com/amirho3inf/V2ReST

Change directory to V2ReST and install the required packages:

    pip install -r requirements.txt
You also need to have installed **redis** on your system

Run the app using uvicorn:

    uvicorn main:app

## Configuration
You can find all config variables in `config.py` file, and they all can be defined either in environment or `.env` file
    

## API documentation
After running, you can see and try API methods at http://127.0.0.1:8000/doc (this is default, you may change it later)


## TODO
- [ ] Username validation
- [ ] Authentication
- [ ] Dockerize
- [ ] Logging
- [ ] Connect link and QR
- [ ] Add new network stream options other than TCP
