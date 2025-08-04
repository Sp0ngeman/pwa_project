import React, { useState } from "react";

const TaskItem = ({ task, deleteTask }) => {
  const [isCompleted, setIsCompleted] = useState(false);

  const toggleComplete = () => {
    setIsCompleted(!isCompleted);
  };

  return (
    <li className={`task-item ${isCompleted ? "completed" : ""}`}>
      <input
        type="checkbox"
        checked={isCompleted}
        onChange={toggleComplete}
      />
      <span className="task-name">{task.name}</span>
      <button className="delete-btn" onClick={() => deleteTask(task.id)}>
        X
      </button>
    </li>
  );
};

export default TaskItem; 