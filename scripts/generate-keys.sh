#!/bin/bash
set -e

CERT_DIR="/auth/certs"

mkdir -p "$CERT_DIR"
echo "Generating new JWT keys..."
openssl genpkey -algorithm RSA -out "$CERT_DIR/jwt-private.pem"
openssl rsa -in "$CERT_DIR/jwt-private.pem" -pubout -out "$CERT_DIR/jwt-public.pem"
chmod 600 "$CERT_DIR"/*