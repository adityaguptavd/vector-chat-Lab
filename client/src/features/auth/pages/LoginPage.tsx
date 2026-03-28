import { Form } from "@/shared/components/Form/Form";
import { FormField } from "@/shared/components/Form/FormField";
import { Input } from "@/shared/components/Input";
import { useLogin } from "../hooks/useLogin";
import { useToastContext } from "@/shared/components/Toast/ToastContext";
import { toPromise } from "@/shared/utils/toPromise";

export default function LoginPage() {
  const { loginUser, isLoading } = useLogin();
  const { showPromise } = useToastContext();

  const handleSubmit = async (values: Record<string, any>) => {
    await showPromise(
      toPromise(
        loginUser({
          email: values.email,
          password: values.password,
        })
      ),
      {
        loading: "Logging you in...",
        success: "Welcome back!",
        error: "Invalid credentials",
      }
    );
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
        </div>
      </Form>
    </div>
  );
}