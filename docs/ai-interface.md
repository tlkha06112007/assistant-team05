# AI service interface

Specification of the LLM-backed responder that will replace (or sit in front of)
the current rule-based one in `src/assistant/rules.py`.

**Status: specification only. No LLM call is implemented yet.** The function
below describes the contract a future implementation must satisfy; today the
assistant answers with `assistant.rules.reply()`.

## Scope

- In scope: the public function contract, its inputs and outputs, the errors it
  raises, and the fallback behaviour when the model is unavailable.
- Out of scope: prompt wording, model/vendor choice, token limits, cost.

## Function signature

```python
def ask_llm(
    message: str,
    offices: dict[str, dict[str, str]] | None = None,
    *,
    timeout: float = 5.0,
) -> str:
    """Answer a student question about university offices.

    Args:
        message: the raw user question, e.g. "where is the training office?".
        offices: {office_name_lower: row} from `data/offices.csv`. Loaded from
            disk when None.
        timeout: seconds to wait for the model before falling back.

    Returns:
        A human-readable answer, e.g.
        "Training Office: room I.101, open Mon-Fri 07:30-16:30."

    Raises:
        LLMError: the model was unreachable, timed out, or returned an
            unusable response.
    """
```

The signature deliberately mirrors `assistant.rules.reply(message, offices)` so
the two can be swapped without touching callers.

## Inputs

| Name | Type | Required | Notes |
|---|---|---|---|
| `message` | `str` | yes | Free-form question. Stripped and lower-cased before lookup. Empty or whitespace-only input is rejected. |
| `offices` | `dict[str, dict[str, str]]` | no | Keys are office names lower-cased; values are `data/offices.csv` rows with keys `name`, `room`, `hours`. Loaded from disk when `None`. |
| `timeout` | `float` | no (kw-only) | Seconds to wait for the model. Default `5.0`. Must be positive. |

Source of truth for the data shape is `assistant.rules.load_offices()`.

## Outputs

Returns a single `str`. No structured/streaming output in this iteration.

- Answers must be grounded in `offices` only — the assistant states room numbers
  and opening hours, it does not invent them.
- Answer format follows the existing rule-based responder:
  `"<Office name>: room <room>, open <hours>."`
- Empty or whitespace-only `message` returns
  `"Please type a question."` rather than raising.

## Errors

All failures are surfaced as a single exception type so callers do not have to
know which vendor failed.

| Condition | Behaviour |
|---|---|
| Model unreachable (network/auth error) | raise `LLMError` |
| Model did not answer within `timeout` | raise `LLMError` |
| Model returned empty or unparsable output | raise `LLMError` |
| `message` is empty or whitespace | return the prompt message, do **not** raise |
| `offices` file missing or malformed | propagate the underlying `OSError` / `ValueError` |

```python
class LLMError(RuntimeError):
    """The language model could not produce a usable answer."""
```

## Fallback

`ask_llm` never returns a degraded answer itself — it raises. Fallback is the
caller's decision, so that the log records when the model was skipped:

```python
try:
    answer = ask_llm(message, offices)
except LLMError:
    answer = rules.reply(message, offices)  # deterministic, offline
```

Rules for the fallback path:

1. Fall back on **any** `LLMError`, never on a partial answer.
2. The fallback answer must come from `rules.reply()` so the app keeps working
   with no network and no API key.
3. Log the reason (timeout / error / empty output) at WARNING level, without
   logging the student's message verbatim.
4. The user must not be able to tell the difference between a real answer and
   a fallback answer, other than wording quality.

`data/offices.csv` is the only knowledge source either way, so both paths give
consistent facts.
