all: clean gen

gen:
	# CA
	openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -nodes -out ca.crt -keyout ca.key -config ./cnf/ca.cnf

	# Server CSR and key
	openssl req -newkey rsa:4096 -nodes -out server.csr -keyout server.key -config ./cnf/server.cnf

	# Server CSR sign
	openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -sha256 -days 365 -out server.crt -extfile ./cnf/server.cnf -extensions v3_req

	# Server certificate chain
	cat server.crt ca.crt > server-chain.pem

	# Client CSR and key
	openssl req -newkey rsa:4096 -nodes -out client.csr -keyout client.key -config ./cnf/client.cnf

	# Client CSR sign
	openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -sha256 -days 365 -out client.crt -extfile ./cnf/client.cnf -extensions v3_req

	# Client certificate chain
	cat client.crt ca.crt > client-chain.pem

clean:
	rm -f ca.crt ca.key ca.srl client-chain.pem client.crt client.csr client.key server-chain.pem server.crt server.csr server.key

.PHONY: all clean gen
