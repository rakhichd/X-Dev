import TextInput from "../TextInput/TextInput";
import Button from "../Button/Button";
import { useState } from "react";
import { RxCross1 } from "react-icons/rx";
import { setGlobalState, useGlobalState } from "../../state/state";

export default function AddPeople() {
  const [people] = useGlobalState("people");
  const [form, setForm] = useState("");
  const [start, setStart] = useState("2000");
  const [end, setEnd] = useState("2024");

  const handleChange = (event) => {
    setForm(event.target.value);
  };

  const handleStart = (event) => {
    setStart(event.target.value);
  };

  const handleEnd = (event) => {
    setEnd(event.target.value);
  };

  const handleDone = () => {
    let p;
    if (form.length > 0) {
      p = form.split(",").map((item) => item.trim());
    } else {
      p = [];
    }
    const combined = p.concat(people);
    setGlobalState("people", combined);
    setForm("");
    setGlobalState("showAddPeople", false);
  };

  const UserTag = ({ children }) => {
    return (
      <div
        className="bg-blue-100 flex items-center cursor-pointer rounded-md px-2 relative text-blue-500 hover:bg-red-100 hover:text-red-500 duration-200"
        onClick={() => deletePerson(children)}
      >
        {children}
      </div>
    );
  };

  const deletePerson = (personName) => {
    if (personName !== "everyone") {
      const filteredPeople = people.filter((p) => p !== personName);
      setGlobalState("people", filteredPeople);
    }
  };

  const CloseModal = () => {
    return (
      <div
        className="absolute right-6 cursor-pointer"
        onClick={() => setGlobalState("showAddPeople", false)}
      >
        <RxCross1 />
      </div>
    );
  };

  return (
    <div className="fixed inset-0 z-[999] flex justify-center items-center">
      <div className="absolute inset-0 bg-black opacity-50"></div>
      <div className="relative z-[1000] bg-white rounded-md p-8 shadow-lg w-[500px]">
        <CloseModal />
        <div className="flex items-center mb-2">
          <h1 className="text-left flex-grow text-2xl">Add People</h1>
        </div>
        <TextInput
          value={form}
          onChange={handleChange}
          placeholder="Specify who to pull tweets from..."
        />
        <div className="flex items-center mb-2 mt-2">
          <h1 className="text-left flex-grow text-xl">
            {people.length === 0 ||
            (people.length === 1 && people[0].length == 0) ? (
              <div className="flex gap-1 flex-wrap">
                <h1> Current People:</h1>
                <UserTag id={-1}>everyone</UserTag>
              </div>
            ) : (
              <div className="flex gap-1 flex-wrap">
                <h1> Current People:</h1>
                {people.map((person, index) => (
                  <UserTag key={index} id={index}>
                    {person}
                  </UserTag>
                ))}
              </div>
            )}
          </h1>
        </div>
        <div className="flex items-center gap-3 mt-5">
          <h1 className="text-xl">Time Period:</h1>
          <div className="flex gap-2">

          <TextInput
            value={start}
            onChange={handleStart}
            placeholder="Start Date"
            className="w-28 text-center"
            />
          <TextInput
            value={end}
            onChange={handleEnd}
            placeholder="End Date"
            className="w-28 text-center"
            />
        </div>
            </div>
        <Button
          className="bg-black hover:opacity-80 duration-200 px-5 py-2 mt-3 rounded-md text-white"
          onClick={handleDone}
        >
          Done
        </Button>
      </div>
    </div>
  );
}
