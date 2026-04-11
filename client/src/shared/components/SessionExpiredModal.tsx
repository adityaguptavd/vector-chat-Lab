import { useNavigate } from "react-router-dom";
import { useAuth } from "@/features/auth/hooks/useAuthContext";

export const SessionExpiredModal = ({
  open,
}: {
  open: boolean;
}) => {
  const navigate = useNavigate();
  const { logout } = useAuth();

  if (!open) return null;

  const handleLogin = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
      <div className="bg-gray-900 text-white p-6 rounded-lg w-80 space-y-4 shadow-lg">
        <h2 className="text-lg font-semibold">Session Expired</h2>

        <p className="text-sm text-gray-400">
          Your session has expired. Please login again to continue.
        </p>

        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 hover:bg-blue-700 transition p-2 rounded"
        >
          Go to Login
        </button>
      </div>
    </div>
  );
};