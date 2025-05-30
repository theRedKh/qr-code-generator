import { useState } from 'react';
import './App.css';
import Header from './components/Header';
import TextInput from './components/TextInput';
import ColorPicker from './components/ColorPicker';
import QRCodeDisplay from './components/QRCodeDisplay';
import Button from './components/Button';

function App() {
  const [imageURL, setImageUrl] = useState(null);
  const [inputText, setInputText] = useState('');
  const [fillColor, setFillColor] = useState('#000000'); // default black
  const [bgColor, setBgColor] = useState('#FFFFFF'); // default white
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true); //set loading to true
    try {
      const response = await fetch('simple-qr-code-generator-atg4f7agc7gbb5en.canadacentral-01.azurewebsites.net/generate', {
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
    finally {
      setLoading(false); //set loading to false
    }
  };

  return (
    <>
      <Header/>
      <div className="mainInputContainer">
        <div className='inputContainer1'>
          <TextInput
            inputText={inputText}
            setInputText={setInputText}
          />
          {loading ? (
            <div className='spinner'></div>
          ) : (
            <Button onClick={handleGenerate} label="Generate"/>
          )}
        </div>
        <div className='inputContainer2'>
          <ColorPicker
            label="Fill"
            color={fillColor}
            onChange={setFillColor} 
            title="Select fill color (QR code Dots)"
            />
            <ColorPicker
              label="Background"
              color={bgColor}
              onChange={setBgColor}
              title="Select background color (QR code Background)"
            />
        </div>
        <QRCodeDisplay imageURL={imageURL}/>
      </div>
    </>
  );
}

export default App;
