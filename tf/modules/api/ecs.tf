resource "aws_ecs_cluster" "recsys_cluster" {
  name = "${var.product_name}-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}
