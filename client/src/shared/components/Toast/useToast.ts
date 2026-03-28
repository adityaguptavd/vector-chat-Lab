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
    promise: Promise<T>,
    messages: {
      loading: string;
      success: string;
      error: string;
    }
  ) => {
    const id = showToast(messages.loading, "loading", 0);

    try {
      const result = await promise;

      setToasts((prev) =>
        prev.map((t) =>
          t.id === id
            ? { ...t, message: messages.success, type: "success" }
            : t
        )
      );

      setTimeout(() => removeToast(id), 3000);

      return result;
    } catch (err: any) {
      setToasts((prev) =>
        prev.map((t) =>
          t.id === id
            ? {
                ...t,
                message: err?.message || messages.error,
                type: "error",
              }
            : t
        )
      );

      setTimeout(() => removeToast(id), 3000);

      throw err;
    }
  };

  return {
    toasts,
    showToast,
    showPromise,
    removeToast,
  };
};