# Auto Shop Service Bot

This project builds on the auto shop service bot idea I used in earlier assignments. Instead of matching exact keywords, this version uses TF-IDF and cosine similarity to classify the customer's intent.

The bot handles 5 service areas: electrical, drivability, interior, exterior, and maintenance.

## How to Run

```
streamlit run app.py
```

## How to Run Tests

```
python test_classifier.py
```

## Threshold Evidence

The lowest score for a message the bot should handle was `0.46`.

The highest score for a message the bot should reject was `0.38`.

I chose a threshold of `0.42` because it sits between those 2 scores. I split the lowest match score and highest reject score down the middle so the bot accepts auto shop messages but rejects unrelated messages.

## Normalization

The normalize function lowercases text, removes punctuation, drops stop words, and stems simple word endings. The stop word list does not remove `not` or `no` because those words can change the meaning of a message. For example, `my car is not starting` should not be treated the same as `my car is starting`. From a user service standpoint, this does not hinder operations and will in most cases align the user to the appropriate service area.

## Test Results

The test file checks 15 messages the bot should handle and 5 messages the bot should reject. All 20 tests passed.

## What I Would Improve With More Time

With more time, I would add a separate file with more training examples so the bot could classify more customer wording without cluttering the code. I would also improve the Streamlit interface if custom styling was allowed or expected.
