import { useState, useEffect } from "react";
import { AuthContext } from "./auth-context";
import { useMe } from "../hooks/useMe";

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const { getMe } = useMe();

  const isAuthenticated = !!token;

  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem("access_token");

      if (!storedToken) {
        setLoading(false);
        return;
      }

      // temporarily set token (needed for api calls)
      setToken(storedToken);

      const result = await getMe();

      if (!result.success) {
        // invalid token → cleanup
        localStorage.removeItem("access_token");
        setToken(null);
      }

      // valid → keep token
      setLoading(false);
    };

    initAuth();
  }, [token]);

  const login = (newToken: string) => {
    localStorage.setItem("access_token", newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
  };

  return (
    <AuthContext.Provider
      value={{ token, isAuthenticated, loading, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};