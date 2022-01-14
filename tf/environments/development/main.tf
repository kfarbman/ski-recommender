

module "api" {
  source       = "../../modules/api"
  environment  = var.environment
  product_name = var.product_name
}
