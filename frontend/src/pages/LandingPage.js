import React from "react";
import { BsTwitterX } from "react-icons/bs";
import { PolygonCard } from "react-awesome-shapes/dist/shapes/polygonCard";
import { CircleGrid } from "react-awesome-shapes/dist/shapes/circlegrid";
import { Circle } from "react-awesome-shapes/dist/shapes/circle";
import { Cross } from "react-awesome-shapes/dist/shapes/cross";
import { Donut } from "react-awesome-shapes/dist/shapes/donut";
import { Button } from "../components";
import { signIn } from "../api";
import grid from "../media/grid.png"

export default function LandingPage() {
  const handleClick = async () => {
    const { resultJson } = await signIn();
    const url = resultJson[0].link;
    window.location.href = url
  };

  return (
    <div>
      <div className="absolute left-10 top-10">
        <BsTwitterX size={40} />
      </div>
      <img src={grid} className="absolute top-32 left-[40%] w-[500px] z-[-1]"/>
      <Donut
        color="#f43f5e"
        size="180px"
        width={["40px", "40px", "60px", "60px"]}
        left={[`80px`, `10px`, `10px`, `600px`]}
        top={[`-80px`, `50px`, `50px`, `60px`]}
      />
      <Donut
        color="#f43f5e"
        size="180px"
        width={["40px", "40px", "60px", "60px"]}
        right={[`80px`, `10px`, `10px`, `600px`]}
        bottom={[`-80px`, `50px`, `50px`, `100px`]}
      />
      <Cross
        size="100px"
        zIndex={2}
        color="#0ea5e9"
        left={[`80px`, `10px`, `10px`, `250px`]}
        top={[`-80px`, `50px`, `50px`, `150px`]}
      />
      <CircleGrid
        color="#10b981"
        size="175px"
        zIndex={2}
        left={[`80px`, `10px`, `10px`, `150px`]}
        top={[`-80px`, `50px`, `50px`, `30px`]}
      />
      <CircleGrid
        color="#10b981"
        size="175px"
        zIndex={2}
        left={[`100px`, `10px`, `10px`, `100px`]}
        top={[`-80px`, `80px`, `30px`, `100px`]}
      />
      <Circle
        color="linear-gradient(135deg, #a5b4fc, #6366f1)"
        size="140px"
        zIndex={2}
        left={[`100px`, `10px`, `10px`, `180px`]}
        bottom={[`-80px`, `80px`, `30px`, `30px`]}
      />
      <CircleGrid
        color="#10b981"
        size="175px"
        zIndex={2}
        right={[`100px`, `10px`, `10px`, `100px`]}
        bottom={[`-80px`, `80px`, `30px`, `100px`]}
      />
      <CircleGrid
        color="#10b981"
        size="175px"
        zIndex={2}
        right={[`80px`, `10px`, `10px`, `150px`]}
        bottom={[`-80px`, `50px`, `50px`, `50px`]}
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
        top={[`-80px`, `50px`, `50px`, `10px`]}
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
        <div className="flex items-center gap-2 z-[999]">
          <h1>Sign In With</h1> <BsTwitterX />
        </div>
      </Button>
    </div>
  );
}
