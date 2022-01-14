resource "aws_ecr_repository" "ecr_repository" {
  name                 = "${var.product_name}-${var.environment}"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
