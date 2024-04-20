export default function Button({children, className}) {
    return (
        <button className = {className}>
            <h1 className = "font-bold">{children}</h1>
        </button>
    )
}
