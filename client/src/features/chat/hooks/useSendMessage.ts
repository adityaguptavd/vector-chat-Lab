import { useState } from "react";
import { sendMessageApi } from "../api";
import { apiHandler } from "@/services/apiHandler";
import type { ChatMessage } from "../types";
import { Result } from "@/shared/types/result";
import { ApiResponse } from "@/shared/types/api";

export const useSendMessage = () => {
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (
    sessionId: string,
    content: string
  ): Promise<Result<ChatMessage[]>> => {
    setIsLoading(true);

    const { data, error } =
      await apiHandler<ApiResponse<ChatMessage[]>>(
        sendMessageApi(sessionId, content)
      );

    setIsLoading(false);

    if (error) return { success: false, error: error.message };

    if (!data || !data.success) {
      return {
        success: false,
        error: data?.message || "Message failed",
      };
    }

    return {
      success: true,
      data: data.data,
    };
  };

  return {
    sendMessage,
    isLoading,
  };
};