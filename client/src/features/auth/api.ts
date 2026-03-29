import { apiClient } from "@/services/apiClient";
import { ApiResponse } from "@/shared/types/api";
import type { RegisterPayload, RegisterData, LoginData, LoginPayload, UserData } from "./types";

export const registerApi = async (
  payload: RegisterPayload
): Promise<ApiResponse<RegisterData>> => {
  const response = await apiClient.post<ApiResponse<RegisterData>>(
    "/auth/register",
    payload
  );

  return response.data;
};

export const loginApi = async (
  payload: LoginPayload
): Promise<ApiResponse<LoginData>> => {
  const response = await apiClient.post<ApiResponse<LoginData>>(
    "/auth/login",
    payload
  );

  return response.data;
};

export const getMeApi = async (): Promise<ApiResponse<UserData>> => {
  const response = await apiClient.get<ApiResponse<UserData>>(
    "/users/me",
  );

  return response.data;
};