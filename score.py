import re

# Core skills for Data Science roles
REQUIRED_SKILLS = [
    "python",
    "sql",
    "machine learning",
    "statistics",
    "pandas",
    "numpy",
    "data analysis"
]

PREFERRED_SKILLS = [
    "power bi",
    "tableau",
    "aws",
    "tensorflow",
    "pytorch",
    "nlp",
    "spark",
    "streamlit"
]


def detect_education(text):
    text = text.lower()

    education_keywords = [
        "b.tech",
        "b.e",
        "bachelor",
        "m.tech",
        "master",
        "b.sc",
        "m.sc",
        "phd"
    ]

    for keyword in education_keywords:
        if keyword in text:
            return True

    return False


def detect_projects(text):
    text = text.lower()

    keywords = [
        "project",
        "projects",
        "developed",
        "implemented",
        "built",
        "designed"
    ]

    return any(word in text for word in keywords)


def detect_certifications(text):
    text = text.lower()

    keywords = [
        "certificate",
        "certification",
        "coursera",
        "udemy",
        "google",
        "ibm",
        "aws certified",
        "microsoft"
    ]

    return any(word in text for word in keywords)


def detect_experience(text):
    """
    Detect years of experience.
    Example:
    2 years experience
    3+ years experience
    """

    text = text.lower()

    patterns = [
        r'(\d+)\+?\s*years',
        r'(\d+)\+?\s*year'
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return int(match.group(1))

    return 0


def calculate_ats_score(skills, resume_text=""):
    """
    Returns ATS score between 0 and 100
    """

    score = 0

    # Required skills = 50 marks
    skill_score = 0

    for skill in REQUIRED_SKILLS:
        if skill in skills:
            skill_score += 50 / len(REQUIRED_SKILLS)

    score += skill_score

    # Preferred skills = 20 marks
    preferred_score = 0

    for skill in PREFERRED_SKILLS:
        if skill in skills:
            preferred_score += 20 / len(PREFERRED_SKILLS)

    score += preferred_score

    # Education = 10 marks
    if detect_education(resume_text):
        score += 10

    # Projects = 10 marks
    if detect_projects(resume_text):
        score += 10

    # Certifications = 5 marks
    if detect_certifications(resume_text):
        score += 5

    # Experience = 5 marks
    experience = detect_experience(resume_text)

    if experience >= 2:
        score += 5
    elif experience == 1:
        score += 3

    return min(round(score), 100)
