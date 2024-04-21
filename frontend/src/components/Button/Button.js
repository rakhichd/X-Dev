export default function Button({ children, className, onClick, style }) {
    return (
        <button className={className} onClick={onClick} style={style}>
            <h1 className="font-bold">{children}</h1>
        </button>
    )
}
