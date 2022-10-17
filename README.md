# V2ReST

ReST API Interface to run v2ray server and manage users

⚠️ **This project only supports VMess currently. note that it's not compatible with V2ray v5 and above. It is recommended to run with V2ray** [v4.45.2](https://github.com/v2fly/v2ray-core/releases/tag/v4.45.2)

## Features

- Plan based system, feature to set expiration date and limit user traffic
- Running V2ray server automatically and internally
- Managing users through grpc (without restarting server)


## How to run
First you need to install **redis**, then

Clone the repository:

    git clone https://github.com/amirho3inf/V2ReST

Change directory to V2ReST and install the required packages:

    pip install -r requirements.txt

Run the app using uvicorn:

    uvicorn main:app

## Configuration
You can find all config variables in `config.py` file, and they all can be defined either in environment or `.env` file
    

## API documentation
Documentation will be available on http://127.0.0.1:8000/docs (this is default, you may change it later)


## TODO
- [ ] Username validation
- [ ] Authentication
- [ ] Dockerize
- [X] Connect link and QR