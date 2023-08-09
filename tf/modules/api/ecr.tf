resource "aws_ecr_repository" "ecr_repository" {
  name                 = "${var.product_name}-${var.environment}"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "KMS"
  }

  image_scanning_configuration {
    scan_on_push = true
  }
}
