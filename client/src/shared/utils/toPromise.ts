import { Result } from "@/shared/types/result";

export const toPromise = async <T>(fn: Promise<Result<T>>): Promise<T> => {
  const res = await fn;

  if (!res.success) {
    throw new Error(res.error);
  }

  return res.data;
};