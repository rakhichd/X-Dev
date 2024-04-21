const signIn = async () => {
  const result = await fetch(
    "https://444e-8-25-197-34.ngrok-free.app",
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include"
    }
  );
  const resultJson = await result.json();
  console.log(resultJson)
  return { resultJson };
};

export default signIn;
