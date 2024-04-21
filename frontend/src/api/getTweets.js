const getTweets = async (people, start, end) => {
    console.log(people, start, end)
  const formatDate = (year) => {
    if (year === "2024") {
        const now = new Date();
        now.setMinutes(now.getMinutes() - 10);
        return now.toISOString();
    } else {
      return `${year}-01-01T00:00:00Z`;
    }
  };

  const result = await fetch("https://444e-8-25-197-34.ngrok-free.app/generate_game", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
        custom_users: people,
        start_time: formatDate(start),
        end_time: formatDate(end)
    }),
    credentials: "include"
  });
  const resultJson = await result.json();
  const resultStatus = result.status;

  console.log(resultJson)

  return { resultJson, resultStatus };
};

export default getTweets;
