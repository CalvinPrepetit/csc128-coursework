# Auto Shop Appointment Bot

This project is a Streamlit appointment bot for an Auto Shop. The bot helps a customer schedule service by collecting the service area, issue details, an appointment slot, and confirmation.

## How to run the chatbot

```
streamlit run appointment_bot.py
```

## How to run the tests

```
python test_flow.py
```

## Conversation Flow

The bot moves through these stages:

1. choose_department
2. describe_issue
3. choose_slot
4. confirm
5. done

The same input can be handled differently depending on the current stage. For example:

| Current stage | If the user types Monday |
| --- | --- |
| choose_department | The bot does not treat it as a service area and asks which service area the customer needs. |
| choose_slot | The bot treats it as an appointment choice. |
| confirm | The bot does not treat it as confirmation and asks the customer to answer yes or no. |

The bot also supports restart words like cancel, restart, and start over from any stage.

## What I Would Improve With More Time

With more time and moving outside the scope of the assignment, I would add customer names, phone numbers, real appointment availability, and stronger validation for issue details. I would also add CSV files for the keywords and load them into the bot for better matching without cluttering the code. If CSS styling was allowed or appropriate for the assignment, I would also improve the GUI to make it look better and feel more polished for the user.
