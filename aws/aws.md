# AWS

Walkthrough for setting up ski recommender infrastructure on AWS

## Architecture Diagram

## Tutorial

1. Create Cluster and Network

`1_create_cluster.yaml` creates the following services:

    * Security Groups
    * ECS cluster
    * ECR repository
    * IAM roles

Within CloudFormation, upload `1_create_cluster.yaml`, and follow the prompts.

TODO
2. Create CodeBuild project
- CloudWatch Logs

3. Create ECS Task Definition & Service

4. Create CodeDeploy pipeline


1. Load Balancer
    * Specify ports
        - 8080 (prod)
        - 9000 (test / BG deployment)
2. ECR Repo
3. ECS cluster
    - Empty cluster
4. ECS Task definition
    - FARGATE
5. CodePipeline
    * CodeBuild
    * CodeDeploy
6. ECS - Service
7. CloudWatch
    - Configure within other CF templates?
8. IAM Policies
