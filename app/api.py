from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from main import load_webpage_content

# Initialize our models
chain = Chain()
portfolio = Portfolio()

# Create FastAPI app
app = FastAPI(title="Cold Email Generator API")

# Add CORS middleware to allow cross-origin requests from our frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API requests/responses
class URLRequest(BaseModel):
    url: str

class Skill(BaseModel):
    name: str

class JobDetails(BaseModel):
    role: str
    experience: str
    skills: List[str]
    description: str

class PortfolioLink(BaseModel):
    url: str

class GeneratedEmail(BaseModel):
    email: str
    job_details: JobDetails
    portfolio_links: List[str]

@app.get("/")
async def root():
    """Root endpoint to check if API is running"""
    return {"message": "Cold Email Generator API is running"}

@app.post("/api/generate-email", response_model=GeneratedEmail)
async def generate_email(request: URLRequest):
    """Generate a cold email based on a job listing URL"""
    try:
        # Load the webpage content
        data = load_webpage_content(request.url)
        
        # Clean and process the data
        cleaned_data = clean_text(data)
        
        # Load portfolio and extract job details
        portfolio.load_portfolio()
        jobs = chain.extract_jobs(cleaned_data)
        
        if not jobs:
            raise HTTPException(
                status_code=404, 
                detail="No job details could be extracted from the provided URL."
            )
        
        # Get the first job
        job = jobs[0]
        skills = job.get('skills', [])
        
        # Query relevant portfolio links
        metadata_list = portfolio.query_links(skills)
        links = [item.get('links', '') for item in metadata_list]
        
        # Generate email
        email = chain.write_mail(job, links)
        
        return GeneratedEmail(
            email=email,
            job_details=JobDetails(
                role=job.get('role', 'N/A'),
                experience=job.get('experience', 'N/A'),
                skills=job.get('skills', []),
                description=job.get('description', 'N/A')
            ),
            portfolio_links=links
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 