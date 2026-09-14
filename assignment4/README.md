# Auto Shop Appointment Bot (Slot Filling Adaptation)

Calvin A. Prepetit - CSC-128 Assignment 4

This project continues my auto shop bot from earlier assignments.

- Keeps the 5 service departments, chat history, appointment summary, and restart option.
- Adds regular expression extraction, volunteered details, and corrections to saved values.
- Keeps conversation logic separate from the Streamlit interface.

## How to Run

Install the requirements from the project folder, then run the app:

```
python -m pip install -r requirements.txt
streamlit run app.py
```

## How to Run Tests

```
python test_booking.py
```

Verified output:

```
35 out of 35 tests passed.
```

- Covers extraction, invalid input, relative dates, volunteered values, corrections, confirmation, and restarting.
- Failures print the message, expected value, and actual value.
- Returns a nonzero exit status if a test fails.

Run the following command to reproduce the extraction collision before the fix. This test is expected to fail:

```
python test_booking.py --without-time-fix
```

Verified output:

```
Using the original time pattern. This regression test should fail.
FAILED
Message: Book maintenance for 4 vehicles on Thursday at 3pm
Expected: 3
Actual: 4
```

- This command uses the original time pattern on the full message to reproduce the wrong hour. It does not change any files.
- Exit status 1 is expected for this command. The corrected extractor passes the same test in the normal run.

## Slots and Conversation Flow

- **Required slots:** service department, day, and time.
- **Optional slot:** number of vehicles.
- **Departments:** electrical, drivability, interior, exterior, and maintenance.
- **Service matching:** department names and selected issue words identify the service. "My battery keeps dying" selects Electrical; the full issue description is not saved.
- **Matching:** uses service keywords from the earlier bot with regular expressions. A request can include multiple departments. Capitalization, punctuation, and extra spaces are handled.
- **Additional services:** "check my bumper too" adds Exterior to the existing services. Use "also", "add", "too", or "as well" to add services; "electrical instead" replaces the selection. Confirmation includes every selected department.
- **Volunteered details:** every message is checked for all slots. Normal collection fills only empty slots and asks only for missing details.
- **Example:** "Maintenance on Thursday at 3pm for two vehicles" supplies all 4 values and moves directly to confirmation.
- **Corrections:** phrases such as `make it`, `let's do`, `switch to`, `actually`, `no wait`, and `instead` replace saved values. The bot acknowledges the change.
- **Schedule changes:** new details such as "Saturday at 8am" also update an appointment awaiting confirmation or already confirmed. The bot reads back the changes and asks for confirmation again.
- **Availability:** the bot records your preferred schedule but cannot check shop availability.
- **Confirmation:** the bot reads back all details before confirming the appointment. Answering "no" lets the customer make changes. Updated appointments must be confirmed again.
- **Remove vehicle count:** "Actually remove vehicle count" clears the optional quantity.
- **Restart:** `restart`, `start over`, and `cancel` clear the appointment. The Start Over button also clears chat history.
- **Conversation history:** the bot remembers appointment details as the customer provides or changes them.

## Documented Extraction Collision

Triggering message:

```
Book maintenance for 4 vehicles on Thursday at 3pm
```

- **Problem:** the original time extractor accepts a number without minutes or am/pm. It finds `4` before reaching `3pm` and incorrectly returns `4:00`.
- **Why this is a collision:** the vehicle extractor correctly reads `4` as the vehicle count, but the original time extractor also reads that same number as a time.
- **Correct result:** `4` vehicles with an appointment time of `3:00 PM`.
- **Fix:** the time extractor requires a colon or am/pm, so it skips the bare `4` and reads `3pm`. The bot also removes vehicle quantities from the message before extracting the time.
- **Test:** the `--without-time-fix` command shown above runs the time extractor on this message using the original pattern. It fails because the expected hour is `3`, but the original pattern returns `4`.

## Supported Input and Limitations

- **Days:** full weekday names.
- **Times:** `3pm`, `3 pm`, `3:30pm`, or `15:00`.
- **Vehicles:** positive digits, written numbers from `one` through `twelve`, `just my car`, or `both cars` (2 vehicles).
- **Relative dates:** for phrases like "tomorrow" or "next Tuesday", the bot asks for a specific weekday and keeps the other appointment details.
- **Scope:** multiple service departments can share one appointment day, time, and optional vehicle count. Negated details such as "not Thursday" and general spelling correction are not supported.
- **Storage:** appointments are stored only in the current session.

## What I Would Improve With More Time

With more time, I would add actual dates and check shop availability before confirming an appointment. I would also save appointments to a database to make the bot more useful for practical use beyond the current session.
