export default function Button({name, className}) {
    return (
        <button className = {className}>
            <h1 className = "font-bold">{name}</h1>
        </button>
    )
}
