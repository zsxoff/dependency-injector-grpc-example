all: clean gen

clean:
	rm -rf organizer/note/v1/*_{grpc.py,pb2.py,pb2.pyi}

gen:
	python -m grpc_tools.protoc -I=. --python_out=. --pyi_out=. --grpc_python_out=. ./organizer/note/v1/*.proto

.PHONY: all clean gen
