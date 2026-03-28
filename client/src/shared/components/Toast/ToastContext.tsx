import { createContext, useContext } from "react";
import { useToast } from "./useToast";

type ToastContextType = ReturnType<typeof useToast> | null;

const ToastContext = createContext<ToastContextType>(null);

export const useToastContext = () => {
  const context = useContext(ToastContext);

  if (!context) {
    throw new Error("useToastContext must be used within ToastProvider");
  }

  return context;
};

export default ToastContext;