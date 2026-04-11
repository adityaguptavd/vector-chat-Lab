import AppRoutes from "@/app/routes";
import { AuthProvider } from "@/features/auth/context/AuthProvider";
import { ToastProvider } from "@/shared/components/Toast/ToastProvider";

export default function App() {
  return (
    <AuthProvider>
      <ToastProvider>
        <AppRoutes />;
      </ToastProvider>
    </AuthProvider>
  );
}
