import { apiClient } from "@/services/apiClient";
import { ApiResponse } from "@/shared/types/api";
import type { DocumentData } from "./types";

// Upload Document (single file)
export const uploadDocumentApi = async (
  file: File
): Promise<ApiResponse<DocumentData>> => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await apiClient.post<ApiResponse<DocumentData>>(
    "/documents/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const listDocumentsApi = async (): Promise<
  ApiResponse<DocumentData[]>
> => {
  const response = await apiClient.get<
    ApiResponse<DocumentData[]>
  >("/documents");

  return response.data;
};