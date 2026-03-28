import { useState } from "react";
import { registerApi } from "../api";
import type { RegisterPayload, RegisterData } from "../types";
import { apiHandler } from "@/services/apiHandler";
import { ApiResponse } from "@/shared/types/api";

export const useRegister = () => {
  const [data, setData] = useState<RegisterData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const registerUser = async (payload: RegisterPayload) => {
    setIsLoading(true);
    setError(null);

    const { data: res, error: httpError } =
        await apiHandler<ApiResponse<RegisterData>>(
            registerApi(payload)
        );

    // HTTP / Network error
    if (httpError) {
      setError(httpError.message);
      setIsLoading(false);
      return;
    }

    // Business error
    if (!res || !res.success) {
        setError(res?.message || "Something went wrong");
        setIsLoading(false);
        return;
    }

    // Success
    setData(res.data);
    localStorage.setItem("access_token", res.data.access_token);
    setIsLoading(false);
  };

  return {
    data,
    isLoading,
    error,
    registerUser,
  };
};