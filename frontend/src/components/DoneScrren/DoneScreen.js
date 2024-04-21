import React from "react"
import Button from "../Button/Button"

export default function DoneScreen({status}) {

    const userName = "@bob"

    return (
        <div>
            {status === "win" ? <> 
            <div className="flex justify-center">
                    <div className="bg-pink-200 box-content h-32 w-32 p-4 mt-8 flex items-center">
                        <div>
                            congrats {userName}, you won!
                        </div>
                    </div>
                </div>
                    
            </>: 

                <Button
                style={{
                    transition: "transform 0.2s, box-shadow 0.3s",
                    boxShadow: "0 0 10px rgba(0, 0, 255, 0.7)",
                }}
                className={`py-3 px-1 rounded-lg h-20 w-13 max-w-md bg-blue-100 transform hover:rotate-3`}
                >
                </Button>


                // <div className="relative h-screen">
                //     Sorry {userName}, you lost!
                //     <div className="bg-pink-200 box-content h-32 w-32 p-4 mt-8 absolute animate-bounce">
                //         <Button className="flex items-center justify-center h-full">
                //             Try Again!
                //         </Button>
                //     </div>
                // </div>
            
            }
        </div>
    )

}

