

module "api" {
  source       = "../../modules/api"
  environment  = var.environment
  product_name = var.product_name
  vpc_id       = var.vpc_id
  alb_subnets  = var.alb_subnets
}


module "ci-cd" {
  source       = "../../modules/ci-cd"
  environment  = var.environment
  product_name = var.product_name
}
