# Auto Shop Service Bot

Calvin A. Prepetit - CSC-128 Assignment 6

This project continues my auto shop theme from the earlier assignments. This version uses retrieval to answer questions from a small approved policy guide instead of allowing the language model to answer from general knowledge.

The policies are examples I wrote for this assignment. They are not policies from a real business.

## How It Works

The bot works in this order:

1. The customer asks a question.
2. `retriever.py` compares the question with the chunks in `knowledge.py` using TF-IDF and cosine similarity.
3. Results below the similarity threshold are removed.
4. If no chunk remains, Python returns the refusal message directly and the model is never called.
5. If a chunk matches, the approved text is placed inside the grounding prompt.
6. The model answers using only that text.
7. The application displays the retrieved source labels under the answer.

## Project Files

- `knowledge.py` contains 12 self-contained policy chunks with an id and source label.
- `retriever.py` contains normalization, stemming, bigrams, TF-IDF retrieval, cosine similarity, and the threshold.
- `grounded_bot.py` contains the Streamlit interface, short circuit, grounding prompt, Groq call, and source display.
- `test_retriever.py` contains 13 questions that should retrieve and 6 that should be refused.
- `.gitignore` protects the real Streamlit secrets file.
- `secrets.toml.example` shows the required key format without containing a real key.

## How to Run

Activate the course virtual environment and install the requirements from the project folder:

```powershell
..\..\csc128\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the retrieval tests before starting the app:

```powershell
python test_retriever.py
```

Run the Streamlit bot:

```powershell
streamlit run grounded_bot.py
```

## API Key Setup

This assignment uses Groq. The real key belongs in:

```text
.streamlit/secrets.toml
```

The local secrets file should use this format:

```toml
GROQ_API_KEY = "paste_your_groq_key_here"
```

The real secrets file is listed in `.gitignore` and should never be committed. The project includes `secrets.toml.example` with a placeholder only.

After this project is copied into the official Git repository, confirm the real key is ignored before committing:

```powershell
git check-ignore -v assignment6/.streamlit/secrets.toml
```

## Knowledge Base

The knowledge base has 12 chunks covering:

- Shop hours.
- Appointment requests and walk-ins.
- Late arrivals.
- Information to bring at check-in.
- After-hours key drop instructions.
- Diagnostic authorization.
- Estimate changes and repair approval.
- Customer-supplied parts.
- Payment and vehicle pickup.
- Personal belongings.
- Unsafe vehicles and towing.
- Warranty review paperwork.

Each chunk covers 1 main idea and can answer a question without depending on the chunk next to it. The wording includes phrases a customer would actually use, such as "what should I bring," "leave my keys after the shop closes," and "my brakes barely work."

## Retriever and Threshold Evidence

The retriever uses the instructor's starter structure with a custom analyzer. The analyzer lowercases text, removes punctuation and common stop words, stems common suffixes, and adds bigrams. It keeps `not` and `no` because those words can change the meaning of a question.

I started with the starter threshold of `0.0`, which allowed every question through. The first evidence runs also showed 2 problems:

- Correct questions written in normal customer language were scoring too low.
- The phrase "open recall" could weakly match the shop-hours chunk because of the word "open."

I rewrote several chunks using customer vocabulary and adjusted the stop-word list so generic words did not control the result. I then selected a final threshold of `0.12` from the printed evidence.

Final evidence:

```text
Lowest match score: 0.178
Highest reject score: 0.000
19 out of 19 tests passed.
```

The lowest correct match remains above the threshold, while the near-miss questions remain below it.

## Short Circuit and Grounding Prompt

`answer_question()` runs retrieval before creating or calling the Groq client. If retrieval returns an empty list, the function immediately returns:

```text
I do not have that information in the auto shop policy guide. Please contact the shop directly.
```

The model is not called in that path.

When retrieval succeeds, the grounding prompt:

- Supplies the retrieved chunks between clear beginning and ending markers.
- Tells the model to use only the approved reference text.
- Forbids outside knowledge and added details.
- Forbids guessing prices, hours, dates, numbers, warranty decisions, repair results, or safety facts.
- Defines the exact refusal message.
- Tells the model not to create its own citations.

## Source Attribution

The application displays each retrieved source and chunk id under the answer. Attribution is added by Python from the retrieval result instead of asking the model to invent a citation.

The sources also help separate 2 different failures. If the wrong source appears, retrieval or chunk wording is the problem. If the correct source appears but the answer is wrong, the grounding prompt or model response is the problem.

## Hallucination Tests

These are 5 questions that are close to the auto shop topic but are not answered by the policy chunks. These are the actual responses returned by the finished program.

### 1. Insurance Claim

Question:

```text
Can you file an insurance claim for my accident?
```

Actual response:

```text
I do not have that information in the auto shop policy guide. Please contact the shop directly.
```

### 2. Manufacturer Recall

Question:

```text
Does my manufacturer have an open recall?
```

Actual response:

```text
I do not have that information in the auto shop policy guide. Please contact the shop directly.
```

### 3. Exact Transmission Price

Question:

```text
How much is a new transmission for my car?
```

Actual response:

```text
I do not have that information in the auto shop policy guide. Please contact the shop directly.
```

### 4. Vehicle-Specific Tire Pressure

Question:

```text
What tire pressure should I use for a 2022 sedan?
```

Actual response:

```text
I do not have that information in the auto shop policy guide. Please contact the shop directly.
```

### 5. At-Home Repair Instructions

Question:

```text
Can you tell me how to replace my brake pads at home?
```

Actual response:

```text
I do not have that information in the auto shop policy guide. Please contact the shop directly.
```

## Changes Made From Testing

The hallucination and retrieval tests caused me to change the threshold and chunk wording instead of trying to solve everything with the prompt.

- I changed the threshold from the starter value of `0.0` to `0.12` using the printed scores.
- I rewrote several chunks to include natural customer phrases that the first test run missed.
- I adjusted the analyzer so "open recall" did not retrieve shop hours and generic vehicle words did not create weak matches.
- I kept the strict grounding prompt as a second layer in case a relevant chunk does not fully answer the question.

The 5 final hallucination tests all stopped at the code-level short circuit, so no final prompt change was needed after the retrieval fixes.

## Live Grounded Test

I also ran 1 live Groq test with this question:

```text
What should I bring when I drop off my car?
```

The bot answered from the check-in policy and displayed these sources:

```text
Vehicle Check-In Guide (check_in)
Vehicle Drop-Off Guide - After-Hours Key Drop (after_hours)
```

This test checked the full path from retrieval through the displayed source.

## What I Would Improve With More Time

With more time, I would replace the example policies with documents approved by a real shop. I would also give staff a simple way to update the policies without editing Python files.
