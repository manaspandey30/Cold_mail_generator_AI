import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from a job listing page of a company website.
            Extract the key details and return them in JSON format containing the following keys:
            - `role`: The job title or position being advertised
            - `experience`: Any mentioned experience requirements
            - `skills`: A list of required skills or technologies (as array)
            - `description`: A summary of the job description
            
            Even if some information is missing, extract what you can find.
            Format the output as valid JSON only, with no additional text.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            # If parsing fails, try a simpler approach with basic job structure
            fallback_job = {
                "role": "Job Position",
                "experience": "Not specified",
                "skills": ["Not specified"],
                "description": "The job description could not be parsed correctly."
            }
            
            # Try to at least extract the job title from the text
            if "Data Engineer" in cleaned_text:
                fallback_job["role"] = "Data Engineer"
            elif "Software Engineer" in cleaned_text:
                fallback_job["role"] = "Software Engineer"
            elif "Developer" in cleaned_text:
                fallback_job["role"] = "Developer"
            
            # Include some of the cleaned text as description
            max_text_length = min(1000, len(cleaned_text))
            fallback_job["description"] = cleaned_text[:max_text_length] + "..."
            
            return [fallback_job]
            
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links, company_name="Your Company", founder_name="Your Name", company_description="a leading technology consulting company"):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are {founder_name}, a business development executive at {company_name}. {company_name} is {company_description} dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of {company_name} 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase {company_name}'s portfolio: {link_list}
            Remember you are {founder_name}, BDE at {company_name}. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job), 
            "link_list": links,
            "company_name": company_name,
            "founder_name": founder_name,
            "company_description": company_description
        })
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))