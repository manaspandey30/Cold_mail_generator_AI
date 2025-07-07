import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import COMPANY_NAME, FOUNDER_NAME, COMPANY_DESCRIPTION, PORTFOLIO_LINK_1, PORTFOLIO_LINK_2


def load_webpage_content(url):
    """Load webpage content with multiple fallback options"""
    st.info("Loading webpage content... This may take a moment.")
    content = ""
    
    # First try with requests for speed
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.text
            if len(content) > 5000:  # If we got a substantial amount of content
                st.success("Successfully loaded content with requests")
                return content
    except Exception as e:
        st.warning(f"Requests method failed: {e}. Trying Selenium...")
    
    # Try with Selenium as fallback with more robust handling
    try:
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Use ChromeDriverManager to automatically handle driver installation
        try:
            service = Service()
            driver = webdriver.Chrome(options=chrome_options, service=service)
        except:
            st.warning("Using ChromeDriverManager to install driver")
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(options=chrome_options, service=service)
        
        # Navigate to the URL
        driver.get(url)
        
        # Wait longer for the page to load fully
        st.info("Waiting for page to load completely...")
        time.sleep(10)
        
        try:
            # Wait for specific content to be present
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except:
            st.warning("Timed out waiting for page elements, but continuing...")
        
        # Scroll down to ensure dynamic content loads
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        # Extract the full page content
        content = driver.page_source
        
        # Close the webdriver
        driver.quit()
        
        if content:
            st.success("Successfully loaded content with Selenium")
            return content
        else:
            st.error("Failed to extract content with Selenium")
    except Exception as e:
        st.error(f"Selenium extraction failed: {e}")
    
    # Last resort: Try WebBaseLoader
    try:
        loader = WebBaseLoader([url])
        data = loader.load()
        content = data[0].page_content
        st.success("Successfully loaded content with WebBaseLoader")
        return content
    except Exception as e:
        st.error(f"WebBaseLoader failed: {e}")
    
    if not content:
        raise Exception("Failed to load webpage content through all available methods")
    
    return content


