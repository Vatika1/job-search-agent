EXCLUDE_TITLE = [
    "intern", "stagiaire", "junior", "co-op", "étudiant", "student",
    "manager", "directeur", "director", "vp", "head of",
    "android", "ios", "mobile", "frontend", "front-end", "ui developer",
    "qa", "test automation", "sdet", "testeur",
    "data engineer", "data scientist", "ml engineer", "machine learning",
    "devops", "sre", "infrastructure", "cloud engineer",
    ".net", "c#", "node", "php", "ruby", "golang", "c++", "embedded",
    "salesforce", "sap", "servicenow", "mulesoft", "workday",
]

INCLUDE_TITLE = [
    "java", "backend", "back-end", "software developer", "software engineer",
    "développeur", "ingénieur logiciel", "full stack", "fullstack",
    "spring", "microservices", "api developer", "platform engineer",
    "application developer", "python",
]

JAVA_KEYWORDS = [
    # core
    "java", "spring boot", "spring", "spring security", "jpa", "hibernate",
    "scala", "kotlin", "python",
    # architecture
    "microservice", "rest", "openapi", "swagger", "event-driven", "distributed",
    "kafka", "streaming", "design pattern", "oop",
    # data
    "postgresql", "postgres", "sql", "oracle", "db2", "mongodb", "elasticsearch",
    "hive", "impala", "spark",
    # cloud / devops
    "aws", "eks", "ecs", "s3", "rds", "msk", "docker", "kubernetes", "terraform",
    "github actions", "jenkins", "ci/cd", "maven", "gradle", "sonarqube",
    "opentelemetry", "cloudwatch", "observability",
    # testing / practice
    "junit", "mockito", "testcontainers", "bdd", "agile", "scrum",
    "on-call", "incident", "l3", "production support",
    # ai
    "llm", "claude", "copilot", "mcp", "prompt",
]

LOCATION_OK = ["montreal", "montréal", "quebec", "québec", "canada", "remote"]

MIN_JAVA_HITS = 5


def location_ok(location: str) -> bool:
    loc = location.lower()
    return any(word in loc for word in LOCATION_OK)

def title_ok(title: str) -> bool:
    t = title.lower()
    if any(word in t for word in EXCLUDE_TITLE):
        return False
    return any(word in t for word in INCLUDE_TITLE)


def java_hits(description: str) -> int:
    d = description.lower()
    return sum(1 for kw in JAVA_KEYWORDS if kw in d)