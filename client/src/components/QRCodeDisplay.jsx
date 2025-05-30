import Button from './Button';

function QRCodeDisplay( { imageURL }){
    return (
        imageURL && (
        <div id="qr-code-display">
          <img src={imageURL} alt="Generated QR Code" />
          <Button 
          onClick={() => {
            const link = document.createElement('a');
            link.href = imageURL;
            link.download = 'qr-code.png'; // name of the downloaded file
            link.click(); //trigger the download
          }}
            label="Download"
          />
        </div>
      )
    );
}

export default QRCodeDisplay;