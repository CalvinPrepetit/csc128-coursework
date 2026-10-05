# Auto Shop Service Advisor

Calvin A. Prepetit - CSC-128 Assignment 7

This continues my auto shop theme using the assignment's model-driven tool loop.
The model interprets the conversation and requests tools. Python checks the name,
validates arguments, executes allowed tools, and returns their results to the model.
Ordinary hours and appointment questions use the model, not a separate local intake bot.

## Tools and Safety

- `get_shop_hours(day="all")`: read the weekly schedule or 1 day's hours.
- `find_service_openings(service_type)`: read available maintenance, diagnostic, or brake slots.
- `create_service_request(customer_name, vehicle, concern, day, time)`: save an available request after confirmation.

Each tool has a JSON schema whose description explains when to call it.
Oil changes and rotations use maintenance; brake-only requests use brakes;
other concerns use diagnostic intake, not a promise of completed repairs.
Reported faults take priority over suggested maintenance: noise or suspected
transmission failure uses diagnostic even if the customer suggests a fluid change.
The fictional schedule repeats by weekday. Requests stay in the current browser
session; refreshing can clear them. Saved slots are removed from availability.

The loop stops when the model answers without tool calls or reaches the 5-round cap.
Tool names are checked before lookup. Malformed JSON, wrong arguments, and tool
exceptions become error results returned to the model. Failed calls appear in the
sidebar with their name, arguments, and result, just like successful calls.

A write proposal displays the exact name, vehicle, original concern, day, and time.
No record is saved until the customer confirms that preview. Corrections require
a new proposal. No or cancel leaves the draft unsaved, and repeated yes does not
create a duplicate. Python validates fields and availability again before saving.
Equivalent times such as 9am and 9:00 AM are normalized before checking the slot;
an invalid time or a missing AM/PM is rejected rather than guessed.
The model helps with language but cannot commit an unconfirmed request.
Changing only the day requires choosing its offered time before a new preview.
Python rejects a write proposal on a weekday-only turn rather than accepting a
model-guessed time. Natural replies to a preview are interpreted by the model as
confirm, revise, cancel, decline, question, or other. Python checks the decision
and saves only the unchanged displayed fields on confirm. Corrections need a new
preview; malformed or unclear decisions never save. A question alone is not consent,
but clear agreement followed by asking what happens next can confirm the preview.
The explicit Confirm button and a plain yes still work without another model call.
Model prose claiming a completed booking is replaced with an honest no-save message;
successful saves are reported by Python.
A simple thank-you keeps the pending preview; it does not count as confirmation.
The bot cannot edit or add notes to saved records. Unsupported pricing and warranty
questions are referred to the shop without promises of updates or estimates.

## The Function I Did Not Write

I did not write `delete_all_service_requests`. It could erase customer records
and destroy the schedule. A prompt can be ignored, but a function that does not
exist cannot be called.

An unknown name returns an error and executes nothing.
`test_unknown_name_never_indexes` uses a dictionary that raises if lookup happens,
proving that the name check comes first.

## Tool Description Rewritten

Earlier description:

```text
Use this state-changing tool only after the customer explicitly confirms the exact name, vehicle, concern, day, and time to submit.
```

The bot kept asking verbal confirmation instead of requesting the tool.
The description did not explain that the application owns confirmation.

Rewritten description:

```text
Use this state-changing tool when the customer's name, vehicle, original concern, and an available weekday/time are collected. The application will display those exact fields and require the customer's agreement before executing the write. Request the tool once; do not repeat verbal confirmation questions. When the customer corrects both the day and time, keep their other details and call this tool immediately for a revised preview; do not ask if the selected time works. Never claim a request was saved before receiving its successful result.
```

## Run and Check

From `csc128/assignment7`, activate `..\\.venv\\Scripts\\Activate.ps1`.
From the Module 7 draft, activate `..\\..\\csc128\\.venv\\Scripts\\Activate.ps1`.

```powershell
python -m pip install -r requirements.txt
python test_tools.py
python -m streamlit run app.py
```

Normal chat needs a private `.streamlit/secrets.toml` containing `GROQ_API_KEY`.
Never commit or attach it. Check `git check-ignore -v assignment7/.streamlit/secrets.toml`
from the course repository. The model is `openai/gpt-oss-20b`, used in my earlier work.

The 15 tests need no API key or network. A fake client checks multiple model rounds,
the cap, errors returned as tool messages, exact previews, revisions, cancellation,
and duplicate prevention. Tests deliberately trigger failures because normal chat
may not cause the model to send malformed arguments or unknown tool names.

For a manual check, ask for hours and oil-change openings. Request an oil change
for a 2020 Chevy Suburban Friday at 9am under your name. Check the tool log and
preview, change to Thursday at 1:30pm, confirm once, and verify 1 saved request.
Say yes again to check duplicates. Start a new intake and cancel before confirming.

## Files and Submission

`tools.py` contains the tools and schemas; `agent.py` contains dispatch, the loop,
history, and confirmation; `app.py` contains the Streamlit chat and tool log.
`test_tools.py` contains the tests. The remaining safe files are this README,
`requirements.txt`, and `.gitignore`. Dependencies are only Streamlit and Groq.

Publish the reviewed assignment7 folder to the public course repository, paste
its link into Brightspace, and attach all 4 Python files and this README directly.
The ZIP includes only these 7 safe files, not secrets, caches, or the environment.
With more time, I would add shop-approved persistent scheduling and a reviewed
technician summary beside the original customer concern.
