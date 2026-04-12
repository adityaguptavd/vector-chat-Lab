import { useEffect, useState } from "react";
import { listDocumentsApi } from "../api";
import { apiHandler } from "@/services/apiHandler";
import type { DocumentData } from "../types";
import type { ApiResponse } from "@/shared/types/api";

export const useDocuments = () => {
  const [data, setData] = useState<DocumentData[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchDocuments = async () => {
    setIsLoading(true);
    setError(null);

    const { data: res, error: httpError } =
      await apiHandler<ApiResponse<DocumentData[]>>(
        listDocumentsApi()
      );

    if (httpError) {
      setError(httpError.message);
      setIsLoading(false);
      return;
    }

    if (!res || !res.success) {
      setError(res?.message || "Failed to fetch documents");
      setIsLoading(false);
      return;
    }

    setData(res.data);
    setIsLoading(false);
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  return {
    data,
    isLoading,
    error,
    fetchDocuments,
  };
};