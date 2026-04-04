import { useAuth } from "@/features/auth/hooks/useAuthContext";

const Dashboard = () => {
  const { user, loading } = useAuth();

  if (loading) return <div className="text-white">Loading...</div>;

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <section className="bg-gray-800 border border-gray-700 rounded-lg p-6">
        <h1 className="text-2xl font-semibold text-white">
          Welcome back{user?.email ? `, ${user.email}` : ""} 👋
        </h1>
        <p className="text-gray-400 mt-1">
          Here's what's happening with your workspace today.
        </p>
      </section>

      {/* User Info Card */}
      <section className="bg-gray-800 border border-gray-700 rounded-lg p-6">
        <h2 className="text-lg font-medium text-white mb-4">
          Your Information
        </h2>

        <div className="space-y-2 text-sm">
          <p className="text-gray-300">
            <span className="text-gray-400">Name:</span>{" "}
            {user?.user_id.toUpperCase() || "N/A"}
          </p>
          <p className="text-gray-300">
            <span className="text-gray-400">Email:</span> {user?.email || "N/A"}
          </p>
        </div>
      </section>

      {/* Placeholder Section (Future Widgets) */}
      <section className="bg-gray-800 border border-gray-700 rounded-lg p-6">
        <h2 className="text-lg font-medium text-white mb-2">Coming Soon 🚀</h2>
        <p className="text-gray-400 text-sm">
          This space will soon show your recent chats, uploaded documents, and
          activity.
        </p>
      </section>
    </div>
  );
};

export default Dashboard;
