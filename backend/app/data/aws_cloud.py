AWS_CLOUD = {
    "id": "aws-cloud",
    "name": "AWS Cloud Engineer",
    "tagline": "Core services to scalable cloud architecture",
    "icon": "☁️",
    "color": "#FFB300",
    "stages": [
        {
            "id": "aws-foundations",
            "title": "Cloud Foundations",
            "subtitle": "Core AWS building blocks",
            "order": 1,
            "topics": [
                {
                    "id": "aws-iam-ec2",
                    "title": "IAM, EC2 & VPC",
                    "description": "Identity & access management, virtual machines, networking basics.",
                    "level": "beginner",
                    "estimated_hours": 18,
                    "resources": [
                        {"title": "AWS IAM Documentation", "url": "https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html", "type": "docs"},
                        {"title": "AWS EC2 User Guide", "url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html", "type": "docs"},
                        {"title": "AWS VPC User Guide", "url": "https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html", "type": "docs"},
                    ],
                },
                {
                    "id": "aws-s3",
                    "title": "S3 & Storage Services",
                    "description": "Object storage, lifecycle policies, EBS vs EFS vs S3.",
                    "level": "beginner",
                    "estimated_hours": 10,
                    "resources": [
                        {"title": "Amazon S3 User Guide", "url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html", "type": "docs"},
                    ],
                },
            ],
        },
        {
            "id": "aws-compute-db",
            "title": "Compute & Databases",
            "subtitle": "Running and storing application data",
            "order": 2,
            "topics": [
                {
                    "id": "aws-lambda",
                    "title": "Serverless with Lambda & API Gateway",
                    "description": "Event-driven functions, REST APIs without servers.",
                    "level": "intermediate",
                    "estimated_hours": 14,
                    "resources": [
                        {"title": "AWS Lambda Developer Guide", "url": "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html", "type": "docs"},
                        {"title": "API Gateway Developer Guide", "url": "https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html", "type": "docs"},
                    ],
                },
                {
                    "id": "aws-rds",
                    "title": "RDS & DynamoDB",
                    "description": "Managed relational databases vs NoSQL DynamoDB design.",
                    "level": "intermediate",
                    "estimated_hours": 14,
                    "resources": [
                        {"title": "Amazon RDS User Guide", "url": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html", "type": "docs"},
                        {"title": "DynamoDB Developer Guide", "url": "https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html", "type": "docs"},
                    ],
                },
            ],
        },
        {
            "id": "aws-devops",
            "title": "DevOps & Infrastructure as Code",
            "subtitle": "Automating cloud infrastructure",
            "order": 3,
            "topics": [
                {
                    "id": "aws-cicd",
                    "title": "CI/CD on AWS",
                    "description": "CodePipeline, CodeBuild, deployment automation.",
                    "level": "advanced",
                    "estimated_hours": 12,
                    "resources": [
                        {"title": "AWS CodePipeline User Guide", "url": "https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html", "type": "docs"},
                    ],
                },
                {
                    "id": "aws-terraform",
                    "title": "Infrastructure as Code (Terraform/CloudFormation)",
                    "description": "Declarative infra provisioning and version-controlled environments.",
                    "level": "advanced",
                    "estimated_hours": 16,
                    "resources": [
                        {"title": "Terraform AWS Provider Docs", "url": "https://registry.terraform.io/providers/hashicorp/aws/latest/docs", "type": "docs"},
                        {"title": "AWS CloudFormation User Guide", "url": "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html", "type": "docs"},
                    ],
                },
            ],
        },
        {
            "id": "aws-architecture",
            "title": "Architecture & Certification",
            "subtitle": "Designing for scale and reliability",
            "order": 4,
            "topics": [
                {
                    "id": "aws-well-architected",
                    "title": "AWS Well-Architected Framework",
                    "description": "Reliability, security, cost optimization, performance pillars.",
                    "level": "advanced",
                    "estimated_hours": 10,
                    "resources": [
                        {"title": "AWS Well-Architected Framework", "url": "https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html", "type": "docs"},
                    ],
                },
                {
                    "id": "aws-cert",
                    "title": "Solutions Architect Associate Prep",
                    "description": "Certification exam guide and practice resources.",
                    "level": "advanced",
                    "estimated_hours": 20,
                    "resources": [
                        {"title": "AWS Certified Solutions Architect - Associate", "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/", "type": "course"},
                    ],
                },
            ],
        },
    ],
}
