export default function Button({ children, className, onClick }) {
    return (
        <button className={className} onClick={onClick}>
            <h1 className="font-bold">{children}</h1>
        </button>
    )
}
