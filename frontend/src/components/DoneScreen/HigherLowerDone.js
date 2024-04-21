import React, { useState, useEffect } from "react";
import Button from "../Button/Button";
import { FaRetweet } from "react-icons/fa6";

import interactTweet from "../../api/interactTweet";
import Heart from "./Heart.js";
import Following from "./Following.js";

export default function HigherLowerDone({ posts, won, score }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const handleInteract = async (interact_type, tweet_id, author_id) => {
    const { resultJson } = await interactTweet(
      interact_type,
      tweet_id,
      author_id
    );
  };

  console.log(posts[0].author_id);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-4 w-full">
        <h2 className="text-2xl font-bold flex justify-center items-center w-full">
          <img
            src={posts[0].profile_image}
            alt={"0"}
            className="rounded-full h-20 w-20 mr-5"
          />
          {posts[0].user}
          <div onClick={() => handleInteract(0, 0, posts[0].author_id)}>
            <Following></Following>
          </div>
        </h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {posts.map((post, idx) => (
          <div key={idx} className="bg-blue-100 p-4 rounded-lg shadow relative pb-8">
            <p className="font-semibold">{post.text}</p>
            <div className="absolute flex items-end justify-center gap-3 bottom-1 w-[90%]">
              <Button
                onClick={() => handleInteract(2, post.id, 0)}
                className="rounded-full p-1 hover:bg-green-100"
              >
                <FaRetweet />
              </Button>
              <p className="text-gray-500 text-sm mt-2 rounded-full p-1 hover:bg-transparent">
                @{posts[0].user}
              </p>
              <div onClick={() => handleInteract(1, post.id, 0)}>
                <Heart />
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-10 flex items-center justify-center">
        <div className="animate-pulse text-red-800 text-4xl font-extrabold">
          {won && "You Win!"}
          {!won && (
            <>
              <h1>Score: {score}</h1> <h1>You Lose...</h1>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
