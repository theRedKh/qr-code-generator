function TextInput({ inputText, setInputText}) {
    return(
        <input
          className="action"
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Enter text here"
        />
    );
}

export default TextInput;