from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI
import os
import json
import requests

load_dotenv()

app = FastAPI(title="ServiceNow AI Change Risk Advisor")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.get("/")
def home():
    return {"message": "ServiceNow AI Change Risk Advisor is running"}


@app.get("/check-env")
def check_env():
    return {
        "openai_key_loaded": bool(os.getenv("OPENAI_API_KEY")),
        "servicenow_url_loaded": bool(os.getenv("SERVICENOW_INSTANCE_URL")),
        "servicenow_username_loaded": bool(os.getenv("SERVICENOW_USERNAME")),
        "servicenow_password_loaded": bool(os.getenv("SERVICENOW_PASSWORD")),
    }


@app.get("/change/{change_number}")
def get_change(change_number: str):
    instance_url = os.getenv("SERVICENOW_INSTANCE_URL")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    url = (
        f"{instance_url}/api/now/table/change_request"
        f"?sysparm_query=number={change_number}"
        "&sysparm_limit=1"
        "&sysparm_fields=number,short_description,description,type,risk,impact,priority,state,implementation_plan,backout_plan,test_plan,justification,start_date,end_date"
    )

    response = requests.get(
        url,
        auth=(username, password),
        headers={"Accept": "application/json"},
        timeout=30,
    )

    data = response.json()

    if not data.get("result"):
        return {"error": f"Change {change_number} not found"}

    return data["result"][0]


@app.get("/ai-change/{change_number}")
def analyze_change(change_number: str):
    change = get_change(change_number)

    if "error" in change:
        return change

    return analyze_change_with_ai(change)


def analyze_change_with_ai(change: dict):
    prompt = f"""
You are a ServiceNow ITSM Change Risk Advisor.

Analyze this ServiceNow Change Request.

Change:
Number: {change.get("number")}
Short Description: {change.get("short_description")}
Description: {change.get("description")}
Type: {change.get("type")}
Risk: {change.get("risk")}
Impact: {change.get("impact")}
Priority: {change.get("priority")}
State: {change.get("state")}
Implementation Plan: {change.get("implementation_plan")}
Backout Plan: {change.get("backout_plan")}
Test Plan: {change.get("test_plan")}
Justification: {change.get("justification")}
Start Date: {change.get("start_date")}
End Date: {change.get("end_date")}

Return STRICT JSON only:
{{
  "change_summary": "...",
  "risk_score": "Low | Medium | High | Critical",
  "risk_reasoning": "...",
  "rollback_assessment": "...",
  "test_plan_review": "...",
  "affected_services": ["...", "..."],
  "cab_recommendation": "...",
  "implementation_advice": "...",
  "approval_recommendation": "Approve | Reject | Needs More Information"
}}

Rules:
- If backout plan is missing or weak, increase risk.
- If test plan is missing or weak, increase risk.
- If implementation plan is missing, recommend Needs More Information.
- If risk or impact is high, recommend CAB review.
- Return JSON only, no markdown.
"""

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert ServiceNow Change Management analyst. Always return valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    ai_text = ai_response.choices[0].message.content

    try:
        parsed = json.loads(ai_text)
    except Exception:
        parsed = {
            "change_summary": ai_text,
            "risk_score": "Unknown",
            "risk_reasoning": "",
            "rollback_assessment": "",
            "test_plan_review": "",
            "affected_services": [],
            "cab_recommendation": "",
            "implementation_advice": "",
            "approval_recommendation": "Needs More Information",
        }

    return {
        "change": change,
        "structured_ai": parsed,
    }