"""
Very light-weight synchronous rate-limiter.

Usage
-----
from common.rate_limiter import groq_call
response = groq_call(llm, prompt)
"""
import os, time, threading

# max requests per minute (default = 45, keep 5 req spare for safety)
GROQ_RPM = int(os.getenv("GROQ_RATE_LIMIT_RPM", "45"))
_PERIOD  = 60.0
_lock    = threading.Lock()
_calls   = []                                 # timestamp of each call

def _throttle():
    with _lock:
        now = time.time()
        # Drop timestamps older than 1 minute
        while _calls and now - _calls[0] > _PERIOD:
            _calls.pop(0)
        if len(_calls) >= GROQ_RPM:           # we’re at the limit, sleep
            sleep_for = _PERIOD - (now - _calls[0]) + 0.1
            time.sleep(sleep_for)
        _calls.append(time.time())

def groq_call(llm, prompt, **kwargs):
    """Wrapper around ChatGroq.invoke / __call__ respecting RPM."""
    _throttle()
    return llm.invoke(prompt, **kwargs)       # Works for LangChain ChatGroq