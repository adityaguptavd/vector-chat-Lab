import { Form } from "@/shared/components/Form/Form";
import { FormField } from "@/shared/components/Form/FormField";
import { Input } from "@/shared/components/Input";
import { useLogin } from "../hooks/useLogin";
import { useToastContext } from "@/shared/components/Toast/ToastContext";
import { useAuth } from "../hooks/useAuthContext";
import { useLocation, useNavigate, Link } from "react-router-dom";

export default function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const from = (location.state as any)?.from?.pathname || "/dashboard";

  const { loginUser, isLoading } = useLogin();
  const { showPromise } = useToastContext();

  const handleSubmit = async (values: Record<string, any>) => {
    const result = await showPromise(
      () =>
        loginUser({
          email: values.email,
          password: values.password,
        }),
      {
        loading: "Logging you in...",
        success: "Welcome back!",
        error: "Login failed",
      }
    );

    if (result.success && result.data) {
      login(result.data.access_token);
      navigate(from, { replace: true });
    }

  };

  return (
    <div className="h-screen flex items-center justify-center bg-gray-950 text-white">
      <Form onSubmit={handleSubmit}>
        <div className="w-80 bg-gray-900 p-6 rounded space-y-4">
          <h2 className="text-xl font-semibold">Login</h2>

          {/* Email */}
          <FormField
            name="email"
            rules={{ required: "Email is required" }}
          >
            <Input
              type="email"
              label="Email"
              placeholder="Enter email"
              className="w-full p-2 rounded bg-gray-800"
            />
          </FormField>

          {/* Password */}
          <FormField
            name="password"
            rules={{
              required: "Password is required",
            }}
          >
            <Input
              type="password"
              label="Password"
              placeholder="Enter password"
              className="w-full p-2 rounded bg-gray-800"
            />
          </FormField>

          {/* Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 p-2 rounded disabled:opacity-50"
          >
            {isLoading ? "Logging in..." : "Login"}
          </button>
          <div className="text-sm text-gray-400 text-center">
            Don't have an account?{" "}
            <Link
              to="/register"
              className="text-blue-400 hover:text-blue-300 hover:underline transition"
            >
              Register
            </Link>
          </div>
        </div>
      </Form>
    </div>
  );
}