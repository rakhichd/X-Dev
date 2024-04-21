const getHint = async ({ user }) => {
  const result = await fetch("https://6b7f-8-25-197-34.ngrok-free.app/hint", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      hinted_user: user
    }),
    credentials: "include",
  });
  const resultJson = await result.json();
  return { resultJson };
};

export default getHint;
