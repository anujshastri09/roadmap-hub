MERN_STACK = {
    "id": "mern-stack",
    "name": "MERN Stack Developer",
    "tagline": "MongoDB, Express, React and Node.js end to end",
    "icon": "⚛️",
    "color": "#00D9C0",
    "stages": [
        {
            "id": "mern-js-foundations",
            "title": "JavaScript Foundations",
            "subtitle": "Modern JS before frameworks",
            "order": 1,
            "topics": [
                {
                    "id": "mern-js-core",
                    "title": "Modern JavaScript (ES6+)",
                    "description": "Arrow functions, destructuring, modules, promises, async/await.",
                    "level": "beginner",
                    "estimated_hours": 18,
                    "resources": [
                        {"title": "MDN JavaScript Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "type": "docs"},
                        {"title": "JavaScript.info", "url": "https://javascript.info/", "type": "course"},
                    ],
                },
                {
                    "id": "mern-node-basics",
                    "title": "Node.js Fundamentals",
                    "description": "Event loop, modules, npm, file system, streams.",
                    "level": "beginner",
                    "estimated_hours": 14,
                    "resources": [
                        {"title": "Node.js Official Docs", "url": "https://nodejs.org/en/docs", "type": "docs"},
                        {"title": "Node.js Event Loop Guide", "url": "https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick", "type": "article"},
                    ],
                },
            ],
        },
        {
            "id": "mern-backend",
            "title": "Backend with Express & MongoDB",
            "subtitle": "Build REST APIs and data models",
            "order": 2,
            "topics": [
                {
                    "id": "mern-express",
                    "title": "Express.js REST APIs",
                    "description": "Routing, middleware, error handling, request validation.",
                    "level": "intermediate",
                    "estimated_hours": 16,
                    "resources": [
                        {"title": "Express.js Official Guide", "url": "https://expressjs.com/en/guide/routing.html", "type": "docs"},
                    ],
                },
                {
                    "id": "mern-mongodb",
                    "title": "MongoDB & Mongoose",
                    "description": "Schema design, aggregation pipeline, indexing, Mongoose ODM.",
                    "level": "intermediate",
                    "estimated_hours": 16,
                    "resources": [
                        {"title": "MongoDB Manual", "url": "https://www.mongodb.com/docs/manual/", "type": "docs"},
                        {"title": "Mongoose Documentation", "url": "https://mongoosejs.com/docs/guide.html", "type": "docs"},
                    ],
                },
                {
                    "id": "mern-auth",
                    "title": "Auth with JWT",
                    "description": "JWT-based auth, refresh tokens, password hashing with bcrypt.",
                    "level": "intermediate",
                    "estimated_hours": 10,
                    "resources": [
                        {"title": "JWT.io Introduction", "url": "https://jwt.io/introduction", "type": "article"},
                    ],
                },
            ],
        },
        {
            "id": "mern-frontend",
            "title": "Frontend with React",
            "subtitle": "Build interactive, modern UIs",
            "order": 3,
            "topics": [
                {
                    "id": "mern-react-core",
                    "title": "React Fundamentals",
                    "description": "Components, props, state, hooks, conditional rendering.",
                    "level": "intermediate",
                    "estimated_hours": 20,
                    "resources": [
                        {"title": "React Official Docs", "url": "https://react.dev/learn", "type": "docs"},
                    ],
                },
                {
                    "id": "mern-react-state",
                    "title": "State Management & Routing",
                    "description": "Context API, Redux Toolkit, React Router.",
                    "level": "intermediate",
                    "estimated_hours": 14,
                    "resources": [
                        {"title": "Redux Toolkit Docs", "url": "https://redux-toolkit.js.org/", "type": "docs"},
                        {"title": "React Router Docs", "url": "https://reactrouter.com/en/main", "type": "docs"},
                    ],
                },
            ],
        },
        {
            "id": "mern-deploy",
            "title": "Deployment & Scaling",
            "subtitle": "Ship the full stack",
            "order": 4,
            "topics": [
                {
                    "id": "mern-deploy-topic",
                    "title": "Deploying MERN Apps",
                    "description": "Docker, environment configs, hosting on Render/Vercel/EC2.",
                    "level": "advanced",
                    "estimated_hours": 10,
                    "resources": [
                        {"title": "MDN - Express Deployment", "url": "https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/Express_Nodejs/deployment", "type": "docs"},
                    ],
                },
            ],
        },
    ],
}
