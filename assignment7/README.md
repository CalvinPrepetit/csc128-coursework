# Auto Shop Service Advisor

Calvin A. Prepetit - CSC-128 Assignment 7

For Assignment 7, I continued my auto shop bot by adding tools to check shop hours,
find available service slots, and create a service request after the customer confirms
the details. The model handles the conversation and requests tools. Python validates
those requests, runs the allowed functions, and returns the results to the model.

## Tools

- `get_shop_hours`: shows shop hours for a selected day or the full week.
- `find_service_openings`: shows available appointment times by service category.
- `create_service_request`: saves the customer's request after confirmation.

Each tool has a JSON schema explaining when the model should call it.
The schedule has 7 appointment times across 3 service categories:

- Maintenance: oil changes and tire rotations.
- Brakes: brake-only service.
- Diagnostic: other issues or repairs. Reported faults take priority over routine maintenance.

These are intake appointments, not promises of completed repairs.

## Safety and Limits

- The tool loop stops after an answer or 5 rounds.
- Tool names are checked against the allowed list before lookup.
- Malformed JSON, wrong arguments, and tool exceptions return error results to the model.
- The sidebar logs every requested tool call, its arguments, and its result, including failures.
- The preview shows the name, vehicle, concern, day, and time before confirmation.
- Python validates the fields and available time before saving. Corrections require a new preview.
- The model interprets natural agreement; unclear replies do not save. The Confirm button or plain yes also works.
- No or cancel leaves the request unsaved. Repeating yes does not create a duplicate.
- Requests stay in the browser session; refreshing can clear them. Reserved times are removed from availability.
- The schedule repeats by weekday, not calendar date. Pricing and warranty questions are referred to the shop.

## The Function I Did Not Write

- Omitted function: `delete_all_service_requests`.
- Risk: it could erase customer requests without permission.
- Protection: there is no delete function for the model to call, even if it ignores the prompt.

## Unknown Tools

- An unknown tool name returns an error to the model and executes nothing.
- `test_unknown_name_never_indexes` raises if dictionary lookup occurs, proving the name check comes first.

## Tool Description Rewritten

Earlier description:

```text
Use this state-changing tool only after the customer explicitly confirms
the exact name, vehicle, concern, day, and time to submit.
```

The old description caused repeated confirmation questions instead of a tool request.
The new version tells the model to request a preview and lets Python handle confirmation.

Rewritten description:

```text
Use this state-changing tool when the customer's name, vehicle, original
concern, and an available weekday/time are collected. The application will
display those exact fields and require the customer's agreement before
executing the write. Request the tool once; do not repeat verbal confirmation
questions. When the customer corrects both the day and time, keep their other
details and call this tool immediately for a revised preview; do not ask if
the selected time works. Never claim a request was saved before receiving
its successful result.
```

## Run and Check

Run these commands from `csc128/assignment7`:

```powershell
..\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python test_tools.py
python -m streamlit run app.py
```

- Model: `openai/gpt-oss-20b`.
- Add `GROQ_API_KEY` to the private `.streamlit/secrets.toml`. Never commit or attach it.
- Verify protection from this folder with `git check-ignore -v .streamlit/secrets.toml`.
- The 15 tests require no API key or network. They cover tools, dispatch, the loop, errors, and confirmation using a fake client.

Quick manual check:

1. Ask for shop hours and oil-change openings.
2. Request an oil change for a 2020 Chevy Suburban Friday at 9am. Supply your name.
3. Change to Thursday at 1:30pm, review the new preview, and confirm.
4. Check the log and saved request. Repeat yes to check duplicate protection.
5. Start another request and cancel before confirming.

## Files and Submission

- `tools.py`: tools and schemas.
- `agent.py`: dispatch, tool loop, history, and confirmation.
- `app.py`: Streamlit chat and tool log.
- `test_tools.py`: no-key tests.
- `README.md`, `requirements.txt`, and `.gitignore`: instructions, dependencies, and secret protection.

Push these 7 files to the public repository. Submit its link in Brightspace and
attach all 4 Python files plus this README directly. Do not submit secrets or the virtual environment.

## With More Time

- I would add persistent scheduling so requests survive a refresh.
- I would add a reviewed technician summary alongside the customer's original wording.
