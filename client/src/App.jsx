import { useState } from 'react';
import './App.css';
import ReactMarkdown from 'react-markdown';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

function App() {
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [promptType, setPromptType] = useState('general');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [markdownContent, setMarkdownContent] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    setMarkdownContent(''); // Clear previous content

    try {
      const response = await fetch('http://localhost:8000/generate_worksheet/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ youtube_url: youtubeUrl, prompt_type: promptType }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate worksheet.');
      }

      const text = await response.text();
      setMarkdownContent(text);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPdf = async () => {
    const element = document.getElementById('markdown-content');
    if (!element) {
      console.error("Element with id 'markdown-content' not found");
      return;
    }

    const canvas = await html2canvas(element, { scale: 2 }); // Adjust scale for better resolution
    const data = canvas.toDataURL('image/jpeg', 0.8); // Use JPEG with quality 0.8

    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4',
    });

    const imgWidth = 210; // A4 width in mm
    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    let heightLeft = imgHeight;
    let position = 0;

    pdf.addImage(data, 'JPEG', 0, position, imgWidth, imgHeight, '', 'FAST'); // Compress
    heightLeft -= 297; // A4 height in mm

    while (heightLeft >= 0) {
      position = heightLeft - imgHeight;
      pdf.addPage();
      pdf.addImage(data, 'JPEG', 0, position, imgWidth, imgHeight, '', 'FAST');
      heightLeft -= 297;
    }

    pdf.save('worksheet.pdf');
  };

  return (
    <>
      <div>
        <h1>YouTube Worksheet Generator</h1>
        <form onSubmit={handleSubmit}>
          <label htmlFor="youtube_url">YouTube URL:</label><br />
          <input
            type="text"
            id="youtube_url"
            name="youtube_url"
            value={youtubeUrl}
            onChange={(e) => setYoutubeUrl(e.target.value)}
            required
          /><br /><br />

          <label>Prompt Type:</label><br />
          <input
            type="radio"
            id="general"
            name="prompt_type"
            value="general"
            checked={promptType === 'general'}
            onChange={(e) => setPromptType(e.target.value)}
          />
          <label htmlFor="general">General</label><br />

          <input
            type="radio"
            id="age"
            name="prompt_type"
            value="age"
            checked={promptType === 'age'}
            onChange={(e) => setPromptType(e.target.value)}
          />
          <label htmlFor="age">Age of Empires</label><br /><br />

          <button type="submit" disabled={loading}>
            {loading ? 'Generating...' : 'Generate Worksheet'}
          </button>
        </form>
        {error && <p style={{ color: 'red' }}>Error: {error}</p>}

        {markdownContent && (
          <>
            <div
              id="markdown-content"
              style={{
                textAlign: 'left',
                backgroundColor: 'white',
                color: 'black',
                border: '1px solid #ccc',
                padding: '20px',
                maxWidth: '800px',
                margin: '0 auto',
              }}
            >
              <h2>Worksheet:</h2>
              <ReactMarkdown className="markdown-body">{markdownContent}</ReactMarkdown>
            </div>
            <button onClick={handleDownloadPdf}>Download PDF</button>
          </>
        )}
      </div>
    </>
  );
}

export default App;
