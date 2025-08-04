import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from './components/Header';
import TaskList from './components/TaskList';
import AddTaskForm from './components/AddTaskForm';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    // Fetch tasks from Django API when component mounts
    axios.get('http://127.0.0.1:8000/tasks/api/tasks/')
      .then(response => {
        setTasks(response.data);
      })
      .catch(error => {
        console.error('Error fetching tasks:', error);
      });
  }, []);

  const addTask = async (taskName) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/tasks/api/tasks/create/', {
        task: taskName
      });
      setTasks([...tasks, response.data.task]);
    } catch (error) {
      console.error('Error adding task:', error);
    }
  };

  const deleteTask = async (taskId) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/tasks/api/tasks/delete/${taskId}/`);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  return (
    <div className="app">
      <Header title="My Task List" />
      <div className="task-container">
        <TaskList tasks={tasks} deleteTask={deleteTask} />
        <AddTaskForm addTask={addTask} />
      </div>
    </div>
  );
}

export default App;
