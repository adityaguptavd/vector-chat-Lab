import AppRoutes from "@/app/routes";
import { ToastProvider } from "@/shared/components/Toast/ToastProvider";

export default function App() {
  return (
    <ToastProvider>
      <AppRoutes />;
    </ToastProvider>
  );
}
