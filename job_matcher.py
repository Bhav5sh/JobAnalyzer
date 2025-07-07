# import json
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # Load job roles
# def load_job_roles(path="data/job_roles.json"):
#     with open(path, "r") as f:
#         return json.load(f)

# # Match resume text to job roles
# def predict_job_roles(resume_text, top_n=3, threshold=0.4):
#     job_roles = load_job_roles()
#     roles = list(job_roles.keys())
#     descriptions = list(job_roles.values())

#     # Combine with resume
#     all_texts = descriptions + [resume_text]

#     # TF-IDF
#     vectorizer = TfidfVectorizer()
#     vectors = vectorizer.fit_transform(all_texts)

#     resume_vector = vectors[-1]
#     role_vectors = vectors[:-1]

#     # Cosine similarity
#     similarities = cosine_similarity(resume_vector, role_vectors).flatten()

#     # Top N matches
#     top_indices = similarities.argsort()[::-1][:top_n]
#     matched_roles = []

#     for i in top_indices:
#         score = similarities[i]
#         if score >= threshold:
#             matched_roles.append((roles[i], round(score * 100, 2)))

#     return matched_roles
