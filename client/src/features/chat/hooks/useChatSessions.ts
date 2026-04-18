import { useState } from "react";
import { apiHandler } from "@/services/apiHandler";
import type { ChatSession, SessionView } from "../types";
import { Result } from "@/shared/types/result";
import { ApiResponse } from "@/shared/types/api";
import {
  listSessionsApi,
  createSessionApi,
  archiveSessionApi,
  unarchiveSessionApi,
  listArchivedSessionsApi,
} from "../api";

export const useChatSessions = () => {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchSessions = async (
    viewType: SessionView = "active",
  ): Promise<Result<ChatSession[]>> => {
    setIsLoading(true);

    const apiCall =
      viewType === "archived" ? listArchivedSessionsApi() : listSessionsApi();

    const { data, error } =
      await apiHandler<ApiResponse<ChatSession[]>>(apiCall);

    setIsLoading(false);

    if (error) return { success: false, error: error.message };

    setSessions(data?.data || []);

    return { success: true, data: data?.data || [] };
  };

  const createSession = async (
    title?: string,
  ): Promise<Result<ChatSession>> => {
    setIsLoading(true);

    const { data, error } = await apiHandler<ApiResponse<ChatSession>>(
      createSessionApi(title),
    );

    setIsLoading(false);

    if (error) return { success: false, error: error.message };

    if (data?.data) {
      setSessions((prev) => [data.data, ...prev]);
      return { success: true, data: data.data };
    }

    return { success: false, error: "Failed to create session" };
  };

  const archiveSession = async (
    sessionId: string,
  ): Promise<Result<ChatSession>> => {
    const { data, error } = await apiHandler<ApiResponse<ChatSession>>(
      archiveSessionApi(sessionId),
    );

    if (error) return { success: false, error: error.message };

    if (data?.data) {
      setSessions((prev) =>
        prev.map((s) => (s.id === sessionId ? { ...s, is_archived: true } : s)),
      );

      return { success: true, data: data.data };
    }

    return { success: false, error: "Failed to archive session" };
  };

  const unarchiveSession = async (
    sessionId: string,
  ): Promise<Result<ChatSession>> => {
    const { data, error } = await apiHandler<ApiResponse<ChatSession>>(
      unarchiveSessionApi(sessionId),
    );

    if (error) return { success: false, error: error.message };

    if (data?.data) {
      setSessions((prev) =>
        prev.map((s) =>
          s.id === sessionId ? { ...s, is_archived: false } : s,
        ),
      );

      return { success: true, data: data.data };
    }

    return { success: false, error: "Failed to unarchive session" };
  };

  return {
    sessions,
    isLoading,
    fetchSessions,
    createSession,
    archiveSession,
    unarchiveSession,
  };
};
