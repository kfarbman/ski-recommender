resource "aws_ecs_cluster" "recsys_cluster" {
  name = "${var.product_name}-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "recsys_task_definition" {
  family = "${var.product_name}-${var.environment}-task-definition"

  container_definitions = jsonencode([
    {
      "name" : "${var.product_name}-${var.environment}-container",
      "image" : "${data.aws_caller_identity.current.id}.dkr.ecr.us-east-1.amazonaws.com/${var.product_name}-${var.environment}:latest",
      "portMappings" : [
        {
          "containerPort" : 8080,
          "hostPort" : 8080,
          "protocol" : "tcp"
        }
      ],
      "essential" : true,
      "entryPoint" : [],
      "command" : [
        "python",
        "web_app/app.py"
      ],
      "logConfiguration" : {
        "logDriver" : "awslogs",
        "options" : {
          "awslogs-group" : "/ecs/${var.product_name}-${var.environment}",
          "awslogs-region" : data.aws_region.region.name,
          "awslogs-stream-prefix" : "ecs"
        },
        "secretOptions" : []
      },
      "systemControls" : []
    }
  ])

  cpu          = 512
  memory       = 1024
  network_mode = "awsvpc"

  requires_compatibilities = ["FARGATE"]

  # TODO: Create task and execution roles
  # task_role_arn = "XXXX_TASK_ROLE_ARN_XXXX"
  # execution_role_arn = "XXXX_EXECUTION_ROLE_ARN_XXXX"

}
