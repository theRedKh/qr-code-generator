function TextInput({ inputText, setInputText}) {
    return(
        <input 
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Enter text here"
        />
    );
}

export default TextInput;