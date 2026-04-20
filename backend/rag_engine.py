import numpy as np

# Simulated Policy Knowledge Base
KNOWLEDGE_BASE = [
    "Home Loan Interest Rate: 8-10%. Max Loan to Income Ratio: 7x. Required Documents: Aadhaar, PAN, Salary Slips or ITR, Bank Statement.",
    "Personal Loan Interest Rate: 11-18%. Max Loan to Income Ratio: 5x. Required Documents: Aadhaar, PAN, Salary Slips or ITR, Bank Statement.",
    "Business Loan Interest Rate: 12-16%. Max Loan to Income Ratio: 4x. Required Documents: Aadhaar, PAN, ITR, Bank Statement.",
    "Vehicle Loan Interest Rate: 9-12%. Max Loan to Income Ratio: 3x. Required Documents: Aadhaar, PAN, Bank Statement.",
    "Education Loan Interest Rate: 8-12%. Max Loan to Income Ratio: 5x. Required Documents: Aadhaar, PAN, Bank Statement.",
    "FOIR (Fixed Obligation to Income Ratio) must not exceed 55% of monthly income.",
    "CIBIL Score guidelines: Reject < 650. Conditional 650-699. Approve >= 700."
]

# Simulated embeddings using NumPy
embed_dim = 128
np.random.seed(42)

doc_embeddings = np.random.random((len(KNOWLEDGE_BASE), embed_dim)).astype('float32')


# 🔍 RAG-like search using cosine similarity
def search_policies(query: str, top_k: int = 3):
    # Simulate query embedding
    query_vector = np.random.random((1, embed_dim)).astype('float32')

    similarities = []

    for vec in doc_embeddings:
        sim = np.dot(query_vector[0], vec) / (
            np.linalg.norm(query_vector[0]) * np.linalg.norm(vec)
        )
        similarities.append(sim)

    # Get top-k similar indices
    indices = np.argsort(similarities)[-top_k:][::-1]

    results = []
    for idx in indices:
        if idx < len(KNOWLEDGE_BASE):
            results.append(KNOWLEDGE_BASE[idx])

    return results


# 💰 Interest Rate Logic
def get_interest_rate(loan_type: str) -> str:
    rates = {
        "home": "8-10%",
        "personal": "11-18%",
        "vehicle": "9-12%",
        "education": "8-12%",
        "business": "12-16%"
    }
    return rates.get(loan_type.lower(), "10-15%")


# 📊 Loan Multiplier Logic
def get_max_multiplier(loan_type: str) -> int:
    mults = {
        "home": 7,
        "personal": 5,
        "vehicle": 3,
        "education": 5,
        "business": 4
    }
    return mults.get(loan_type.lower(), 4)