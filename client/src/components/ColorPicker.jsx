function ColorPicker({ label, color, onChange, title }){
    return(
        <div className="color-container">
            <input
            className="color-picker"
            type="color"
            value={color}
            onChange={(e) => onChange(e.target.value)}
            title={title}
            />
            <label>{label}</label>
        </div>
    );
}

export default ColorPicker;