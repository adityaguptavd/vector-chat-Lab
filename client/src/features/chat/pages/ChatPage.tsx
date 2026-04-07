import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import { useChatSessions } from "../hooks/useChatSessions";
import { useChatMessages } from "../hooks/useChatMessages";
import { useSendMessage } from "../hooks/useSendMessage";
import { useToastContext } from "@/shared/components/Toast/ToastContext";

import { Form } from "@/shared/components/Form/Form";
import { FormField } from "@/shared/components/Form/FormField";
import { Input } from "@/shared/components/Input";

export default function ChatPage() {
  const { sessions, fetchSessions, createSession } = useChatSessions();
  const { messages, setMessages, fetchMessages } = useChatMessages();
  const { sendMessage, isLoading } = useSendMessage();

  const { showPromise } = useToastContext();

  const [searchParams, setSearchParams] = useSearchParams();

  const initialSessionId = searchParams.get("session");

  const [currentSessionId, setCurrentSessionId] = useState<string | null>(
    initialSessionId,
  );

  useEffect(() => {
    fetchSessions();
  }, []);

  useEffect(() => {
    if (!currentSessionId) {
      setSearchParams({});
    } else if (currentSessionId) {
      fetchMessages(currentSessionId);
      setSearchParams({ session: currentSessionId });
    }
  }, [currentSessionId]);

  // ---------------- CREATE SESSION ----------------

  const handleCreateSession = async (
    values: Record<string, any>,
    { reset }: { reset: () => void },
  ) => {
    const title = values.title;

    const res = await showPromise(() => createSession(title || undefined), {
      loading: "Creating chat...",
      success: "Chat created",
      error: "Failed to create chat",
    });

    if (res.success && res.data) {
      reset();
      setCurrentSessionId(res.data.id);
      await fetchSessions();
    }
  };

  // ---------------- SEND MESSAGE ----------------

  const handleSend = async (
    values: Record<string, any>,
    { reset }: { reset: () => void },
  ) => {
    const content = values.message?.trim();
    if (!content) return;

    let sessionId = currentSessionId;

    // 🧠 lazy session creation
    if (!sessionId) {
      const sessionRes = await createSession();
      if (!sessionRes.success || !sessionRes.data) return;

      sessionId = sessionRes.data.id;
      setCurrentSessionId(sessionId);
      await fetchSessions();
    }

    const tempMessage = {
      id: "temp-" + Date.now(),
      session_id: sessionId!,
      role: "user" as const,
      content,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, tempMessage]);
    reset();

    const result = await showPromise(() => sendMessage(sessionId!, content), {
      loading: "Thinking...",
      success: "Response received",
      error: "Failed to send",
    });

    if (result.success && result.data) {
      setMessages((prev) => [
        ...prev.filter((m) => m.id !== tempMessage.id),
        ...result.data!,
      ]);
    }
  };

  return (
    <div className="flex h-screen bg-gray-950 text-white">
      {/* Sidebar */}
      <div className="w-64 border-r border-gray-800 p-4">
        {/* ✅ FORM: CREATE SESSION */}
        <Form onSubmit={handleCreateSession}>
          <div className="mb-4 space-y-2">
            <FormField name="title">
              <Input
                type="text"
                placeholder="Chat title (optional)"
                className="w-full p-2 rounded bg-gray-800 outline-none"
              />
            </FormField>

            <button type="submit" className="w-full bg-blue-600 p-2 rounded">
              New Chat
            </button>
          </div>
        </Form>

        {sessions.map((s) => {
          const isActive = s.id === currentSessionId;

          return (
            <div
              key={s.id}
              onClick={() => setCurrentSessionId(s.id)}
              className={`cursor-pointer p-2 rounded flex items-center gap-2 transition-all duration-200 ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "hover:bg-gray-800 text-gray-300"
              }`}
            >
              <div
                className={`w-1 h-5 rounded ${
                  isActive ? "bg-white" : "bg-transparent"
                }`}
              />
              <span className="truncate">{s.title || "Untitled"}</span>
            </div>
          );
        })}
      </div>

      {/* Chat */}
      <div className="flex flex-col flex-1">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          {messages.map((m) => (
            <div key={m.id}>
              <b>{m.role}:</b> {m.content}
            </div>
          ))}
        </div>

        {/* ✅ FORM: SEND MESSAGE */}
        <Form onSubmit={handleSend}>
          <div className="p-4 border-t border-gray-800 flex gap-2">
            <div className="grow">
              <FormField
                name="message"
                // rules={{ required: "Message cannot be empty" }}
                rules={{ required: "" }}
              >
                <Input
                  type="text"
                  placeholder="Type a message..."
                  className="flex-1 p-2 bg-gray-800 rounded outline-none"
                />
              </FormField>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="bg-blue-600 px-4 rounded"
            >
              Send
            </button>
          </div>
        </Form>
      </div>
    </div>
  );
}
