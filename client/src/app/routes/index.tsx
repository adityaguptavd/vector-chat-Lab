import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ProtectedRoute } from "./ProtectedRoute";
import ProtectedLayout from "@/shared/components/layout/ProtectedLayout";
import { PublicRoute } from "./PublicRoute";

import LoginPage from "@/features/auth/pages/LoginPage";
import RegisterPage from "@/features/auth/pages/RegisterPage";
import Dashboard from "@/features/dashboard/pages/Dashboard";
import DocumentsPage from "@/features/documents/pages/DocumentsPage";
import ChatPage from "@/features/chat/pages/ChatPage";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <LoginPage />
            </PublicRoute>
          }
        />

        <Route
          path="/register"
          element={
            <PublicRoute>
              <RegisterPage />
            </PublicRoute>
          }
        />

        {/* Private */}
        <Route
          element={
            <ProtectedRoute>
              <ProtectedLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/" element={<Navigate to="/dashboard"></Navigate>} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/documents" element={<DocumentsPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/settings" element={<>Settings</>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;
