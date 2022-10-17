# DO NOT RUN THIS SCRIPT
# This supposed to be used for development


import os
import tempfile
import requests
import sys
import io
import tarfile

# Compile proto files from github repository


def compile_proto_from_source(dist):
    tmp = tempfile.TemporaryDirectory()
    tmp_dir = tmp.name

    # download and extract source
    latest = requests.get('https://api.github.com/repos/v2fly/v2ray-core/releases/latest') \
        .json() \
        .get('tag_name')

    version = latest

    download_url = f'https://github.com/v2fly/v2ray-core/archive/refs/tags/{version}.tar.gz'
    r = requests.get(download_url, stream=True)
    io_bytes = io.BytesIO(r.content)
    tar = tarfile.open(fileobj=io_bytes, mode='r')
    tar.extractall(tmp_dir)
    v2ray_dir = os.path.join(tmp_dir, tar.getnames()[0])
    tar.close()
    io_bytes.close()

    # find proto files
    proto_files = ''
    for root, dirs, files in os.walk(tmp_dir):
        for file in files:
            if file.endswith(".proto"):
                proto_files += ' ' + os.path.join(root, file)

    if not proto_files:
        raise FileNotFoundError("there's no proto file.")

    command = f'{sys.executable} -m grpc.tools.protoc ' \
        f'-I={v2ray_dir} ' \
        f'--python_out={dist} ' \
        f'--grpc_python_out={dist} ' + proto_files
    os.system(command)

    tmp.cleanup()


if __name__ == "__main__":
    compile_proto_from_source('.')
