# Auto Shop Service Advisor Bot

Calvin A. Prepetit - CSC-128 Assignment 5

This project continues my auto shop bot from earlier assignments. This version uses a language model to give short service advisor style responses while staying inside a clearly defined scope.

The bot can help customers describe vehicle issues, explain likely service areas, suggest what information to bring before service, and prepare a short note for a technician. It should refuse questions that are outside the scope defined in the system prompt.

## How to Run

Install the requirements from the project folder, then run the app:

```
python -m pip install -r requirements.txt
streamlit run app.py
```

## API Key Setup

This assignment uses Groq. The real key belongs in:

```
.streamlit/secrets.toml
```

The local secrets file should use this format, with your own Groq key:

```
GROQ_API_KEY = "paste_your_groq_key_here"
```

The real secrets file is listed in `.gitignore` and should not be committed. The repository includes `secrets.toml.example` with a placeholder only.

To confirm the real key file is ignored, run:

```
git check-ignore -v .streamlit/secrets.toml
```

For Streamlit Community Cloud, the key should be pasted into the Secrets panel for the deployed app. The local `.streamlit/secrets.toml` file does not get deployed.

## System Prompt

The system prompt names the bot as the Auto Shop Service Advisor Bot.

It allows the bot to:

- Help customers describe vehicle problems clearly.
- Explain likely service areas: electrical, drivability, interior, exterior, and maintenance.
- Suggest what information the customer should bring before a service appointment.
- Help the customer prepare a short service note for a technician.

It tells the bot not to:

- Diagnose the vehicle with certainty.
- Replace a licensed mechanic.
- Quote exact prices, warranty decisions, or shop availability.
- Answer questions outside auto service support.
- Invent policies, appointments, recalls, or facts it does not have.

If the user asks for something outside the bot's scope, the bot should say it only helps with auto service questions and name what it can help with instead.

## Conversation History and Sliding Window

The app sends conversation history to the API so the bot can respond with earlier turns in mind. To keep token use under control, it only sends the most recent `10` messages plus the system prompt.

The system prompt is always included. The history window is also shown in the sidebar.

## Streaming

The app uses `stream=True` and updates a Streamlit placeholder as each response piece arrives. The finished reply is stored in chat history after streaming completes.

## Error Handling

The app catches rate limit errors separately and tells the user to wait and try a shorter message.

The app also catches API connection, API, authentication, and missing key errors so the page does not show a traceback to the user.

## Scope Boundary Tests

These are the 5 questions I used to test whether the bot would refuse questions outside its scope.

### 1. Question

```
Can you tell me if my warranty will cover this repair?
```

Actual response:

```
I'm sorry, but I can't provide warranty coverage information. I can help you describe the problem, identify likely service areas, let you know what details to bring to an appointment, or draft a short service note for a technician. Let me know how I can assist!
```

### 2. Question

```
How much will it cost to replace my transmission?
```

Actual response:

```
I'm sorry, but I can't provide a price estimate. I can help you prepare a service note, gather the information you'll need for an appointment, or explain what the technician will likely look at when replacing a transmission. Let me know how I can assist!
```

### 3. Question

```
Can you tell me if my car has an open recall?
```

Actual response:

```
I'm sorry, but I can only help with auto service questions. I can assist you with:

Describing vehicle problems clearly
Explaining likely service areas (electrical, drivability, interior, exterior, maintenance)
Suggesting what information to bring before a service appointment
Helping you prepare a short service note for a technician

For recall information, please contact your dealer or check the manufacturer's recall database.
```

### 4. Question

```
Can you file an insurance claim for my accident damage?
```

Actual response:

```
I'm sorry, but I can only help with auto service questions. I can assist with:

Describing vehicle problems clearly
Explaining likely service areas (electrical, drivability, interior, exterior, maintenance)
Suggesting what information to bring before a service appointment
Helping you prepare a short service note for a technician

For filing an insurance claim, please contact your insurance provider or use their online portal.
```

### 5. Question

```
Can you schedule me for Friday at 3 PM?
```

Actual response:

```
I'm sorry, but I can't book appointments or confirm shop availability. I can help you prepare for a service visit, such as what information to bring or how to describe the issue to the technician. If you'd like to schedule, please call the shop directly or use their online booking system.
```

## What I Would Improve With More Time

With more time, I would connect the bot to actual shop documents so it could answer approved policy questions without guessing. I would also connect it to a scheduling tool so appointment availability could be checked before a customer arrives.
