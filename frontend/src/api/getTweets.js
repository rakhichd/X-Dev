const getTweets = async (people, start, end) => {
  const formatDate = (year) => {
    if (year === "2024") {
      return new Date().toISOString();
    } else {
      return `${year}-01-01T00:00:00Z`;
    }
  };

  const result = await fetch("http://127.0.0.1:5000/generate_game", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
        custom_users: people,
        start_time: formatDate(start),
        end_time: formatDate(end)
    })
  });
  const resultJson = await result.json();
  const resultStatus = result.status;

  console.log(resultJson)

  return { resultJson, resultStatus };
};

export default getTweets;
