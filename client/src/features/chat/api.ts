import { apiClient } from "@/services/apiClient";
import { ApiResponse } from "@/shared/types/api";
import type { ChatSession, ChatMessage } from "./types";

// ---------------- SESSION ----------------

export const createSessionApi = async (
  title?: string
): Promise<ApiResponse<ChatSession>> => {
  const res = await apiClient.post<ApiResponse<ChatSession>>(
    "/chat/sessions",
    null,
    {
      params: { title },
    }
  );
  return res.data;
};

export const listSessionsApi = async (): Promise<
  ApiResponse<ChatSession[]>
> => {
  const res = await apiClient.get<ApiResponse<ChatSession[]>>(
    "/chat/sessions"
  );
  return res.data;
};

// ---------------- MESSAGE ----------------

export const listMessagesApi = async (
  sessionId: string
): Promise<ApiResponse<ChatMessage[]>> => {
  const res = await apiClient.get<ApiResponse<ChatMessage[]>>(
    `/chat/${sessionId}/messages`
  );
  return res.data;
};

export const sendMessageApi = async (
  sessionId: string,
  content: string
): Promise<ApiResponse<ChatMessage[]>> => {
  const res = await apiClient.post<ApiResponse<ChatMessage[]>>(
    `/chat/${sessionId}/messages`,
    null,
    {
      params: { content },
    }
  );
  return res.data;
};