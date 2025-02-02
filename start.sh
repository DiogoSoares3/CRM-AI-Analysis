#!/bin/sh

# Cria diretórios dos serviços
mkdir -p /home/ubuntu/service1 /home/ubuntu/service2

# Cria arquivos HTML para resposta
echo "Hello from Service 1" > /home/ubuntu/service1/index.html
echo "Hello from Service 2" > /home/ubuntu/service2/index.html

# Inicia os servidores Python
python3 -m http.server 8000 --directory /home/ubuntu/service1 &
python3 -m http.server 8210 --directory /home/ubuntu/service2 &

# Mantém o container rodando
tail -f /dev/null