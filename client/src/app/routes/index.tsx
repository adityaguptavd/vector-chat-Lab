import { BrowserRouter, Routes, Route } from "react-router-dom";
import RegisterPage from "@/features/auth/pages/RegisterPage";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<RegisterPage />} />
      </Routes>
    </BrowserRouter>
  );
}