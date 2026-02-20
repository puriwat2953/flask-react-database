import { render, screen } from '@testing-library/react'
import { expect } from 'vitest'
import TodoItem from '../TodoItem.jsx'
import userEvent from '@testing-library/user-event'
const baseTodo = {             
  id: 1,
  title: 'Sample Todo',
  done: false,
  comments: [],
};
describe('TodoItem', () => {
  it('renders with no comments correctly', () => {
    render(
      <TodoItem todo={baseTodo} />  );
        expect(screen.getByText('Sample Todo')).toBeInTheDocument();
        expect(screen.getByText('No comments')).toBeInTheDocument();
  });

  it('renders with comments correctly', () => {
    const todoWithComment = {
      ...baseTodo,
      comments: [
        {id: 1, message: 'First comment'},
        {id: 2, message: 'Another comment'},
      ]
    };
    render(
      <TodoItem todo={todoWithComment} />
    );
    expect(screen.getByText(/2/)).toBeInTheDocument();
    expect(screen.getByText('Sample Todo')).toBeInTheDocument();
    expect(screen.getByText('First comment')).toBeInTheDocument();
    expect(screen.getByText('Another comment')).toBeInTheDocument();

  });

    it('does not show no comments message when it has a comment', () => {
    const todoWithComment = {
      ...baseTodo,
      comments: [
        {id: 1, message: 'First comment'},
      ]
    };
    render(
      <TodoItem todo={todoWithComment} />
    );
    expect(screen.queryByText('No comments')).not.toBeInTheDocument();
  });  
  
  it('makes callback to toggleDone when Toggle button is clicked', () => {
    const onToggleDone = vi.fn();
    render(
      <TodoItem 
       todo={baseTodo} 
       toggleDone={onToggleDone} />
    );
    const button = screen.getByRole('button', { name: /toggle/i });
    button.click();
    expect(onToggleDone).toHaveBeenCalledWith(baseTodo.id);
  });
  it('makes callback to addNewComment when a new comment is added', async () => {
    const onAddNewComment = vi.fn();
    const user = userEvent.setup();   // 👈 เพิ่มอันนี้

    render(
      <TodoItem
        todo={baseTodo}
        toggleDone={vi.fn()}
        deleteTodo={vi.fn()}
        addNewComment={onAddNewComment}
      />
    );

    const input = screen.getByRole('textbox');
    await user.type(input, 'New comment');  // 👈 ใช้ user แทน

    const button = screen.getByRole('button', { name: /add comment/i });
    await user.click(button);               // 👈 ใช้ user.click แทน fireEvent

    expect(onAddNewComment).toHaveBeenCalledWith(baseTodo.id, 'New comment');
  });
  
  });
