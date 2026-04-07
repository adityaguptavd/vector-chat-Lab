import { useState } from "react";
import { listMessagesApi } from "../api";
import { apiHandler } from "@/services/apiHandler";
import type { ChatMessage } from "../types";
import { Result } from "@/shared/types/result";
import { ApiResponse } from "@/shared/types/api";

export const useChatMessages = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchMessages = async (
    sessionId: string
  ): Promise<Result<ChatMessage[]>> => {
    setIsLoading(true);

    const { data, error } =
      await apiHandler<ApiResponse<ChatMessage[]>>(
        listMessagesApi(sessionId)
      );

    setIsLoading(false);

    if (error) return { success: false, error: error.message };

    const msgs = data?.data || [];
    setMessages(msgs);

    return { success: true, data: msgs };
  };

  return {
    messages,
    setMessages,
    isLoading,
    fetchMessages,
  };
};