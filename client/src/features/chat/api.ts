import { apiClient } from "@/services/apiClient";
import { ApiResponse } from "@/shared/types/api";
import type { ChatSession, ChatMessage, StreamMessageParams } from "./types";
import { safeParse } from "@/shared/utils/json-parser";
import { emitSessionExpired } from "@/shared/events/authEvents";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

// ---------------- SESSION ----------------

export const createSessionApi = async (
  title?: string,
): Promise<ApiResponse<ChatSession>> => {
  const res = await apiClient.post<ApiResponse<ChatSession>>(
    "/chat/sessions",
    null,
    {
      params: { title },
    },
  );
  return res.data;
};

export const listSessionsApi = async (): Promise<
  ApiResponse<ChatSession[]>
> => {
  const res = await apiClient.get<ApiResponse<ChatSession[]>>("/chat/sessions");
  return res.data;
};

export const listArchivedSessionsApi = async (): Promise<
  ApiResponse<ChatSession[]>
> => {
  const res = await apiClient.get<ApiResponse<ChatSession[]>>(
    "/chat/sessions/archived"
  );
  return res.data;
};

// ---------------- MESSAGE ----------------

export const listMessagesApi = async (
  sessionId: string,
): Promise<ApiResponse<ChatMessage[]>> => {
  const res = await apiClient.get<ApiResponse<ChatMessage[]>>(
    `/chat/${sessionId}/messages`,
  );
  return res.data;
};

export const sendMessageApi = async (
  sessionId: string,
  content: string,
): Promise<ApiResponse<ChatMessage[]>> => {
  const res = await apiClient.post<ApiResponse<ChatMessage[]>>(
    `/chat/${sessionId}/messages`,
    null,
    {
      params: { content },
    },
  );
  return res.data;
};

export const streamMessageApi = async ({
  sessionId,
  content,
  token,
  onChunk,
  onEnd,
  onError,
  onWarning,
}: StreamMessageParams) => {
  const res = await fetch(`${BASE_URL}/chat/${sessionId}/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ content }),
  });

  if (res.status === 401) {
    emitSessionExpired();
    return;
  }

  const reader = res.body?.getReader();
  const decoder = new TextDecoder("utf-8");

  let buffer = "";

  while (true) {
    const { done, value } = await reader!.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    const parts = buffer.split("\n\n");
    buffer = parts.pop() || "";

    for (const part of parts) {

      if (!part.trim()) continue; // 🧠 ignore empty chunks

      const lines = part.split("\n").filter(Boolean);

      const eventLine = lines.find((l) => l.startsWith("event:"));
      const dataLine = lines.find((l) => l.startsWith("data:"));

      if (!eventLine || !dataLine) {
        console.warn("Malformed chunk:", part);
        continue;
      }

      const event = eventLine.replace("event: ", "").trim();
      const data = dataLine.replace("data: ", "").trim();

      let parsed = null;

      switch (event) {
        case "chunk":
          onChunk(data);
          break;

        case "warning":
          parsed = safeParse(data);
          if (!parsed) return;
          onWarning(parsed);
          break;

        case "error":
          parsed = safeParse(data);
          if (!parsed) return;
          onError(parsed);
          return;

        case "end":
          parsed = safeParse(data);
          if (!parsed) return;
          onEnd(parsed);
          return;
      }
    }
  }
};

// ---------------- SESSION (ARCHIVE) ----------------

export const archiveSessionApi = async (
  sessionId: string
): Promise<ApiResponse<ChatSession>> => {
  const res = await apiClient.patch<ApiResponse<ChatSession>>(
    `/chat/sessions/${sessionId}/archive`
  );
  return res.data;
};

export const unarchiveSessionApi = async (
  sessionId: string
): Promise<ApiResponse<ChatSession>> => {
  const res = await apiClient.patch<ApiResponse<ChatSession>>(
    `/chat/sessions/${sessionId}/unarchive`
  );
  return res.data;
};