import { useState } from "react";
import { listSessionsApi, createSessionApi } from "../api";
import { apiHandler } from "@/services/apiHandler";
import type { ChatSession } from "../types";
import { Result } from "@/shared/types/result";
import { ApiResponse } from "@/shared/types/api";

export const useChatSessions = () => {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchSessions = async (): Promise<Result<ChatSession[]>> => {
    setIsLoading(true);

    const { data, error } =
      await apiHandler<ApiResponse<ChatSession[]>>(listSessionsApi());

    setIsLoading(false);

    if (error) return { success: false, error: error.message };

    setSessions(data?.data || []);
    return { success: true, data: data?.data || [] };
  };

  const createSession = async (
    title?: string
  ): Promise<Result<ChatSession>> => {
    setIsLoading(true);

    const { data, error } =
      await apiHandler<ApiResponse<ChatSession>>(
        createSessionApi(title)
      );

    setIsLoading(false);

    if (error) return { success: false, error: error.message };

    if (data?.data) {
      setSessions((prev) => [data.data, ...prev]);
      return { success: true, data: data.data };
    }

    return { success: false, error: "Failed to create session" };
  };

  return {
    sessions,
    isLoading,
    fetchSessions,
    createSession,
  };
};