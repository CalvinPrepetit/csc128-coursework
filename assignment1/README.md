# Auto Service Desk Bot

This project is a Streamlit help desk bot for an auto service shop. The bot creates a ticket based on the service areas described: electrical, drivability, interior, exterior, or maintenance.

## How to run the chatbot

```
streamlit run helpdesk_bot.py
```

## How to run the tests

```
python test_helpdesk.py
```

## Failure Cases

These are messages the bot handles badly because it does not fully support the user's request. For each one, this section lists the message, what the bot said, and why it failed.

1. **Message:** "How much does a repair cost?"

   **Bot response:** "I can help with electrical, drivability, interior, exterior, and maintenance issues. What problem are you having with the vehicle?"

   **Why it failed:** The bot does not have pricing keywords, so it cannot estimate cost.

2. **Message:** "My car smells weird."

   **Bot response:** "I can help with electrical, drivability, interior, exterior, and maintenance issues. What problem are you having with the vehicle?"

   **Why it failed:** The message is too vague and does not include a keyword like engine, oil, battery, seat, dent, or brakes.

3. **Message:** "Can I schedule an appointment?"

   **Bot response:** "I can help with electrical, drivability, interior, exterior, and maintenance issues. What problem are you having with the vehicle?"
   
   **Why it failed:** The bot routes vehicle problems to departments, but it does not handle scheduling requests.

## What I Would Improve With More Time

With more time and moving outside the scope of the assignment, I would have the bot handle scheduling, price estimates, and follow-up questions to better narrow the scope of work. I would also improve the GUI to make it look better and feel more polished for the user.
