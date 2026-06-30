SYSTEM_DESIGN = {
    "id": "system-design",
    "name": "System Design",
    "tagline": "From fundamentals to designing large-scale distributed systems",
    "icon": "🏛️",
    "color": "#9B8CFF",
    "stages": [
        {
            "id": "sd-fundamentals",
            "title": "Fundamentals",
            "subtitle": "Building blocks of distributed systems",
            "order": 1,
            "topics": [
                {
                    "id": "sd-scaling-basics",
                    "title": "Scalability & Load Balancing",
                    "description": "Vertical vs horizontal scaling, load balancers, reverse proxies.",
                    "level": "beginner",
                    "estimated_hours": 10,
                    "resources": [
                        {"title": "System Design Primer (GitHub)", "url": "https://github.com/donnemartin/system-design-primer", "type": "article"},
                    ],
                },
                {
                    "id": "sd-caching",
                    "title": "Caching Strategies",
                    "description": "Cache-aside, write-through, CDN caching, cache invalidation.",
                    "level": "beginner",
                    "estimated_hours": 8,
                    "resources": [
                        {"title": "AWS - Caching Overview", "url": "https://aws.amazon.com/caching/", "type": "article"},
                    ],
                },
            ],
        },
        {
            "id": "sd-data",
            "title": "Data & Storage",
            "subtitle": "Database design at scale",
            "order": 2,
            "topics": [
                {
                    "id": "sd-sql-nosql",
                    "title": "SQL vs NoSQL & Sharding",
                    "description": "When to use relational vs document/key-value stores, partitioning strategies.",
                    "level": "intermediate",
                    "estimated_hours": 12,
                    "resources": [
                        {"title": "MongoDB - Sharding Docs", "url": "https://www.mongodb.com/docs/manual/sharding/", "type": "docs"},
                    ],
                },
                {
                    "id": "sd-replication",
                    "title": "Replication & Consistency Models",
                    "description": "Leader-follower replication, CAP theorem, eventual vs strong consistency.",
                    "level": "intermediate",
                    "estimated_hours": 12,
                    "resources": [
                        {"title": "AWS - CAP Theorem Overview", "url": "https://aws.amazon.com/builders-library/", "type": "article"},
                    ],
                },
            ],
        },
        {
            "id": "sd-messaging",
            "title": "Messaging & Microservices",
            "subtitle": "Decoupled, event-driven architecture",
            "order": 3,
            "topics": [
                {
                    "id": "sd-queues",
                    "title": "Message Queues & Pub/Sub",
                    "description": "Kafka, RabbitMQ, async processing, event-driven design.",
                    "level": "advanced",
                    "estimated_hours": 14,
                    "resources": [
                        {"title": "Apache Kafka Documentation", "url": "https://kafka.apache.org/documentation/", "type": "docs"},
                        {"title": "RabbitMQ Tutorials", "url": "https://www.rabbitmq.com/tutorials", "type": "docs"},
                    ],
                },
                {
                    "id": "sd-microservices",
                    "title": "Microservices Architecture",
                    "description": "Service boundaries, API gateways, service discovery, resilience patterns.",
                    "level": "advanced",
                    "estimated_hours": 16,
                    "resources": [
                        {"title": "Martin Fowler - Microservices", "url": "https://martinfowler.com/articles/microservices.html", "type": "article"},
                    ],
                },
            ],
        },
        {
            "id": "sd-case-studies",
            "title": "Case Studies & Interview Prep",
            "subtitle": "Apply concepts to real designs",
            "order": 4,
            "topics": [
                {
                    "id": "sd-interview",
                    "title": "Designing Real Systems",
                    "description": "URL shortener, chat app, news feed, rate limiter - practice designs.",
                    "level": "advanced",
                    "estimated_hours": 20,
                    "resources": [
                        {"title": "System Design Primer - Case Studies", "url": "https://github.com/donnemartin/system-design-primer#system-design-interview-questions-with-solutions", "type": "article"},
                    ],
                },
            ],
        },
    ],
}
