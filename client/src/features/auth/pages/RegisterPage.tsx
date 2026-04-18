import { Form } from "@/shared/components/Form/Form";
import { FormField } from "@/shared/components/Form/FormField";
import { Input } from "@/shared/components/Input";
import { useRegister } from "../hooks/useRegister";
import { useToastContext } from "@/shared/components/Toast/ToastContext";
import { useAuth } from "../hooks/useAuthContext";
import { useLocation, useNavigate, Link } from "react-router-dom";

export default function RegisterPage() {

  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const from = (location.state as any)?.from?.pathname || "/dashboard";

  const { registerUser, isLoading, error, data } = useRegister();

  const { showPromise } = useToastContext();

  const handleSubmit = async (values: Record<string, any>) => {
    const result = await showPromise(
      () =>
        registerUser({
          email: values.email,
          password: values.password,
          full_name: values.full_name
        }),
      {
        loading: "Creating your account...",
        success: "Welcome aboard!",
        error: "Registration failed",
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
          <h2 className="text-xl font-semibold">Register</h2>

          {/* Email */}
          <FormField
            name="full_name"
            rules={{ required: "Full Name is required" }}
          >
            <Input
              type="text"
              label="Full Name"
              placeholder="Enter full name"
              className="w-full p-2 rounded bg-gray-800 outline-none"
            />
          </FormField>

          {/* Email */}
          <FormField
            name="email"
            rules={{ required: "Email is required" }}
          >
            <Input
              type="email"
              label="Email"
              placeholder="Enter email"
              className="w-full p-2 rounded bg-gray-800 outline-none"
            />
          </FormField>

          {/* Password */}
          <FormField
            name="password"
            rules={{
              required: "Password is required",
              minLength: {
                value: 6,
                message: "Minimum 6 characters required",
              },
            }}
          >
            <Input
              type="password"
              label="Password"
              placeholder="Enter password"
              className="w-full p-2 rounded bg-gray-800 outline-none"
            />
          </FormField>

          {/* API Error (NOT form validation) */}
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
          <div className="text-sm text-gray-400 text-center">
            Already have an account?{" "}
            <Link
              to="/login"
              className="text-blue-400 hover:text-blue-300 hover:underline transition"
            >
              Login
            </Link>
          </div>
        </div>
      </Form>
    </div>
  );
}