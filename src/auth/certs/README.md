### Warning
These keys are created only for development and testing purposes, they will not be included in the build,
please do not use them in a production environment.

You can use the following commands to generate keys using OpenSSL: 
```shell
openssl genpkey -algorithm RSA -out jwt-private.pem
openssl rsa -in jwt-private.pem -pubout -out jwt-public.pem
```
Make sure you save them to the `/certs` folder.