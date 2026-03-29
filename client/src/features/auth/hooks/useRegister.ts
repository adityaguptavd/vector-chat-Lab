import { useState } from "react";
import { registerApi } from "../api";
import type { RegisterPayload, RegisterData } from "../types";
import { apiHandler } from "@/services/apiHandler";
import { ApiResponse } from "@/shared/types/api";
import { Result } from "@/shared/types/result";

export const useRegister = () => {
  const [data, setData] = useState<RegisterData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const registerUser = async (payload: RegisterPayload):Promise<Result<RegisterData>> => {
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
      return { success: false, error: httpError.message };
    }

    // Business error
    if (!res || !res.success) {
      const message = res?.message || "Something went wrong"
      setError(message);
      setIsLoading(false);
      return { success: false, error: message };
    }

    // Success
    setData(res.data);
    setIsLoading(false);
    return { success: true, data: res.data };
  };

  return {
    data,
    isLoading,
    error,
    registerUser,
  };
};