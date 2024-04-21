import { useEffect, useState } from "react";

const useDimensions = () => {
    const [width, setWidth] = useState(() => {
        if (typeof window !== 'undefined') {
            return window.innerWidth
        }
    });
    const [height, setHeight] = useState(() => {
        if (typeof window !== 'undefined') {
            return window.innerHeight
        }
    });

    const updateDimensions = () => {
        setWidth(window.innerWidth);
        setHeight(window.innerHeight);
    }

    useEffect(() => {
        window.addEventListener("resize", updateDimensions);
        return () => window.removeEventListener("resize", updateDimensions);
    }, []);

    return { width, height }
}

export default useDimensions;