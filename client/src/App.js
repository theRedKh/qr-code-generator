import { useState } from 'react';
import './App.css';

function App() {
  const [imageURL, setImageUrl] = useState(null);
  const [inputText, setInputText] = useState('');
  const handleGenerate = async () => {
    try {
      const response = await fetch('http://localhost:5000/generate', {
        method: 'POST', //SENDING data to server
        headers: {
          'Content-Type': 'application/json', //sending JSON data to server
        },
        body: JSON.stringify({ text: inputText }), //convert input to JSON string
      });

      const blob = await response.blob(); //convert raw data to Binary Large Object
      const url = window.URL.createObjectURL(blob); //temp URL for image blob
      setImageUrl(url);
    }
    catch (error) {
      console.error('Error generating QR code:', error);      
    }
  };
  return (
    <>
      <div>
        <h1>Hello from QR Code Generator</h1>
        <p>Type your text in the field, and click Generate to watch the magic happen</p>
      </div>
      <div>
        <input 
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Enter text here" 
        />
        <button onClick={handleGenerate}>Generate</button>
      </div>
      {imageURL && <img src={imageURL} alt="Generated QR Code" />}
    </>
  );
}

export default App;
