import React, { useState, useEffect }  from "react"
import Button from "../Button/Button" 

export default function StartPage({handleStartGame}) {

    const [gameStarted, setGameStarted] = useState(false);

    const handleGame = () => {
        setGameStarted(true);
        // Add any additional logic to start the game here
    };

    return (
        <div className="container mx-auto px-4 py-8">
            {!gameStarted ? (
                <div>
                    <Button className={"active:bg-blue-300 border border-opacity-100 px-6 py-2 rounded-full border-black"} onClick={handleGame}>Start Game</Button>
                </div>
            ) : (
                <div>
                    <p>Game is starting...</p>
                </div>
            )}
        </div>
    );

}