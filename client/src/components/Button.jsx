function Button({ onClick, label }){
    return(
        <button className="actionBtn" onClick={onClick}>{label}</button>
    );
}

export default Button;