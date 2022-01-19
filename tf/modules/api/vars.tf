variable "environment" {
  type        = string
  description = "Name of environment"
}

variable "product_name" {
  type        = string
  description = "Name of product"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID"
}

variable "alb_subnets" {
  type        = list(any)
  description = "ALB subnets"
}
