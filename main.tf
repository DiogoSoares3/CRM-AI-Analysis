terraform {
    #############################################################
    ## AFTER RUNNING TERRAFORM APPLY (WITH LOCAL BACKEND)
    ## YOU WILL UNCOMMENT THIS CODE THEN RERUN TERRAFORM INIT
    ## TO SWITCH FROM LOCAL BACKEND TO REMOTE AWS BACKEND
    #############################################################
    # backend "s3" {
    #   bucket         = "crm-analysis-tf-state"
    #   key            = "terraform.tfstate"
    #   region         = "us-east-1"
    #   dynamodb_table = "terraform-state-locking"
    #   encrypt        = true
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

resource "aws_s3_bucket" "terraform_state" {
  bucket        = "crm-analysis-tf-state"
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "terraform_bucket_versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state_crypto_conf" {
  bucket        = aws_s3_bucket.terraform_state.bucket 
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-locking"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
}

resource "aws_secretsmanager_secret_version" "app_secrets_version" {
  secret_id     = data.aws_secretsmanager_secret.app_secrets.id
  secret_string = jsonencode({
    POSTGRES_USER            = var.POSTGRES_USER
    POSTGRES_PASSWORD        = var.POSTGRES_PASSWORD
    POSTGRES_DB              = var.POSTGRES_DB
    DB_URL_PROD              = var.DB_URL_PROD
    PROJECT_PATH             = var.PROJECT_PATH
    OPENAI_API_KEY           = var.OPENAI_API_KEY
    HOST_AWS                 = var.HOST_AWS
    force_update             = timestamp()
  })
}

data "aws_secretsmanager_secret" "app_secrets" {
  name = "app-secrets"
}

data "aws_secretsmanager_secret_version" "app_secrets_version" {
  secret_id = data.aws_secretsmanager_secret.app_secrets.id
}

locals {
  secrets = jsondecode(aws_secretsmanager_secret_version.app_secrets_version.secret_string)
}

output "secrets" {
  value     = local.secrets
  sensitive = true
}

data "aws_vpc" "default_vpc" {
  default = true
}

data "aws_subnet_ids" "default_subnet" {
  vpc_id = data.aws_vpc.default_vpc.id
}

resource "aws_security_group" "instances" {
  name = "instance-security-group"
  description = "Security group for EC2 instances"
  vpc_id      = data.aws_vpc.default_vpc.id

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
  vpc_security_group_ids = [aws_security_group.instances.name]
  associate_public_ip_address = true

  user_data = <<-EOF
    #!/bin/bash
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
    DB_URL_PROD=${local.secrets["DB_URL_PROD"]}
    DB_SCHEMA_PROD=${local.secrets["DB_URL_PROD"]}
    PROJECT_PATH=${local.secrets["PROJECT_PATH"]}
    OPENAI_API_KEY=${local.secrets["OPENAI_API_KEY"]}
    EOT

    cat <<EOT >> /home/ubuntu/app/datawarehouse/.env
    POSTGRES_USER=${local.secrets["POSTGRES_USER"]}
    POSTGRES_PASSWORD=${local.secrets["POSTGRES_PASSWORD"]}
    POSTGRES_DB=${local.secrets["POSTGRES_DB"]}
    POSTGRES_PORT=5432
    DB_TYPE="postgres"
    DB_SCHEMA_PROD=${local.secrets["DB_URL_PROD"]}
    DB_THREADS=16
    HOST_AWS=${local.secrets["HOST_AWS"]}
    EOT

    sudo apt-get install -y nginx python3

    sudo tee /etc/nginx/sites-available/default << 'NGINX_CONF'
    server {
        listen 80 default_server;
        listen [::]:80 default_server;
        server_name _;

        location /docs/ {
            proxy_pass http://127.0.0.1:8000/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        location /dbt_docs/ {
            proxy_pass http://127.0.0.1:8080/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        location /api_docs/ {
            proxy_pass http://127.0.0.1:8200/docs;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        location /app/ {
            proxy_pass http://127.0.0.1:8210/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        location / {
               # First attempt to serve request as file, then
               # as directory, then fall back to displaying a 40>
            try_files $uri $uri/ =404;
       }
    }
    NGINX_CONF

    sudo systemctl restart nginx

    sudo docker compose -f docker-compose.prod.yaml up -d
  EOF

  tags = {
    Name = "AppServer"
  }
}

### If all the ports are consecutive (for example, 8000-8210),
### we can release the range in one go:
resource "aws_security_group_rule" "allow_http_services" {
  type              = "ingress"
  security_group_id = aws_security_group.instances.id
  from_port         = 8000
  to_port           = 8210
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_lb_target_group" "web" {
  name     = "tg-web"
  port     = 80
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.default_vpc.id
}

resource "aws_lb_target_group_attachment" "instance_web" {
  target_group_arn = aws_lb_target_group.web.arn
  target_id        = aws_instance.app_server.id
  port             = 80
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.load_balancer.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web.arn
  }
}

resource "aws_security_group" "alb" {
  name = "alb-security-group"
}

resource "aws_security_group_rule" "allow_alb_http_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.alb.id

  from_port   = 80
  to_port     = 80
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]

}

resource "aws_security_group_rule" "allow_alb_all_outbound" {
  type              = "egress"
  security_group_id = aws_security_group.alb.id

  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]

}

resource "aws_lb" "load_balancer" {
  name               = "web-app-lb"
  load_balancer_type = "application"
  subnets            = data.aws_subnet_ids.default_subnet.ids
  security_groups    = [aws_security_group.alb.id]
}

resource "aws_db_instance" "postgres_db" {
  identifier             = "postgres-db"
  instance_class         = "db.t3.micro"
  engine                 = "postgres"
  engine_version         = "16"
  allocated_storage      = 20
  storage_type           = "gp2"
  name                   = local.secrets["POSTGRES_DB"]
  username               = local.secrets["POSTGRES_USER"]
  password               = local.secrets["POSTGRES_PASSWORD"]
  parameter_group_name   = aws_db_parameter_group.postgres_db.name
  skip_final_snapshot    = true
  publicly_accessible    = true
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.postgres_db.name
  deletion_protection    = false
  backup_retention_period = 0
}

resource "aws_db_parameter_group" "postgres_db" {
  name   = "postgres-db-params"
  family = "postgres16"

  parameter {
    name  = "timezone"
    value = "UTC"
  }

  parameter {
    name  = "log_statement"
    value = "none"
  }
}

# Security Group para o RDS
resource "aws_security_group" "rds_sg" {
  name        = "rds-security-group"
  description = "Permite trafego PostgreSQL"

  ingress {
    from_port   = 5432
    to_port     = 5432
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

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default_vpc.id]
  }
}

# Subnet Group
resource "aws_db_subnet_group" "postgres_db" {
  name       = "postgres-db-subnet-group"
  subnet_ids = data.aws_subnets.default.ids
}
