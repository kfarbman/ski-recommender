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
            "Service" : ["ecs.amazonaws.com", "ecs-tasks.amazonaws.com"]
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
            "Service" : ["ecs.amazonaws.com", "ecs-tasks.amazonaws.com"]
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

  # task_role_arn      = aws_iam_role.ecs_task_role.arn
  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn

}

resource "aws_ecs_service" "reccys_ecs_service" {
  name    = "${var.product_name}-${var.environment}-ecs-service"
  cluster = aws_ecs_cluster.recsys_cluster.arn
  load_balancer {
    target_group_arn = aws_lb_target_group.recsys_alb_target_group.arn
    container_name   = "${var.product_name}-${var.environment}-container"
    container_port   = 8080
  }
  desired_count                      = 1
  launch_type                        = "FARGATE"
  platform_version                   = "LATEST"
  task_definition                    = aws_ecs_task_definition.recsys_task_definition.arn
  deployment_maximum_percent         = 200
  deployment_minimum_healthy_percent = 100

  network_configuration {
    assign_public_ip = true
    security_groups = [
      "sg-017bf7dd6620262bf"
    ]
    subnets = [
      "subnet-00b3c45a",
      "subnet-978fbedf"
    ]
  }
  health_check_grace_period_seconds = 0
  scheduling_strategy               = "REPLICA"

  deployment_controller {
    type = "ECS"
  }
}


resource "aws_cloudwatch_log_group" "recsys_log_group" {
  name              = "/ecs/${var.product_name}-${var.environment}"
  retention_in_days = 365
}

resource "aws_cloudwatch_log_stream" "recsys_log_stream" {
  name           = "/ecs/${var.product_name}-${var.environment}-log-stream"
  log_group_name = aws_cloudwatch_log_group.recsys_log_group.name
}
