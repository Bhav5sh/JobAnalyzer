import pdfplumber
import docx
import spacy

nlp = spacy.load("en_core_web_sm")

# Extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Extract text from DOCX
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Extract named entities (skills, education, etc.)
def extract_entities(text):
    doc = nlp(text)
    skills = []
    education = []
    experience = []

    for ent in doc.ents:
        if ent.label_ in ["ORG", "SKILL", "PRODUCT"]:
            skills.append(ent.text)
        elif ent.label_ in ["EDUCATION", "DEGREE"]:
            education.append(ent.text)
        elif ent.label_ in ["DATE", "TIME", "QUANTITY"]:
            experience.append(ent.text)

    return {
        "skills": list(set(skills)),
        "education": list(set(education)),
        "experience": list(set(experience))
    }

# Main function
def parse_resume(file):
    if file.name.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        text = extract_text_from_docx(file)
    else:
        return None, "Unsupported file format"

    entities = extract_entities(text)
    return text, entities
