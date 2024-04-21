const signIn = async () => {
  const result = await fetch(
    "https://6b7f-8-25-197-34.ngrok-free.app/authenticate",
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
