function ColorPicker({ label, color, onChange, title }){
    return(
        <div>
            <label>{label}</label>
            <input 
            type="color"
            value={color}
            onChange={(e) => onChange(e.target.value)}
            title={title}
            />
        </div>
    );
}

export default ColorPicker;