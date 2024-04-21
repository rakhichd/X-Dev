import Button from "../Button/Button";

export default function Card({ text, likes, shown, setCurrent }) {
  return (
    <div className="flex-grow-0 flex-shrink-0 w-1/2 h-full bg-blue-300">
      {shown ? (
        <div className="flex flex-col items-center justify-center h-full">
          <h1 className="text-center font-semibold text-5xl mb-5">{text}</h1>
          <h1 className="text-center text-3xl mb-5">has</h1>
          <h1 className="text-center text-5xl font-bold">{likes}</h1>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center h-full">
          <h1 className="text-center font-semibold text-5xl mb-8">{text}</h1>
          <Button
            className="bg-gray-200 w-80 py-2 hover:opacity-80 cursor-pointer rounded-full z-[999] mb-5"
            onClick={() => setCurrent((prev) => prev + 1)}
          >
            Higher
          </Button>
          <Button
            className="bg-gray-200 w-80 py-2 hover:opacity-80 cursor-pointer rounded-full z-[999]"
            onClick={() => setCurrent((prev) => prev - 1)}
          >
            Lower
          </Button>
        </div>
      )}
    </div>
  );
}
