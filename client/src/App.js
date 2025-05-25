import { useState } from 'react';
import './App.css';

function App() {
  const [imageURL, setImageUrl] = useState(null);
  const [inputText, setInputText] = useState('');
  const [fillColor, setFillColor] = useState('#000000'); // default black
  const [bgColor, setBgColor] = useState('#FFFFFF'); // default white

  const handleGenerate = async () => {
    try {
      const response = await fetch('http://localhost:5000/generate', {
        method: 'POST', //SENDING data to server
        headers: {
          'Content-Type': 'application/json', //sending JSON data to server
        },
        body: JSON.stringify({ 
          data: inputText, //convert input to JSON string
          fill_color: fillColor, //convert input to JSON string
          back_color: bgColor //convert input to JSON string
        }), 
      });

      if (!response.ok) {
        // status code is not in the range 200-299
        const errorData = await response.json();
        alert("Error: " + errorData.error);
        return; //stop any further execution
      }
      // response is ok, proceed to get the image

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
      <div>
        <input 
          type="color"
          value={fillColor}
          onChange={(e) => setFillColor(e.target.value)}
          title="Select fill color (QR code Dots)"
        />
        <input
          type="color" 
          value={bgColor}
          onChange={(e) => setBgColor(e.target.value)}
          title="Select background color (QR code Background)"
        />
      </div>
      {imageURL && <img src={imageURL} alt="Generated QR Code" />}
    </>
  );
}

export default App;
