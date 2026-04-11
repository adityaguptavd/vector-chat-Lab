export const FullScreenLoader = ({
  message = "Loading...",
}: {
  message?: string;
}) => {
  return (
    <div className="h-screen flex flex-col items-center justify-center bg-gray-950 text-white">
      {/* Spinner */}
      <div className="relative w-12 h-12">
        <div className="absolute inset-0 rounded-full border-4 border-blue-500 border-t-transparent animate-spin shadow-[0_0_15px_rgba(59,130,246,0.6)]"></div>
      </div>

      <h1 className="text-lg font-semibold text-blue-400 mb-3">VectorChat</h1>

      {/* Text */}
      <p className="mt-4 text-sm text-gray-400 animate-pulse">{message}</p>
    </div>
  );
};
