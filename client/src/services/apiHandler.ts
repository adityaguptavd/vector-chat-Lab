type ApiHandlerError = {
  message: string;
  code?: string | null;
  raw?: any;
};

type ApiHandlerResponse<T> = {
  data: T | null;
  error: ApiHandlerError | null;
};

export async function apiHandler<T>(
  promise: Promise<T>
): Promise<ApiHandlerResponse<T>> {
  try {
    const data = await promise;

    return {
      data,
      error: null,
    };
  } catch (err: any) {
    return {
      data: null,
      error: {
        message:
          err?.response?.data?.message ||
          err?.message ||
          "Something went wrong",
        code: err?.response?.data?.error_code || null,
        raw: err,
      },
    };
  }
}