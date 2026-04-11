export const AUTH_EVENTS = {
  SESSION_EXPIRED: "SESSION_EXPIRED",
};

export const emitSessionExpired = () => {
  window.dispatchEvent(new Event(AUTH_EVENTS.SESSION_EXPIRED));
};