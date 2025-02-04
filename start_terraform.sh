#!/bin/bash

# Inicializa o Terraform
terraform init

# Cria o plano e o salva em um arquivo
terraform plan -out=tfplan

# Aplica o plano sem pedir confirmação
terraform apply -auto-approve tfplan

# Para destruir, se necessário:
terraform destroy -auto-approve