import { useEffect, useState } from "react";

const STORAGE_KEY = "chat_stream_mode";

export const useStreamMode = () => {
  const [isStreaming, setIsStreaming] = useState(true);

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved !== null) {
      setIsStreaming(saved === "true");
    }
  }, []);

  const toggle = () => {
    setIsStreaming((prev) => {
      const next = !prev;
      localStorage.setItem(STORAGE_KEY, String(next));
      return next;
    });
  };

  return { isStreaming, toggle };
};