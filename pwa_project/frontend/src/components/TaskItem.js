import React, { useState } from "react";
import axios from "axios";

const TaskItem = ({ task, deleteTask, updateTask }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTask, setEditedTask] = useState({
    name: task.name,
    description: task.description || "",
    category: task.category || "other",
    priority: task.priority || "medium",
    due_date: task.due_date ? task.due_date.slice(0, 16) : "",
  });

  const priorityColors = {
    urgent: "#ff4444",
    high: "#ff8800",
    medium: "#ffaa00",
    low: "#44ff44"
  };

  const categoryIcons = {
    work: "💼",
    personal: "👤",
    shopping: "🛒",
    health: "🏥",
    education: "📚",
    other: "📝"
  };

  const handleToggleComplete = async () => {
    try {
      const response = await axios.post(`http://127.0.0.1:8000/tasks/api/tasks/toggle/${task.id}/`);
      updateTask(task.id, { completed: response.data.completed });
    } catch (error) {
      console.error('Error toggling task completion:', error);
    }
  };

  const handleSave = async () => {
    try {
      const response = await axios.put(`http://127.0.0.1:8000/tasks/api/tasks/update/${task.id}/`, editedTask);
      updateTask(task.id, response.data.task);
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const handleCancel = () => {
    setEditedTask({
      name: task.name,
      description: task.description || "",
      category: task.category || "other",
      priority: task.priority || "medium",
      due_date: task.due_date ? task.due_date.slice(0, 16) : "",
    });
    setIsEditing(false);
  };

  const formatDueDate = (dueDate) => {
    if (!dueDate) return null;
    const date = new Date(dueDate);
    const now = new Date();
    const diffTime = date - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 0) return `Overdue by ${Math.abs(diffDays)} days`;
    if (diffDays === 0) return "Due today";
    if (diffDays === 1) return "Due tomorrow";
    return `Due in ${diffDays} days`;
  };

  const isOverdue = task.due_date && new Date(task.due_date) < new Date() && !task.completed;

  return (
    <li className={`task-item ${task.completed ? "completed" : ""} ${isOverdue ? "overdue" : ""}`}>
      <div className="task-header">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggleComplete}
          className="task-checkbox"
        />
        
        <div className="task-priority" style={{ backgroundColor: priorityColors[task.priority] }}>
          {task.priority}
        </div>
        
        <span className="task-category">
          {categoryIcons[task.category]} {task.category}
        </span>
      </div>

      {isEditing ? (
        <div className="task-edit-form">
          <input
            type="text"
            value={editedTask.name}
            onChange={(e) => setEditedTask({...editedTask, name: e.target.value})}
            className="edit-task-name"
          />
          <textarea
            value={editedTask.description}
            onChange={(e) => setEditedTask({...editedTask, description: e.target.value})}
            placeholder="Description (optional)"
            className="edit-task-description"
          />
          <div className="edit-task-fields">
            <select
              value={editedTask.category}
              onChange={(e) => setEditedTask({...editedTask, category: e.target.value})}
            >
              <option value="work">Work</option>
              <option value="personal">Personal</option>
              <option value="shopping">Shopping</option>
              <option value="health">Health</option>
              <option value="education">Education</option>
              <option value="other">Other</option>
            </select>
            <select
              value={editedTask.priority}
              onChange={(e) => setEditedTask({...editedTask, priority: e.target.value})}
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
            <input
              type="datetime-local"
              value={editedTask.due_date}
              onChange={(e) => setEditedTask({...editedTask, due_date: e.target.value})}
            />
          </div>
          <div className="edit-buttons">
            <button onClick={handleSave} className="save-btn">Save</button>
            <button onClick={handleCancel} className="cancel-btn">Cancel</button>
          </div>
        </div>
      ) : (
        <div className="task-content">
          <span className="task-name">{task.name}</span>
          {task.description && (
            <p className="task-description">{task.description}</p>
          )}
          {task.due_date && (
            <span className={`task-due-date ${isOverdue ? 'overdue' : ''}`}>
              {formatDueDate(task.due_date)}
            </span>
          )}
        </div>
      )}

      <div className="task-actions">
        <button 
          className="edit-btn" 
          onClick={() => setIsEditing(true)}
        >
          ✏️
        </button>
        <button 
          className="delete-btn" 
          onClick={() => deleteTask(task.id)}
        >
          🗑️
        </button>
      </div>
    </li>
  );
};

export default TaskItem; 