resource "aws_lb" "recsys_alb" {
  name               = "${var.product_name}-${var.environment}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.recsys_sg.id]
  subnets            = var.alb_subnets

  enable_deletion_protection = false

  tags = {
    Environment = var.environment
  }
}

resource "aws_lb_target_group" "recsys_alb_target_group" {
  health_check {
    interval            = 30
    path                = "/"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
    healthy_threshold   = 5
    matcher             = "200"
  }
  port        = 8080
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id
  name        = "${var.product_name}-${var.environment}-tg"
}

resource "aws_lb_listener" "https_listener" {
  load_balancer_arn = aws_lb.recsys_alb.arn
  port              = "8080"
  protocol          = "HTTP"
  # ssl_policy        = "ELBSecurityPolicy-2016-08"
  # certificate_arn   = "arn:aws:iam::187416307283:server-certificate/test_cert_rab3wuqwgja25ct3n4jdj2tzu4"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.recsys_alb_target_group.arn
  }
}