def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    
    # Create a nice layout
    st.title("📧 Cold Email Generator")
    st.write("Enter a job listing URL and get a personalized cold email based on the job details.")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Generate Email", "Company Settings", "About", "Help"])
    
    with tab1:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Custom URL input only
            url_input = st.text_input("Enter a job listing URL:", placeholder="https://example.com/job-listing")
        
        with col2:
            st.write("")
            st.write("")
            submit_button = st.button("Generate Cold Email", type="primary", use_container_width=True)
    
        if submit_button and url_input:
            try:
                # Add a progress bar
                progress_bar = st.progress(0)
                
                with st.spinner("Loading webpage content..."):
                    data = load_webpage_content(url_input)
                    progress_bar.progress(25)
                
                with st.spinner("Cleaning and processing content..."):
                    cleaned_data = clean_text(data)
                    progress_bar.progress(50)
                
                with st.spinner("Analyzing job details..."):
                    portfolio.load_portfolio()
                    jobs = llm.extract_jobs(cleaned_data)
                    progress_bar.progress(75)
                
                # Complete the progress bar
                progress_bar.progress(100)
                
                if jobs:
                    # Display job details in expander
                    with st.expander("Job Details", expanded=False):
                        job = jobs[0]
                        st.write(f"**Role:** {job.get('role', 'N/A')}")
                        st.write(f"**Experience:** {job.get('experience', 'N/A')}")
                        st.write(f"**Skills:** {', '.join(job.get('skills', []))}")
                        st.write(f"**Description:** {job.get('description', 'N/A')}")
                    
                    # Generate email for the first job
                    job = jobs[0]
                    skills = job.get('skills', [])
                    
                    # Get company settings from session state or use defaults from config
                    company_name = st.session_state.get('company_name', COMPANY_NAME)
                    founder_name = st.session_state.get('founder_name', FOUNDER_NAME)
                    company_description = st.session_state.get('company_description', COMPANY_DESCRIPTION)
                    
                    # Get custom portfolio links
                    custom_links = []
                    portfolio_link1 = st.session_state.get('portfolio_link1', PORTFOLIO_LINK_1)
                    portfolio_link2 = st.session_state.get('portfolio_link2', PORTFOLIO_LINK_2)
                    if portfolio_link1:
                        custom_links.append(portfolio_link1)
                    if portfolio_link2:
                        custom_links.append(portfolio_link2)
                    
                    # Use custom links if available, otherwise use AI-selected links
                    links = portfolio.query_links(skills, custom_links if custom_links else None)
                    
                    with st.spinner("Generating cold email..."):
                        email = llm.write_mail(job, links, company_name, founder_name, company_description)
                    
                    # Show the email in a nice box
                    st.subheader("📤 Your Generated Cold Email:")
                    st.code(email, language='markdown')
                    
                    # Add copy button
                    st.download_button(
                        label="Download Email as Text",
                        data=email,
                        file_name="cold_email.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("No job details could be extracted from the provided URL.")
            except Exception as e:
                st.error(f"An Error Occurred: {str(e)}")
                with st.expander("Error Details"):
                    import traceback
                    st.code(traceback.format_exc())
    
    with tab2:
        st.subheader("🏢 Company Settings")
        st.write("Configure your company details for personalized email generation.")
        
        # Company settings form
        with st.form("company_settings"):
            col1, col2 = st.columns(2)
            
            with col1:
                company_name = st.text_input(
                    "Company Name", 
                    value=st.session_state.get('company_name', COMPANY_NAME),
                    placeholder="e.g., TechCorp Solutions"
                )
                founder_name = st.text_input(
                    "Your Name", 
                    value=st.session_state.get('founder_name', FOUNDER_NAME),
                    placeholder="e.g., John Smith"
                )
            
            with col2:
                company_description = st.text_area(
                    "Company Description", 
                    value=st.session_state.get('company_description', COMPANY_DESCRIPTION),
                    placeholder="e.g., a leading AI & Software Consulting company",
                    height=100
                )
                
                # Portfolio Links Section
                st.subheader("📁 Portfolio Links")
                st.write("Add your portfolio links that will be included in emails:")
                
                portfolio_link1 = st.text_input(
                    "Portfolio Link 1",
                    value=st.session_state.get('portfolio_link1', PORTFOLIO_LINK_1),
                    placeholder="https://your-portfolio1.com"
                )
                
                portfolio_link2 = st.text_input(
                    "Portfolio Link 2", 
                    value=st.session_state.get('portfolio_link2', PORTFOLIO_LINK_2),
                    placeholder="https://your-portfolio2.com"
                )
            
            if st.form_submit_button("Save Settings"):
                st.session_state['company_name'] = company_name
                st.session_state['founder_name'] = founder_name
                st.session_state['company_description'] = company_description
                st.session_state['portfolio_link1'] = portfolio_link1
                st.session_state['portfolio_link2'] = portfolio_link2
                st.success("Company settings saved successfully!")
        
        # Show current settings
        st.subheader("Current Settings")
        st.write(f"**Company:** {st.session_state.get('company_name', COMPANY_NAME)}")
        st.write(f"**Contact Person:** {st.session_state.get('founder_name', FOUNDER_NAME)}")
        st.write(f"**Description:** {st.session_state.get('company_description', COMPANY_DESCRIPTION)}")
        
        # Show portfolio links
        portfolio_link1 = st.session_state.get('portfolio_link1', PORTFOLIO_LINK_1)
        portfolio_link2 = st.session_state.get('portfolio_link2', PORTFOLIO_LINK_2)
        
        if portfolio_link1 or portfolio_link2:
            st.write("**Portfolio Links:**")
            if portfolio_link1:
                st.write(f"• {portfolio_link1}")
            if portfolio_link2:
                st.write(f"• {portfolio_link2}")
        else:
            st.write("**Portfolio Links:** None configured (will use AI-selected links)")
    
    with tab3:
        st.subheader("About This Tool")
        st.write("""
        This tool helps business development executives generate personalized cold emails for potential clients based on job listings.
        
        ### How it works:
        1. It extracts job details from a provided URL
        2. Analyzes the requirements and skills needed
        3. Matches relevant portfolio items from your database
        4. Generates a personalized cold email tailored to the specific job opening
        
        ### Benefits:
        - Save time crafting personalized outreach
        - Ensure relevant portfolio examples are included
        - Maintain a consistent professional tone
        - Increase response rates with targeted content
        """)
        
    with tab4:
        st.subheader("Help & Troubleshooting")
        st.write("""
        ### Common Issues:
        
        **URL Loading Issues**
        - Some job sites use JavaScript to load content which may be harder to extract
        - Try using a direct link to the job description page
        - Corporate firewalls may block web scraping attempts
        
        **No Skills Detected**
        - Try using a URL with more detailed job descriptions
        - Check if the skills section is clearly defined on the job page
        
        **Email Generation Issues**
        - Ensure your API key is valid and has sufficient credits
        - Check your internet connection
        """)


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)