import { BrowserRouter, Routes, Route } from "react-router-dom";
import RegisterPage from "@/features/auth/pages/RegisterPage";
import LoginPage from "@/features/auth/pages/LoginPage";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </BrowserRouter>
  );
}