import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Skill database
SKILLS_DB = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "data analysis",
    "data science",
    "power bi",
    "tableau",
    "excel",
    "aws",
    "azure",
    "gcp",
    "tensorflow",
    "pytorch",
    "nlp",
    "computer vision",
    "statistics",
    "spark",
    "hadoop",
    "flask",
    "streamlit",
    "scikit-learn",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "git",
    "docker",
    "kubernetes",
    "mongodb",
    "postgresql",
    "mysql"
]


def preprocess_text(text):
    """
    Clean and normalize text
    """
    doc = nlp(text.lower())

    tokens = []

    for token in doc:
        if not token.is_stop and not token.is_punct:
            tokens.append(token.text)

    return " ".join(tokens)


def extract_skills(text):
    """
    Extract skills from resume text
    """

    processed_text = preprocess_text(text)

    found_skills = []

    for skill in SKILLS_DB:
        if skill.lower() in processed_text:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))
