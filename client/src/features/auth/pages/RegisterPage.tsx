import { useState } from "react";
import { useRegister } from "../hooks/useRegister";

export default function RegisterPage() {
  const { registerUser, isLoading, error, data } = useRegister();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e: React.SubmitEvent) => {
    e.preventDefault();

    await registerUser({ email, password });
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gray-950 text-white">
      <form
        onSubmit={handleSubmit}
        className="w-80 bg-gray-900 p-6 rounded space-y-4"
      >
        <h2 className="text-xl font-semibold">Register</h2>

        {/* Email */}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-2 rounded bg-gray-800 outline-none"
        />

        {/* Password */}
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 rounded bg-gray-800 outline-none"
        />

        {/* Error */}
        {error && (
          <p className="text-red-400 text-sm">{error}</p>
        )}

        {/* Success */}
        {data && (
          <p className="text-green-400 text-sm">
            Registered successfully!
          </p>
        )}

        {/* Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-600 p-2 rounded disabled:opacity-50"
        >
          {isLoading ? "Registering..." : "Register"}
        </button>
      </form>
    </div>
  );
}