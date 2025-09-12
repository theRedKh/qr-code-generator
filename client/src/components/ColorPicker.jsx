function ColorPicker({ label, color, onChange, title, disabled }){
    return(
        <div className="color-container">
            <input
            className="color-picker"
            type="color"
            value={color}
            onChange={(e) => onChange(e.target.value)}
            title={title}
            disabled={disabled}
            />
            <label>{label}</label>
        </div>
    );
}

export default ColorPicker;