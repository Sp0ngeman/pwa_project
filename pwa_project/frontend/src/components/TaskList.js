import React from "react";
import TaskItem from "./TaskItem";

const TaskList = ({ tasks, deleteTask }) => (
  <ul className="task-list">
    {tasks.length > 0 ? (
      tasks.map(task => (
        <TaskItem key={task.id} task={task} deleteTask={deleteTask} />
      ))
    ) : (
      <li>No tasks available.</li>
    )}
  </ul>
);

export default TaskList; 