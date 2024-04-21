const getTweets = async () => {
  const result = await fetch(
    "https://e2d3-8-25-197-34.ngrok-free.app/authenticate",
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    }
  );
  const resultJson = await result.json();
  const resultStatus = result.staus;

  return { resultJson };
};

export default getTweets;
