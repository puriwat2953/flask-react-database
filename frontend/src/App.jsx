import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from './context/AuthContext.jsx';
import './App.css'

import TodoList from './TodoList.jsx'

function App() {
  const TODOLIST_API_URL = 'http://localhost:5000/api/todos/';

  return (
    <TodoList apiUrl={TODOLIST_API_URL}/>
  )
}

export default App