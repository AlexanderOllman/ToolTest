import { useEffect, useState } from "react";
import { socket } from "../lib/socket";

type Event = { taskId: number; status: string; message: string };
export default function TaskLog() {
  const [events, setEvents] = useState<Event[]>([]);
  useEffect(() => {
    socket.on("task_event", (e: Event) => setEvents((p) => [...p, e]));
  }, []);
  return (
    <div className="p-4 space-y-1">
      {events.map((e, i) => (
        <p key={i} className="text-sm font-mono">
          [{e.taskId}] {e.status}: {e.message}
        </p>
      ))}
    </div>
  );
} 