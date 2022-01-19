resource "aws_ssm_parameter" "ecr_image_tag" {
  name        = "/ski-recommender/${var.environment}/ecrRepoName"
  description = "ECR repository name"
  type        = "SecureString"
  value       = aws_ecr_repository.ecr_repository.name

  tags = {
    Environment = var.environment
  }
}
