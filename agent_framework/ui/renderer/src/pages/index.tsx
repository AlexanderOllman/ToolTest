import { useState } from "react";
import TaskLog from "../components/TaskLog";
import SettingsModal from "../components/SettingsModal";
import { getEndpoint } from "../lib/config";

export default function Home() {
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  const send = () => {
    const taskExecutorUrl = getEndpoint("taskExecutor");
    fetch(`${taskExecutorUrl}/run_query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
  };
  return (
    <div className="p-6 space-y-4">
      <h1 className="text-xl font-bold">Agent Framework</h1>
      <textarea value={query} onChange={(e) => setQuery(e.target.value)} className="border w-full p-2" rows={3} />
      <div className="space-x-2">
        <button onClick={send} className="bg-green-500 text-white px-3 py-1 rounded">Run</button>
        <button onClick={() => setOpen(true)} className="bg-gray-500 text-white px-3 py-1 rounded">Settings</button>
      </div>
      <TaskLog />
      <SettingsModal open={open} onClose={() => setOpen(false)} />
    </div>
  );
} 