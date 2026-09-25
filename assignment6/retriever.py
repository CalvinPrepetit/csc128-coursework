"""
CSC-128 Assignment 6 starter: retrieval
Calvin A. Prepetit
"""
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from knowledge import DOCUMENTS


# Common wording is removed so policy-specific words carry more weight.
# "not" and "no" stay because they can change the meaning of a question.
STOP_WORDS = {
    "i", "me", "my", "a", "an", "the", "is", "are", "am", "was", "were",
    "to", "for", "with", "of", "on", "in", "at", "from", "and", "or", "but",
    "can", "could", "would", "you", "please", "it", "this", "that",
    "just", "really", "very", "do", "does", "did", "have", "has", "had", "should", "will",
    "what", "when", "where", "how", "if", "before", "after", "about", "open",
    "car", "cars", "vehicle", "vehicles", "auto", "shop", "brake", "used",
}

# Set from the score evidence printed by test_retriever.py.
DEFAULT_THRESHOLD = 0.12
DEFAULT_TOP_K = 3


def stem(word):
    """Strip a few common suffixes so related forms share a token."""
    if word.endswith("ies") and len(word) > 5:
        return word[:-3] + "y"
    if word.endswith("ation") and len(word) > 7:
        return word[:-5]
    if word.endswith("ing") and len(word) > 5:
        word = word[:-3]
    elif word.endswith("ed") and len(word) > 4:
        word = word[:-2]
    elif word.endswith("es") and len(word) > 4:
        word = word[:-2]
    elif word.endswith("s") and len(word) > 3:
        word = word[:-1]

    if word.endswith("e") and len(word) > 5:
        word = word[:-1]
    return word


def analyze(text):
    """Normalize, tokenize, stem, and add bigrams."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = [stem(token) for token in text.split() if token not in STOP_WORDS]
    bigrams = [f"{tokens[index]}_{tokens[index + 1]}" for index in range(len(tokens) - 1)]
    return tokens + bigrams


class Retriever:
    def __init__(self, documents=None, threshold=DEFAULT_THRESHOLD):
        """Fit a TF-IDF vectorizer on the approved document chunks."""
        self.documents = DOCUMENTS if documents is None else documents
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer(analyzer=analyze, lowercase=False)
        texts = [document["text"] for document in self.documents]
        self.document_vectors = self.vectorizer.fit_transform(texts)

    def search(self, question, top_k=DEFAULT_TOP_K):
        """
        Return a list of (document, score), best first, dropping anything
        below the threshold.

        Returning an empty list is correct and important. It tells the bot
        to refuse instead of calling the model with nothing useful.
        """
        question_vector = self.vectorizer.transform([question])
        scores = cosine_similarity(question_vector, self.document_vectors)[0]
        ranked = sorted(enumerate(scores), key=lambda pair: pair[1], reverse=True)

        hits = []
        for index, score in ranked[:top_k]:
            score = float(score)
            if score >= self.threshold:
                hits.append((self.documents[index], score))
        return hits

    def build_context(self, hits):
        """Format retrieved chunks for the prompt, including their sources."""
        sections = []
        for number, (document, _score) in enumerate(hits, start=1):
            sections.append(
                f"[REFERENCE {number}]\n"
                f"ID: {document['id']}\n"
                f"Source: {document['source']}\n"
                f"Text: {document['text']}\n"
                f"[/REFERENCE {number}]"
            )
        return "\n\n".join(sections)
