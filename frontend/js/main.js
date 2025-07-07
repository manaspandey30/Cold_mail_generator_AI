// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const urlSelect = document.getElementById('urlSelect');
    const customUrlContainer = document.getElementById('customUrlContainer');
    const customUrlInput = document.getElementById('customUrl');
    const generateBtn = document.getElementById('generateBtn');
    const resultsArea = document.getElementById('resultsArea');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsContent = document.getElementById('resultsContent');
    const progressBar = document.getElementById('progressBar');
    const copyEmailBtn = document.getElementById('copyEmailBtn');
    const downloadEmailBtn = document.getElementById('downloadEmailBtn');
    const emailPreview = document.getElementById('emailPreview');
    const jobRole = document.getElementById('jobRole');
    const jobExperience = document.getElementById('jobExperience');
    const jobSkills = document.getElementById('jobSkills');
    const jobDescription = document.getElementById('jobDescription');
    const portfolioLinks = document.getElementById('portfolioLinks');
    
    // Notification modal
    const notificationModal = new bootstrap.Modal(document.getElementById('notificationModal'));
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    
    // Show/hide custom URL input based on selection
    urlSelect.addEventListener('change', function() {
        if (this.value === 'custom') {
            customUrlContainer.style.display = 'block';
            customUrlInput.required = true;
        } else {
            customUrlContainer.style.display = 'none';
            customUrlInput.required = false;
        }
    });
    
    // Generate email function
    function generateEmail() {
        // Get URL
        const selectedUrl = urlSelect.value === 'custom' ? customUrlInput.value : urlSelect.value;
        
        // Validate URL
        if (!selectedUrl || selectedUrl === 'custom') {
            showNotification('Error', 'Please enter a valid URL');
            return;
        }
        
        // Show loading section
        resultsArea.style.display = 'block';
        loadingSpinner.style.display = 'block';
        resultsContent.style.display = 'none';
        
        // Scroll to results
        resultsArea.scrollIntoView({ behavior: 'smooth' });
        
        // Start progress animation
        simulateProgress();
        
        // Instead of calling API, redirect to the Streamlit app with the URL as a parameter
        // This will work if the user already has Streamlit running
        const streamlitUrl = `http://localhost:8501/?url=${encodeURIComponent(selectedUrl)}`;
        window.open(streamlitUrl, '_blank');
        
        // After a short delay, show an info message
        setTimeout(() => {
            // Hide loading spinner
            loadingSpinner.style.display = 'none';
            
            // Show notification
            showNotification('Info', 'Redirected to Streamlit app for email generation. You can now use the Streamlit interface to complete the process.');
            
            // Show demo data for preview
            resultsContent.style.display = 'block';
            
            // Use mock data to demonstrate how results would appear
            const mockJobDetails = {
                role: "Data Engineer",
                experience: "3+ years of experience with big data technologies",
                skills: ["Python", "SQL", "Hadoop", "Spark", "Data Warehousing", "ETL", "Machine Learning"],
                description: "We are looking for a Data Engineer to build and maintain data pipelines and infrastructure. The ideal candidate will have experience with big data technologies, strong programming skills, and a passion for building scalable data solutions."
            };
            
            const mockPortfolioLinks = [
                "https://example.com/python-portfolio",
                "https://example.com/ml-python-portfolio"
            ];
            
            const mockEmail = `Subject: AtliQ's Data Engineering Solutions for Your Team

Dear Hiring Manager,

I noticed your job listing for a Data Engineer position and wanted to reach out. AtliQ specializes in providing dedicated data engineering solutions that can help you scale your data infrastructure without the lengthy hiring process.

Our team has extensive experience with Python, SQL, Hadoop, and Spark - all technologies mentioned in your requirements. We've successfully delivered data pipeline and warehouse solutions for companies in similar industries.

I'd love to share more about how our dedicated engineers could support your team. You might be interested in reviewing some of our previous work:
- Python data engineering project: https://example.com/python-portfolio
- Machine learning integration: https://example.com/ml-python-portfolio

Would you be available for a brief call next week to discuss how AtliQ could support your data engineering needs?

Best regards,
Mohan K.
Business Development Executive
AtliQ
mohan@atliq.com
+91 9876543210`;
            
            // Populate with mock data as example
            populateJobDetails(mockJobDetails);
            populatePortfolioLinks(mockPortfolioLinks);
            populateEmailPreview(mockEmail);
            
            // Add note about demonstration
            const demoNote = document.createElement('div');
            demoNote.className = 'alert alert-info mt-3';
            demoNote.innerHTML = `<strong>Note:</strong> This is sample data shown for demonstration. The actual email generation is taking place in the Streamlit app that opened in a new tab.`;
            resultsContent.prepend(demoNote);
        }, 2000);
    }
    
    // Populate job details
    function populateJobDetails(job) {
        jobRole.textContent = job.role;
        jobExperience.textContent = job.experience || 'Not specified';
        
        // Create skill tags
        if (job.skills && job.skills.length > 0) {
            jobSkills.innerHTML = '';
            job.skills.forEach(skill => {
                const skillTag = document.createElement('span');
                skillTag.classList.add('skill-tag');
                skillTag.textContent = skill;
                jobSkills.appendChild(skillTag);
            });
        } else {
            jobSkills.textContent = 'No specific skills mentioned';
        }
        
        jobDescription.textContent = job.description || 'No description provided';
    }
    
    // Populate portfolio links
    function populatePortfolioLinks(links) {
        if (links && links.length > 0) {
            portfolioLinks.innerHTML = '';
            links.forEach(link => {
                const linkElement = document.createElement('a');
                linkElement.href = link;
                linkElement.target = '_blank';
                linkElement.classList.add('portfolio-link');
                linkElement.innerHTML = `<i class="fas fa-external-link-alt"></i> ${link}`;
                portfolioLinks.appendChild(linkElement);
            });
        } else {
            portfolioLinks.innerHTML = '<p>No relevant portfolio links found</p>';
        }
    }
    
    // Populate email preview
    function populateEmailPreview(email) {
        emailPreview.textContent = email;
    }
    
    // Simulate progress bar advancement
    function simulateProgress() {
        let progress = 0;
        progressBar.style.width = '0%';
        
        const interval = setInterval(() => {
            progress += 5;
            progressBar.style.width = `${progress}%`;
            
            if (progress >= 100) {
                clearInterval(interval);
            }
        }, 150);
    }
    
    // Copy email to clipboard
    copyEmailBtn.addEventListener('click', function() {
        const emailText = emailPreview.textContent;
        navigator.clipboard.writeText(emailText).then(() => {
            showNotification('Success', 'Email copied to clipboard!');
        }, () => {
            showNotification('Error', 'Failed to copy email. Please try again.');
        });
    });
    
    // Download email as text file
    downloadEmailBtn.addEventListener('click', function() {
        const emailText = emailPreview.textContent;
        const blob = new Blob([emailText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = 'cold_email.txt';
        document.body.appendChild(a);
        a.click();
        
        // Cleanup
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showNotification('Success', 'Email downloaded successfully!');
    });
    
    // Show notification
    function showNotification(title, message) {
        modalTitle.textContent = title;
        modalBody.textContent = message;
        notificationModal.show();
        
        // Auto hide after 5 seconds
        setTimeout(() => {
            notificationModal.hide();
        }, 5000);
    }
    
    // Initialize
    function init() {
        // Set up event listeners
        generateBtn.addEventListener('click', generateEmail);
        
        // Initialize URL selector
        urlSelect.dispatchEvent(new Event('change'));
        
        // Add info alert about the app
        const infoAlert = document.createElement('div');
        infoAlert.className = 'alert alert-primary mt-3';
        infoAlert.innerHTML = `<strong>How this works:</strong> When you click "Generate Email", you'll be redirected to the Streamlit app that's running on port 8501. Make sure the Streamlit app is running before clicking the button.`;
        document.querySelector('.url-selector').appendChild(infoAlert);
    }
    
    // Call init function
    init();
}); 