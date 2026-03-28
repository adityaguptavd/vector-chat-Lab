import { useState } from "react";
import { loginApi } from "../api";
import type { LoginPayload, LoginData } from "../types";
import { apiHandler } from "@/services/apiHandler";
import { ApiResponse } from "@/shared/types/api";
import { Result } from "@/shared/types/result";

export const useLogin = () => {
  const [data, setData] = useState<LoginData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loginUser = async (
    payload: LoginPayload
  ): Promise<Result<LoginData>> => {
    setIsLoading(true);
    setError(null);

    const { data: res, error: httpError } =
      await apiHandler<ApiResponse<LoginData>>(loginApi(payload));

    // HTTP / Network error
    if (httpError) {
      setError(httpError.message);
      setIsLoading(false);
      return { success: false, error: httpError.message };
    }

    // Business error
    if (!res || !res.success) {
      const message = res?.message || "Invalid credentials";
      setError(message);
      setIsLoading(false);
      return { success: false, error: message };
    }

    // Success
    setData(res.data);
    localStorage.setItem("access_token", res.data.access_token);
    setIsLoading(false);

    return { success: true, data: res.data };
  };

  return {
    data,
    isLoading,
    error,
    loginUser,
  };
};