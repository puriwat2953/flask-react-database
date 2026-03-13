import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

export default function PrivateRoute({ children }) {
  const { accessToken } = useAuth();

  return (accessToken ? children : <Navigate to="/login" replace />);

}