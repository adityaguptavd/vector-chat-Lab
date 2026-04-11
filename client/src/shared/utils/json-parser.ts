export const safeParse = (str: string) => {
  try {
    return JSON.parse(str);
  } catch {
    return null;
  }
};