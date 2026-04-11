import { useState } from "react";
import { sendMessageApi, streamMessageApi } from "../api";
import { StreamMessageParams } from "../types";

export const useSendMessage = () => {
  const [isLoading, setIsLoading] = useState(false);

  // ---------------- NORMAL ----------------
  const sendMessage = async (sessionId: string, content: string) => {
    setIsLoading(true);

    try {
      const res = await sendMessageApi(sessionId, content);
      return { success: true, data: res.data };
    } catch (err: any) {
      return { success: false, error: err.message };
    } finally {
      setIsLoading(false);
    }
  };

  // ---------------- STREAM ----------------
  const streamMessage = async (params: StreamMessageParams) => {
    setIsLoading(true);

    try {
      await streamMessageApi(params);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    sendMessage,
    streamMessage,
    isLoading,
  };
};