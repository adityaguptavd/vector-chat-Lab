import ToastContext from "./ToastContext";
import { useToast } from "./useToast";
import Toast from "@/shared/components/Toast/Toast";

export const ToastProvider = ({ children }: { children: React.ReactNode }) => {
  const { toasts, showToast, showPromise, removeToast } = useToast();

  return (
    <ToastContext.Provider
      value={{ toasts, showToast, showPromise, removeToast }}
    >
      {children}

      <div className="fixed top-5 right-5 flex flex-col gap-2 z-50">
        {toasts.map((t) => (
          <Toast key={t.id} message={t.message} type={t.type} />
        ))}
      </div>
    </ToastContext.Provider>
  );
};