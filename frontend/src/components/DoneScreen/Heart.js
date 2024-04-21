import Button from "../Button/Button";
import { IoMdHeartEmpty } from "react-icons/io";
import { IoMdHeart } from "react-icons/io";
import { useState } from "react";

export default function Heart() {
    const [heart, setHeart] = useState(false);
    return (
        <Button onClick={() => {
            setHeart(true);
        }}
            className="rounded-full p-1 hover:text-red-800"
        >
            {heart ? <IoMdHeart className="text-red-600"></IoMdHeart> : <IoMdHeartEmpty />}
        </Button>

    )
}