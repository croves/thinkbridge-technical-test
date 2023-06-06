# Python Compatibility Test

This is my technical assessment for thinkbridge.in


# Setting up
Create a Python3 virtual environment:
`python3 -m venv .venv`

Activate and install dependencies
```
source .venv/bin/activate
pip install -r requirements.txt
```
Set-up Playwright
```
sudo playwright install
sudo playwright install-deps
```
Start server
`uvicorn main:app --reload`

Go to http://127.0.0.1:8000/docs

Quick note: I was struggling with authentication in LinkedIn. The auth wall changes after a certain ammount of requests to make it harder to scrape.