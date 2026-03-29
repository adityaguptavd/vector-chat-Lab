import { useState } from "react";
import { getMeApi } from "../api";
import { UserData } from "../types";
import { apiHandler } from "@/services/apiHandler";
import { ApiResponse } from "@/shared/types/api";
import { Result } from "@/shared/types/result";

export const useMe = () => {
  const [data, setData] = useState<UserData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getMe = async (): Promise<Result<UserData>> => {
    setIsLoading(true);
    setError(null);

    const { data: res, error: httpError } =
      await apiHandler<ApiResponse<UserData>>(getMeApi());

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
    setIsLoading(false);

    return { success: true, data: res.data };
  };

  return {
    data,
    isLoading,
    error,
    getMe,
  };
};