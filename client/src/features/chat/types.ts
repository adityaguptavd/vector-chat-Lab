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