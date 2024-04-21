const getHighLow = async () => {
  const result = await fetch("https://6b7f-8-25-197-34.ngrok-free.app/generate_higherlower", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
  });
  const resultJson = await result.json();
  return { resultJson };
};

export default getHighLow;
