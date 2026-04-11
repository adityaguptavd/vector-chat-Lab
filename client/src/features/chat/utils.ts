import type { ChatMessage } from "./types";
import type { StreamEndPayload } from "./types";

export const normalizeMessages = (
  payload: StreamEndPayload
): ChatMessage[] => {
  return [payload.user_message, payload.ai_message].filter(
    (m): m is ChatMessage => m !== null
  );
};