import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from './components/Header';
import TaskList from './components/TaskList';
import AddTaskForm from './components/AddTaskForm';
import TaskStats from './components/TaskStats';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('tasks');

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get('http://127.0.0.1:8000/tasks/api/tasks/');
      setTasks(response.data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      setError('Failed to load tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const addTask = async (taskData) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/tasks/api/tasks/create/', {
        task: taskData.name,
        description: taskData.description,
        category: taskData.category,
        priority: taskData.priority,
        due_date: taskData.due_date
      });
      setTasks([...tasks, response.data.task]);
    } catch (error) {
      console.error('Error adding task:', error);
      setError('Failed to add task. Please try again.');
    }
  };

  const deleteTask = async (taskId) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/tasks/api/tasks/delete/${taskId}/`);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (error) {
      console.error('Error deleting task:', error);
      setError('Failed to delete task. Please try again.');
    }
  };

  const updateTask = (taskId, updatedFields) => {
    setTasks(tasks.map(task => 
      task.id === taskId 
        ? { ...task, ...updatedFields }
        : task
    ));
  };

  const clearError = () => {
    setError(null);
  };

  if (loading) {
    return (
      <div className="app">
        <Header title="My Task List" />
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <Header title="My Task List" />
      
      {error && (
        <div className="error-message">
          <span>{error}</span>
          <button onClick={clearError} className="error-close">×</button>
        </div>
      )}
      
      {/* Tab Navigation */}
      <div className="tab-navigation">
        <button 
          className={`tab-btn ${activeTab === 'tasks' ? 'active' : ''}`}
          onClick={() => setActiveTab('tasks')}
        >
          📝 Tasks
        </button>
        <button 
          className={`tab-btn ${activeTab === 'analytics' ? 'active' : ''}`}
          onClick={() => setActiveTab('analytics')}
        >
          📊 Analytics
        </button>
      </div>
      
      <div className="task-container">
        {activeTab === 'tasks' ? (
          <>
            <AddTaskForm addTask={addTask} />
            <TaskList 
              tasks={tasks} 
              deleteTask={deleteTask}
              updateTask={updateTask}
            />
          </>
        ) : (
          <TaskStats tasks={tasks} />
        )}
      </div>
    </div>
  );
}

export default App;
