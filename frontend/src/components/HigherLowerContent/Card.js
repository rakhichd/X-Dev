import Button from "../Button/Button";

export default function Card({ text, likes, shown, handleHigher, handleLower }) {
  return (
    <div className="flex-shrink-0 w-1/2 h-full flex items-center justify-center">
      {shown ? (
        <div className="flex flex-col items-center justify-center h-full w-3/4">
          <h1 className="text-center font-semibold text-2xl">{text}</h1>
          <h1 className="text-center text-xl">has</h1>
          <h1 className="text-center font-bold text-4xl flex gap-2">
            <span>{likes}</span><span>Likes</span>
          </h1>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center h-full w-3/4 gap-3">
          <h1 className="text-center font-semibold text-2xl">{text}</h1>
          <Button
            className="bg-gray-200 w-80 py-2 hover:opacity-80 cursor-pointer rounded-md z-[999]"
            onClick={handleHigher}
          >
            Higher
          </Button>
          <Button
            className="bg-gray-200 w-80 py-2 hover:opacity-80 cursor-pointer rounded-md z-[999]"
            onClick={handleLower}
          >
            Lower
          </Button>
        </div>
      )}
    </div>
  );
}
