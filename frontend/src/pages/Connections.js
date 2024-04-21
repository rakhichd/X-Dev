import { AddPeople, Sidebar, ConnectionsTitle, Main } from "../components";
import { useGlobalState } from "../state/state";

export default function Connections() {
  const [showAddPeople] = useGlobalState("showAddPeople");

  return (
    <div>
      {showAddPeople && <AddPeople />}
      <Sidebar />
      <div className="ml-[80px] flex flex-col">
        <ConnectionsTitle />
        <Main />
      </div>
    </div>
  );
}
