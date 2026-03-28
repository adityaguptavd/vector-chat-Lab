import { apiClient } from "@/services/apiClient";
import { ApiResponse } from "@/shared/types/api";
import type { RegisterPayload, RegisterData } from "./types";

export const registerApi = async (
  payload: RegisterPayload
): Promise<ApiResponse<RegisterData>> => {
  const response = await apiClient.post<ApiResponse<RegisterData>>(
    "/auth/register",
    payload
  );

  return response.data;
};