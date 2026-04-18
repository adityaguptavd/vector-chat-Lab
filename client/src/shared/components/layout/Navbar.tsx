import { useNavigate } from "react-router-dom";
import { useAuth } from "@/features/auth/hooks/useAuthContext";

const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header className="h-16 bg-gray-900 border-b border-gray-700 flex items-center justify-between px-6">
      {/* Left: App Name */}
      <div
        className="text-lg font-semibold cursor-pointer"
        onClick={() => navigate("/dashboard")}
      >
        VectorChatLab
      </div>

      {/* Right: User Section */}
      {isAuthenticated && (
        <div className="flex items-center gap-4">
          {/* User Info */}
          <div className="text-sm text-gray-300 hidden sm:block">
            <p className="font-medium text-white">{user?.full_name || "User"}</p>
            <p className="text-xs text-gray-400">{user?.email}</p>
          </div>

          {/* Logout Button */}
          <button
            onClick={handleLogout}
            className="bg-red-600 hover:bg-red-700 transition px-3 py-1.5 rounded-md text-sm font-medium"
          >
            Logout
          </button>
        </div>
      )}
    </header>
  );
};

export default Navbar;