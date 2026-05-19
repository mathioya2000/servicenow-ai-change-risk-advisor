\# ServiceNow AI Change Risk Advisor



\## Overview

AI-powered ServiceNow Change Management assistant that analyzes change requests and provides structured risk guidance.



This project integrates:



\- ServiceNow Change Management

\- FastAPI backend

\- OpenAI API

\- Render cloud deployment

\- ServiceNow UI Action

\- GlideAjax Script Include



\## Business Use Case

Change Advisory Boards (CAB) and IT teams need fast risk assessment for change requests.



This assistant provides:



\- change summary

\- risk scoring

\- risk reasoning

\- rollback assessment

\- test plan review

\- affected services analysis

\- CAB recommendation

\- implementation advice

\- approval recommendation



\---



\## Architecture



ServiceNow Change Record  

↓  

UI Action: Analyze Change Risk  

↓  

GlideAjax Script Include  

↓  

FastAPI REST API on Render  

↓  

OpenAI Analysis Engine  

↓  

Structured JSON Response  

↓  

ServiceNow Work Notes  



\---



\## API Endpoints



\### Health Check

GET /



\### AI Change Analysis

GET /ai-change/{change\_number}



Example:



/ai-change/CHG0000009



\---



\## Key Features



\- change risk scoring

\- rollback analysis

\- CAB guidance

\- approval intelligence

\- affected service prediction

\- implementation recommendations



\---



\## Tech Stack



\- Python

\- FastAPI

\- OpenAI API

\- ServiceNow

\- GlideAjax

\- RESTMessageV2

\- Render

\- GitHub



\---



\## ServiceNow Components



\### UI Action

Change Request \[change\_request]



Button:



Analyze Change Risk



\### Script Include

AIChangeRiskAdvisorAjax



\### Output

Writes structured AI risk analysis into Change Work Notes.



\---



\## Deployment



Hosted on Render.



Environment variables:



OPENAI\_API\_KEY  

SERVICENOW\_INSTANCE\_URL  

SERVICENOW\_USERNAME  

SERVICENOW\_PASSWORD  



\---



\## Portfolio Value



Demonstrates:



\- Change Management automation

\- CAB decision support

\- AI integration

\- enterprise workflow automation

\- ServiceNow development

\- cloud deployment



\---



\## Author



Joseph Mwangi

