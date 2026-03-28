export type ApiResponse<T> = {
  success: boolean;
  message: string;
  data: T;
  error_code?: string | null;
  errors?: any;
  metadata?: any;
  request_id: string;
};