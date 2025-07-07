# Cold Email Generator Frontend

A modern, responsive web interface for the Cold Email Generator tool. This frontend provides a user-friendly way to generate personalized cold emails based on job listings.

## Features

- **Modern UI**: Clean, professional interface with responsive design
- **Real-time Processing**: Visual feedback during email generation
- **Detailed Results**: View job details, relevant portfolio links, and the generated email
- **Convenient Tools**: Copy email to clipboard or download as text file
- **Mobile-Friendly**: Works on devices of all sizes

## Getting Started

### Running the Application

The easiest way to run both the frontend and backend together is to use the provided run script:

```bash
# From the project root directory
python run.py
```

This will:
1. Start the FastAPI backend on port 8000
2. Serve the frontend on port 8080
3. Open your default browser to http://localhost:8080

### Manual Setup

If you prefer to run the frontend and backend separately:

1. Start the backend API:
   ```bash
   cd project-genai-cold-email-generator
   python app/api.py
   ```

2. Serve the frontend (using any HTTP server):
   ```bash
   cd project-genai-cold-email-generator/frontend
   python -m http.server 8080
   ```

3. Open your browser to http://localhost:8080

## Usage Instructions

1. Select a predefined example URL or choose "Custom URL" to enter your own job listing URL
2. Click "Generate Email" to start the process
3. View the extracted job details and relevant portfolio links
4. Use the generated email in your outreach efforts
5. Optionally, copy the email to your clipboard or download it as a text file

## Technical Details

- Built with HTML5, CSS3, and JavaScript
- Uses Bootstrap 5 for responsive layout and components
- Font Awesome icons for improved visual cues
- Connects to the backend API for email generation logic

## Troubleshooting

- If the frontend cannot connect to the API, ensure the backend is running on port 8000
- For CORS issues, make sure the backend has proper CORS settings enabled
- If job details aren't extracted correctly, try using a different URL with clearer job information

## License

This project is licensed under the MIT License - see the LICENSE file for details. 