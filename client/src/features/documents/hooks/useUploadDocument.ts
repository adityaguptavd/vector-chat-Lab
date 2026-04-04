import { useState } from "react";
import { uploadDocumentApi } from "../api";
import type { DocumentData } from "../types";
import { apiHandler } from "@/services/apiHandler";
import { ApiResponse } from "@/shared/types/api";
import { Result } from "@/shared/types/result";

export const useUploadDocument = () => {
  const [data, setData] = useState<DocumentData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const uploadDocument = async (
    file: File
  ): Promise<Result<DocumentData>> => {
    setIsLoading(true);
    setError(null);

    const { data: res, error: httpError } =
      await apiHandler<ApiResponse<DocumentData>>(
        uploadDocumentApi(file)
      );

    // HTTP / Network error
    if (httpError) {
      setError(httpError.message);
      setIsLoading(false);
      return { success: false, error: httpError.message };
    }

    // Business error
    if (!res || !res.success) {
      const message = res?.message || "Upload failed";
      setError(message);
      setIsLoading(false);
      return { success: false, error: message };
    }

    // ✅ Success
    setData(res.data);
    setIsLoading(false);

    return { success: true, data: res.data };
  };

  return {
    data,
    isLoading,
    error,
    uploadDocument,
  };
};