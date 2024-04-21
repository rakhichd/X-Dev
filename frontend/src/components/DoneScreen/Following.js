import Button from "../Button/Button";
import { IoMdHeartEmpty } from "react-icons/io";
import { IoMdHeart } from "react-icons/io";
import { useState } from "react";

export default function Following() {
    const [follow, setFollow] = useState(false);
    return (
        <Button onClick={() => {
            setFollow(true);
        }}
            className="hover:bg-gray-800 border border-opacity-100 px-3 py-1 rounded-full border-black bg-black text-white text-sm ml-4"
        >
            {follow ? 'Following' : 'Follow'}
        </Button>

    )
}