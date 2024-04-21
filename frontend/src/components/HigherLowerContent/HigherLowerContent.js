import { useState } from "react";
import Card from "./Card";
import useDimensions from "../../hooks/useDimensions";

const HigherLowerContent = ({ posts, setDone, setScore, score }) => {
  const [current, setCurrent] = useState(1);
  const [offset, setOffset] = useState(0);
  const { width } = useDimensions();

  const handleLower = () => {
    if (posts[current].likes < posts[current - 1].likes) {
      const s = score + 1
      setScore((prev) => prev + 1);
      console.log(s)
      if (s == posts.length - 1) {
        setCurrent((prev) => prev + 1);
        setTimeout(function() {
          setDone(true)
        }, 1000);
      } else {
        setOffset((prev) => prev + (width - 80) / 2);
        setCurrent((prev) => prev + 1);
      }
    } else {
      setCurrent((prev) => prev + 1)
      setTimeout(function() {
        setDone(true)
      }, 1000);
    }
  };

  const handleHigher = () => {
    if (posts[current].likes > posts[current - 1].likes) {
      const s = score + 1
      setScore((prev) => prev + 1);
      if (s == posts.length - 1) {
        setCurrent((prev) => prev + 1);
        setTimeout(function() {
          setDone(true)
        }, 1000);
      } else {
        setOffset((prev) => prev + (width - 80) / 2);
        setCurrent((prev) => prev + 1);
      }
    } else {
      setCurrent((prev) => prev + 1)
      setTimeout(function() {
        setDone(true)
      }, 1000);
    }
  };

  return (
    <div className="h-full overflow-hidden" style={{ width: width - 80 }}>
      <div
        className={`flex h-full transition-transform duration-500`}
        style={{ transform: `translateX(-${offset}px)` }}
      >
        {posts.map((post, idx) => (
          <Card
            key={idx}
            text={post.text}
            likes={post.likes}
            shown={idx < current}
            handleHigher={handleHigher}
            handleLower={handleLower}
          />
        ))}
      </div>
    </div>
  );
};

export default HigherLowerContent;
