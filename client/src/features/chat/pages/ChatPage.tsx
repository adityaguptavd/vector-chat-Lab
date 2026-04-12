import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";

import { useChatSessions } from "../hooks/useChatSessions";
import { useChatMessages } from "../hooks/useChatMessages";
import { useSendMessage } from "../hooks/useSendMessage";
import { useStreamMode } from "../hooks/useStreamMode";

import { normalizeMessages } from "../utils";

import { useToastContext } from "@/shared/components/Toast/ToastContext";

import { Form } from "@/shared/components/Form/Form";
import { FormField } from "@/shared/components/Form/FormField";
import { Input } from "@/shared/components/Input";

export default function ChatPage() {
  const { sessions, fetchSessions, createSession } = useChatSessions();
  const { messages, setMessages, fetchMessages } = useChatMessages();
  const { sendMessage, streamMessage, isLoading } = useSendMessage();
  const { isStreaming, toggle } = useStreamMode();

  const { showPromise } = useToastContext();

  const [searchParams, setSearchParams] = useSearchParams();

  const initialSessionId = searchParams.get("session");

  const [currentSessionId, setCurrentSessionId] = useState<string | null>(
    initialSessionId,
  );

  // for buffering and throttling
  const bufferRef = useRef("");
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const hasStartedRef = useRef(false);

  // for auto scroll
  const bottomRef = useRef<HTMLDivElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const isAtBottomRef = useRef(true);

  // AI typing rate
  const TIME_FRAME = 30;
  const MAX_TYPED_CHARS = 5;

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

  const appendChunk = (prev: string, chunk: string) => {
    if (!prev) return chunk;

    const lastChar = prev[prev.length - 1];
    const firstChar = chunk[0];

    const needsSpace =
      lastChar !== " " &&
      firstChar !== " " &&
      /[a-zA-Z0-9]/.test(lastChar) &&
      /[a-zA-Z0-9]/.test(firstChar);

    return needsSpace ? prev + " " + chunk : prev + chunk;
  };

  const getNextWordChunk = (buffer: string) => {
    if (!buffer) return "";

    // if buffer small → return all
    if (buffer.length <= MAX_TYPED_CHARS) {
      return buffer;
    }

    // try to find space boundary
    const slice = buffer.slice(0, MAX_TYPED_CHARS);

    const lastSpaceIndex = slice.lastIndexOf(" ");

    if (lastSpaceIndex > 0) {
      return buffer.slice(0, lastSpaceIndex + 1);
    }

    // fallback → take full slice (for long words)
    return slice;
  };

  // ---------------- SEND MESSAGE ----------------

  const handleSend = async (
    values: Record<string, any>,
    { reset }: { reset: () => void },
  ) => {
    const content = values.message?.trim();
    if (!content) return;

    let sessionId = currentSessionId;

    if (!sessionId) {
      const sessionRes = await createSession();
      if (!sessionRes.success || !sessionRes.data) return;

      sessionId = sessionRes.data.id;
      setCurrentSessionId(sessionId);
      await fetchSessions();
    }

    // 🧠 1. Add USER message (optimistic)
    const userTemp = {
      id: "temp-user-" + Date.now(),
      session_id: sessionId!,
      role: "user" as const,
      content,
      created_at: new Date().toISOString(),
    };

    // 🧠 2. Add EMPTY AI message (stream target)
    const aiTempId = "temp-ai-" + Date.now();

    const aiTemp = {
      id: aiTempId,
      session_id: sessionId!,
      role: "assistant" as const,
      content: "",
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userTemp, aiTemp]);
    reset();

    // 3. START CHAT
    if (isStreaming) {
      intervalRef.current = setInterval(() => {
        if (!bufferRef.current) return;

        // delay start until some buffer collected
        if (!hasStartedRef.current && bufferRef.current.length < 20) {
          return;
        }

        hasStartedRef.current = true;

        const nextChunk = getNextWordChunk(bufferRef.current);
        bufferRef.current = bufferRef.current.slice(nextChunk.length);

        setMessages((prev) => {
          let updated = false;

          const next = prev.map((m) => {
            if (m.id !== aiTempId) return m;

            updated = true;

            return {
              ...m,
              content: appendChunk(m.content, nextChunk),
            };
          });

          return updated ? next : prev;
        });
      }, TIME_FRAME);

      // 🔁 STREAMING FLOW
      await streamMessage({
        sessionId,
        content,
        token: localStorage.getItem("access_token")!,

        onChunk: (chunk) => {
          bufferRef.current += chunk;
        },

        onWarning: (warn) => {
          console.warn("Warning:", warn.message);
        },

        onError: (err) => {
          console.error("Error:", err.message);
        },

        onEnd: (data) => {
          if (intervalRef.current) {
            clearInterval(intervalRef.current);
          }

          const newMessages = normalizeMessages(data);

          setMessages((prev) => {
            const filtered = prev.filter(
              (m) => m.id !== userTemp.id && m.id !== aiTempId,
            );

            return [...filtered, ...newMessages];
          });

          bufferRef.current = "";
          hasStartedRef.current = false;
        },
      });
    } else {
      // NON-STREAMING FLOW
      const result = await showPromise(() => sendMessage(sessionId!, content), {
        loading: "Thinking...",
        success: "Response received",
        error: "Failed to send",
      });

      if (result.success && result.data) {
        setMessages((prev) => [
          ...prev.filter((m) => m.id !== userTemp.id && m.id !== aiTempId),
          ...result.data!,
        ]);
      }
    }
  };

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;

    const handleScroll = () => {
      const threshold = 100; // px buffer
      const isAtBottom =
        el.scrollHeight - el.scrollTop - el.clientHeight < threshold;

      isAtBottomRef.current = isAtBottom;
    };

    el.addEventListener("scroll", handleScroll);
    return () => el.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    if (!isAtBottomRef.current) return;

    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, []);

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
      <div className="flex flex-col flex-1 overflow-hidden">
        {/* Messages */}
        <div
          className="flex-1 overflow-y-auto p-4 space-y-2 min-h-0"
          ref={containerRef}
        >
          {messages.map((m) => {
            const isStreamingMessage = m.id.startsWith("temp-ai-");

            return (
              <div key={m.id}>
                <b>{m.role}:</b> {m.content}
                {isStreamingMessage && (
                  <span className="ml-1 inline-block w-[8px] bg-white animate-pulse">
                    &nbsp;
                  </span>
                )}
              </div>
            );
          })}
          <div ref={bottomRef} />
        </div>

        {/* ✅ FORM: SEND MESSAGE */}
        <Form onSubmit={handleSend}>
          <div className="p-4 border-t border-gray-800">
            <div className="flex justify-end mb-2">
              <button
                onClick={toggle}
                type="button"
                className={`text-xs px-3 py-1 rounded transition-all duration-200 ${
                  isStreaming
                    ? "bg-blue-600 text-white shadow-[0_0_10px_rgba(59,130,246,0.5)]"
                    : "bg-gray-800 text-gray-400"
                }`}
              >
                ⚡ Streaming: {isStreaming ? "ON" : "OFF"}
              </button>
            </div>
            <div className="flex gap-2">
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
          </div>
        </Form>
      </div>
    </div>
  );
}
