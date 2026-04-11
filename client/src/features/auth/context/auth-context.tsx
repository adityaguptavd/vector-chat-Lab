import React, { createContext } from "react";

type User = {
  user_id: string;
  email: string;
};

type AuthContextType = {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (token: string) => void;
  logout: () => void;
  sessionExpired: boolean;
  setSessionExpired: React.Dispatch<React.SetStateAction<boolean>>
};

export const AuthContext = createContext<AuthContextType | null>(null);