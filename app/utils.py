import re

def clean_text(text):
    # Remove script and style elements
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
    
    # Replace various HTML elements with readable format
    text = re.sub(r'</?h[1-6][^>]*>', '\n\n', text)  # Headers become line breaks
    text = re.sub(r'</?p[^>]*>', '\n', text)  # Paragraphs become line breaks
    text = re.sub(r'<br[^>]*>', '\n', text)  # Line breaks preserved
    text = re.sub(r'<li[^>]*>', '\n• ', text)  # List items become bullets
    text = re.sub(r'<tr[^>]*>', '\n', text)  # Table rows become line breaks
    text = re.sub(r'<\/td>', ' | ', text)  # Table cells separated by pipe
    
    # Remove remaining HTML tags but preserve the content
    text = re.sub(r'<[^>]*?>', ' ', text)
    
    # Fix bullet points for consistency
    text = re.sub(r'\*\s+', '• ', text)
    
    # Replace common HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&apos;', "'")
    
    # Convert multiple whitespace to single space
    text = re.sub(r'\s+', ' ', text)
    
    # Restore line breaks
    text = text.replace(' \n ', '\n')
    text = text.replace(' \n', '\n')
    text = text.replace('\n ', '\n')
    
    # Remove multiple line breaks
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Trim leading and trailing whitespace
    text = text.strip()
    
    return text