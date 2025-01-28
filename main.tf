terraform {
    # backend "s3" {
    #     bucket         = "ai-crm-tf-state"
    #     key            = "terraform.tfstate" # Where within the bucket it will store that state
    #     region         = "us-east-1"
    #     dynamodb_table = "terraform-state-locking"
    #     encrypt        = true
    # }
    required_providers {
      aws = {
        source = "hashicorp/aws"
        version = "~> 3.0"
      }
    }
    
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "custom_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
}

data "aws_vpc" "custom_vpc" {
  id = aws_vpc.custom_vpc.id
}

resource "aws_subnet" "subnet_1" {
  vpc_id                  = aws_vpc.custom_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "subnet_2" {
  vpc_id                  = aws_vpc.custom_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true
}

# Criando o Internet Gateway (IGW)
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.custom_vpc.id
}

# Criando a tabela de rotas
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.custom_vpc.id
}

# Adicionando uma rota para o IGW
resource "aws_route" "route_to_internet" {
  route_table_id         = aws_route_table.public_route_table.id
  destination_cidr_block = "0.0.0.0/0"  # Toda a internet
  gateway_id             = aws_internet_gateway.igw.id
}

# Associando a tabela de rotas à subnet pública
resource "aws_route_table_association" "subnet_1_association" {
  subnet_id      = aws_subnet.subnet_1.id
  route_table_id = aws_route_table.public_route_table.id
}

# resource "aws_secretsmanager_secret_version" "app_secrets_version" {
#   secret_id     = aws_secretsmanager_secret.app_secrets.id
#   secret_string = jsonencode({
#     POSTGRES_USER           = var.POSTGRES_USER
#     POSTGRES_PASSWORD       = var.POSTGRES_PASSWORD
#     POSTGRES_DB             = var.POSTGRES_DB
#     PGADMIN_DEFAULT_EMAIL   = var.PGADMIN_DEFAULT_EMAIL
#     PGADMIN_DEFAULT_PASSWORD = var.PGADMIN_DEFAULT_PASSWORD
#     DB_URL                  = var.DB_URL
#     PROJECT_PATH            = var.PROJECT_PATH
#     DB_LOCAL_URL            = var.DB_LOCAL_URL
#     OPENAI_API_KEY          = var.OPENAI_API_KEY
#   })
# }

data "aws_secretsmanager_secret" "app_secrets" {
  name = "app-secrets"
}

data "aws_secretsmanager_secret_version" "app_secrets_version" {
  secret_id = data.aws_secretsmanager_secret.app_secrets.id
}

locals {
  secrets = jsondecode(data.aws_secretsmanager_secret_version.app_secrets_version.secret_string)
}

output "secrets" {
  value     = local.secrets
  sensitive = true
}

resource "aws_security_group" "instances" {
  name = "instance-security-group"
  description = "Security group for EC2 instances"
  vpc_id      = aws_vpc.custom_vpc.id

  # Permite tráfego HTTP e SSH
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app_server" {
  ami           = "ami-011899242bb902164"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.instances.id]
  subnet_id = aws_subnet.subnet_1.id
  associate_public_ip_address = true

  user_data = <<-EOF
    Content-Type: multipart/mixed; boundary="//"
    MIME-Version: 1.0
    --//
    Content-Type: text/cloud-config; charset="us-ascii"
    MIME-Version: 1.0
    Content-Transfer-Encoding: 7bit
    Content-Disposition: attachment; filename="cloud-config.txt"
    #cloud-config
    cloud_final_modules:
    - [scripts-user, always]
    --//
    Content-Type: text/x-shellscript; charset="us-ascii"
    MIME-Version: 1.0
    Content-Transfer-Encoding: 7bit
    Content-Disposition: attachment; filename="userdata.txt"
    #!/bin/bash
    sudo ufw disable
    sudo iptables -L
    sudo iptables -F
    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install ca-certificates curl -y
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update -y
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
    sudo systemctl start docker
    sudo systemctl enable docker

    git clone https://github.com/DiogoSoares3/CRM-AI-Analysis.git /home/ubuntu/app
    cd /home/ubuntu/app

    cat <<EOT >> /home/ubuntu/app/.env
    POSTGRES_USER=${local.secrets["POSTGRES_USER"]}
    POSTGRES_PASSWORD=${local.secrets["POSTGRES_PASSWORD"]}
    POSTGRES_DB=${local.secrets["POSTGRES_DB"]}
    PGADMIN_DEFAULT_EMAIL=${local.secrets["PGADMIN_DEFAULT_EMAIL"]}
    PGADMIN_DEFAULT_PASSWORD=${local.secrets["PGADMIN_DEFAULT_PASSWORD"]}
    DB_URL=${local.secrets["DB_URL"]}
    PROJECT_PATH=${local.secrets["PROJECT_PATH"]}
    DB_LOCAL_URL=${local.secrets["DB_LOCAL_URL"]}
    OPENAI_API_KEY=${local.secrets["OPENAI_API_KEY"]}
    EOT

    cat <<EOT >> /home/ubuntu/app/datawarehouse/.env
    POSTGRES_USER=${local.secrets["POSTGRES_USER"]}
    POSTGRES_PASSWORD=${local.secrets["POSTGRES_PASSWORD"]}
    POSTGRES_DB=${local.secrets["POSTGRES_DB"]}
    POSTGRES_PORT="5432"
    DB_TYPE="postgres"
    DB_SCHEMA_DEV="dev"
    DB_SCHEMA_PROD="prod"
    DB_THREADS=16
    EOT

    sudo docker compose -f docker-compose.prod.yaml -d
  EOF

  tags = {
    Name = "AppServer"
  }
}

resource "aws_security_group_rule" "allow_http_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.instances.id

  from_port   = 8080
  to_port     = 8080
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}