import './App.css'
import { useState } from 'react'

function TodoItem({todo, toggleDone, deleteTodo, addNewComment}) {
  const [newComment, setNewComment] = useState("");

  return (
    <li>
      <span className={todo.done ? "done" : ""}>
        {todo.title}
      </span>

      <button onClick={() => toggleDone(todo.id)}>Toggle</button>
      <button onClick={() => deleteTodo(todo.id)}>❌</button>

      {/* ✅ ไม่มี comment */}
      {todo.comments && todo.comments.length === 0 && (
        <p>No comments</p>
      )}

      {/* ✅ มี comment */}
      {todo.comments && todo.comments.length > 0 && (
        <>
          <b>Comments:</b>
          <p>{todo.comments.length}</p>
          <ul>
            {todo.comments.map(comment => (
              <li key={comment.id}>{comment.message}</li>
            ))}
          </ul>
        </>
      )}

      <div className="new-comment-forms">
        <input
          type="text"
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
        />

        <button
          onClick={() => {
            addNewComment(todo.id, newComment);
            setNewComment("");
          }}
        >
          Add Comment
        </button>
      </div>
    </li>
  )
}

export default TodoItem