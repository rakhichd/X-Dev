const getHint = async ({ user }) => {
  const result = await fetch("https://444e-8-25-197-34.ngrok-free.app/hint", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      hinted_user: user
    }),
  });
  const resultJson = await result.json();
  return { resultJson };
};

export default getHint;
