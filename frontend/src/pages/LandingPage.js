import React from "react";
import { BsTwitterX } from "react-icons/bs";
import { PolygonCard } from "react-awesome-shapes/dist/shapes/polygonCard";
import { CircleGrid } from "react-awesome-shapes/dist/shapes/circlegrid";
import { Circle } from "react-awesome-shapes/dist/shapes/circle";
import { Button } from "../components";
import signIn from "../api/signIn";

export default function LandingPage() {
  const handleClick = async () => {
    const { resultJson } = await signIn();
    console.log(resultJson[0].link)
    const url = resultJson[0].link
    window.location.href = url;
  };

  return (
    <div>
      <div className="absolute left-10 top-10">
        <BsTwitterX size={40} />
      </div>
      <CircleGrid
        color="#10b981"
        size="175px"
        zIndex={2}
        left={[`80px`, `10px`, `10px`, `150px`]}
        top={[`-80px`, `50px`, `50px`, `50px`]}
      />
      <CircleGrid
        color="#10b981"
        size="175px"
        zIndex={2}
        left={[`100px`, `10px`, `10px`, `100px`]}
        top={[`-80px`, `80px`, `30px`, `100px`]}
      />
      <Circle
        color="#f9f9f9"
        size="40px"
        zIndex={2}
        right={[`100px`, `10px`, `10px`, `320px`]}
        top={[`-80px`, `50px`, `50px`, `60px`]}
      />
      <PolygonCard
        height="200px"
        width="300px"
        zIndex={1}
        color="linear-gradient(135deg, #f9a8d4, #ec4899)"
        right={[`80px`, `10px`, `10px`, `200px`]}
        top={[`-80px`, `50px`, `50px`, `50px`]}
      />
      <Button
        className="hover:opacity-[80%]"
        style={{
          position: "fixed",
          top: "80%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          padding: "15px 30px",
          backgroundColor: "black",
          color: "white",
          borderRadius: "8px",
          transition: "opacity 0.2s ease",
        }}
        onClick={handleClick}
      >
        <div className="flex items-center gap-2">
          <h1>Sign In With</h1> <BsTwitterX />
        </div>
      </Button>
    </div>
  );
}
