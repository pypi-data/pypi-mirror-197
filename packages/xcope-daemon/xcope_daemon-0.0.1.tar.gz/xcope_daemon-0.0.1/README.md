# PyXcope.Daemon

## How to compile protobuf
The *diagnose_daemon.proto* is a grpc protobuf file. It should keep consistent with the server endpoint.
Whenever it changes, we must regenerate with commands on linux(dont' use on windows):

``` bash
cd xcope_daemon
python3 -m grpc_tools.protoc -I=. --python_out=. --pyi_out=. --grpc_python_out=. ./diagnose_daemon.proto
```

