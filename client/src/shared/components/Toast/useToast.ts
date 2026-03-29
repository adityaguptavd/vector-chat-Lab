import { useState } from "react";

export type ToastItem = {
  id: string;
  message: string;
  type: "success" | "error" | "loading";
};

export const useToast = () => {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  const showToast = (
    message: string,
    type: ToastItem["type"] = "success",
    duration = 3000
  ) => {
    const id = crypto.randomUUID();

    setToasts((prev) => [...prev, { id, message, type }]);

    if (type !== "loading") {
      setTimeout(() => removeToast(id), duration);
    }

    return id;
  };

  const showPromise = async <T>(
    fn: () => Promise<{ success: boolean; data?: T; error?: string }>,
    messages: {
      loading: string;
      success: string;
      error?: string;
    }
  ) => {
    const id = showToast(messages.loading, "loading", 0);

    const result = await fn();

    if (result.success) {
      setToasts((prev) =>
        prev.map((t) =>
          t.id === id
            ? { ...t, message: messages.success, type: "success" }
            : t
        )
      );

      setTimeout(() => removeToast(id), 3000);

      return result;
    }

    const errorMessage =
      result.error || messages.error || "Something went wrong";

    setToasts((prev) =>
      prev.map((t) =>
        t.id === id
          ? {
              ...t,
              message: errorMessage,
              type: "error",
            }
          : t
      )
    );

    setTimeout(() => removeToast(id), 3000);

    return result;
  };

  return {
    toasts,
    showToast,
    showPromise,
    removeToast,
  };
};