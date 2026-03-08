import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from './AuthContext.jsx'; // ✅ แก้ path
import './App.css'
import LoginForm from './LoginForm.jsx';
import TodoList from './TodoList.jsx'
import PrivateRoute from './PrivateRoute.jsx'; 

function App() {
  const TODOLIST_API_URL = 'http://localhost:5000/api/todos/';
  const TODOLIST_LOGIN_URL = 'http://localhost:5000/api/login/';

  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route 
            path="/" 
            element={
              <PrivateRoute>
                <TodoList apiUrl={TODOLIST_API_URL}/>
              </PrivateRoute>
            } 
          />
          <Route 
            path="/about" 
            element={
              <>
                <h1>About</h1>
                <p>This is a simple todo list application built with React and Flask.</p>
                <a href="/">Back to Home</a>
              </>
            } 
          />
          <Route
            path="/login"
            element={<LoginForm loginUrl={TODOLIST_LOGIN_URL} />}
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App