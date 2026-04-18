export type ChatSession = {
  id: string;
  title?: string;
  created_at: string;
  updated_at: string;
  is_archived: boolean;
};

export type ChatMessage = {
  id: string;
  session_id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;
};

// Payloads
export type SendMessagePayload = {
  session_id: string;
  content: string;
};

export type StreamChunkHandler = (chunk: string) => void;

export type StreamEndPayload = {
  user_message: ChatMessage | null;
  ai_message: ChatMessage | null;
};

export type StreamError = {
  message: string;
};

export type StreamWarning = {
  message: string;
};

export type StreamMessageParams = {
  sessionId: string;
  content: string;
  token: string;

  onChunk: StreamChunkHandler;
  onEnd: (data: StreamEndPayload) => void;
  onError: (err: StreamError) => void;
  onWarning: (warn: StreamWarning) => void;
};

// archive/unarchive view
export type SessionView = "active" | "archived";