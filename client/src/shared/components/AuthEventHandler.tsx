import { useEffect } from "react";
import { AUTH_EVENTS } from "@/shared/events/authEvents";
import { SessionExpiredModal } from "./SessionExpiredModal";
import { useAuth } from "@/features/auth/hooks/useAuthContext";

export const AuthEventHandler = () => {
  const { sessionExpired, setSessionExpired } = useAuth();

  useEffect(() => {
    const handler = () => {
      setSessionExpired((prev) => prev || true);
    };

    window.addEventListener(AUTH_EVENTS.SESSION_EXPIRED, handler);

    return () => {
      window.removeEventListener(AUTH_EVENTS.SESSION_EXPIRED, handler);
    };
  }, []);

  return <SessionExpiredModal open={sessionExpired} />;
};