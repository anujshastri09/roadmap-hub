JAVA_DEVELOPER = {
    "id": "java-developer",
    "name": "Java Developer",
    "tagline": "Core Java to enterprise Spring Boot systems",
    "icon": "☕",
    "color": "#FF8A3D",
    "stages": [
        {
            "id": "java-core",
            "title": "Core Java",
            "subtitle": "Language fundamentals and OOP",
            "order": 1,
            "topics": [
                {
                    "id": "java-syntax",
                    "title": "Java Syntax & OOP",
                    "description": "Classes, interfaces, inheritance, polymorphism, collections.",
                    "level": "beginner",
                    "estimated_hours": 22,
                    "resources": [
                        {"title": "Oracle Java Tutorials", "url": "https://docs.oracle.com/javase/tutorial/", "type": "docs"},
                        {"title": "Java Collections Framework Guide", "url": "https://docs.oracle.com/javase/tutorial/collections/index.html", "type": "docs"},
                    ],
                },
                {
                    "id": "java-streams",
                    "title": "Streams & Functional Features",
                    "description": "Lambdas, Stream API, Optional, method references.",
                    "level": "intermediate",
                    "estimated_hours": 12,
                    "resources": [
                        {"title": "Oracle - Lambda Expressions", "url": "https://docs.oracle.com/javase/tutorial/java/javaOO/lambdaexpressions.html", "type": "docs"},
                    ],
                },
            ],
        },
        {
            "id": "java-spring",
            "title": "Spring Ecosystem",
            "subtitle": "Build enterprise-grade backends",
            "order": 2,
            "topics": [
                {
                    "id": "java-spring-boot",
                    "title": "Spring Boot Fundamentals",
                    "description": "Auto-configuration, REST controllers, dependency injection.",
                    "level": "intermediate",
                    "estimated_hours": 22,
                    "resources": [
                        {"title": "Spring Boot Reference Docs", "url": "https://docs.spring.io/spring-boot/index.html", "type": "docs"},
                    ],
                },
                {
                    "id": "java-spring-data",
                    "title": "Spring Data JPA",
                    "description": "Entity mapping, repositories, transactions, query methods.",
                    "level": "intermediate",
                    "estimated_hours": 16,
                    "resources": [
                        {"title": "Spring Data JPA Docs", "url": "https://docs.spring.io/spring-data/jpa/reference/", "type": "docs"},
                    ],
                },
                {
                    "id": "java-spring-security",
                    "title": "Spring Security",
                    "description": "Authentication, authorization, JWT integration.",
                    "level": "advanced",
                    "estimated_hours": 14,
                    "resources": [
                        {"title": "Spring Security Reference", "url": "https://docs.spring.io/spring-security/reference/index.html", "type": "docs"},
                    ],
                },
            ],
        },
        {
            "id": "java-production",
            "title": "Testing & Production",
            "subtitle": "Quality and deployment",
            "order": 3,
            "topics": [
                {
                    "id": "java-testing",
                    "title": "Testing with JUnit & Mockito",
                    "description": "Unit and integration testing for Spring applications.",
                    "level": "intermediate",
                    "estimated_hours": 10,
                    "resources": [
                        {"title": "JUnit 5 User Guide", "url": "https://junit.org/junit5/docs/current/user-guide/", "type": "docs"},
                        {"title": "Mockito Documentation", "url": "https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html", "type": "docs"},
                    ],
                },
                {
                    "id": "java-docker-deploy",
                    "title": "Containerizing Spring Boot",
                    "description": "Dockerizing Java apps, building production jars.",
                    "level": "advanced",
                    "estimated_hours": 8,
                    "resources": [
                        {"title": "Spring Boot - Docker Guide", "url": "https://docs.spring.io/spring-boot/reference/packaging/container-images/dockerfiles.html", "type": "docs"},
                    ],
                },
            ],
        },
    ],
}
