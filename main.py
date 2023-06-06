import logging
import os
from dotenv import load_dotenv

from fastapi import FastAPI, UploadFile
from playwright.async_api import async_playwright

app = FastAPI()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

@app.post("/")
async def upload(file: UploadFile):
    contents = await file.read()
    string_data = contents.decode("utf-8")
    companies = string_data.split("\n")

    response = list()

    logger.info("Launching Playwright")
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        logger.info("Trying to authenticate to LinkedIn")
        await page.goto(f"https://www.linkedin.com/")
        form_exists = await page.wait_for_selector('form[data-id="sign-in-form"]', timeout=0) is not None

        if form_exists:
            await page.fill("input#session_key", LINKEDIN_EMAIL)
            await page.fill("input#session_password", password)
            await page.click("button.sign-in-form__submit-btn--full-width") 
            await page.wait_for_load_state()
            logger.info("Authentication form was found")

        logger.info("Reading the files and fetching data from company page")
        for company_name in companies:
            logger.info(company_name)
            await page.goto(f"https://www.linkedin.com/company/{company_name}")

            await page.wait_for_selector("span.org-top-card-secondary-content__see-all")
            number_of_employees = await page.inner_text(".org-top-card-secondary-content__see-all")
            
            response.append({"company": company_name, "employees": number_of_employees})

    return response
