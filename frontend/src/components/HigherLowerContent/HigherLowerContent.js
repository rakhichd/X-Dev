import { useState } from "react";
import Card from "./Card";

const HigherLowerContent = ({ posts }) => {
  const [current, setCurrent] = useState(0);
  const [offset, setOffset] = useState(0);

  const handleGuess = (direction) => {
    setCurrent((prev) => {
      const newIndex = direction === 'higher' ? prev + 1 : prev - 1;
      if (newIndex >= 0 && newIndex < posts.length) {
        setOffset(newIndex * -50);
        return newIndex;
      }
      return prev;
    });
  };

  return (
    <div className="bg-blue-300 w-full h-full flex overflow-hidden relative">
      <div className="flex transition-transform duration-500" style={{ transform: `translateX(${offset}%)` }}>
        {posts.map((post, idx) => (
          <Card key={idx} text={post.text} likes={post.likes} shown={idx === current} setCurrent={handleGuess} />
        ))}
      </div>
    </div>
  );
};

export default HigherLowerContent;
