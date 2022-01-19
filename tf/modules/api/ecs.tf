resource "aws_ecs_cluster" "recsys_cluster" {
  name = "${var.product_name}-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.product_name}-${var.environment}-ecs-task-execution-role"

  assume_role_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Action" : "sts:AssumeRole",
          "Principal" : {
            "Service" : "ecs-tasks.amazonaws.com"
          },
          "Effect" : "Allow",
          "Sid" : ""
        }
      ]
    }
  )
}

resource "aws_iam_role" "ecs_task_role" {
  name = "${var.product_name}-${var.environment}-ecs-task-role"

  assume_role_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Action" : "sts:AssumeRole",
          "Principal" : {
            "Service" : "ecs-tasks.amazonaws.com"
          },
          "Effect" : "Allow",
          "Sid" : ""
        }
      ]
    }
  )
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "ecs_task_policy" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
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

  task_role_arn      = aws_iam_role.ecs_task_role.arn
  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn

}
