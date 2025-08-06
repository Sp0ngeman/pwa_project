import React, { useState } from "react";
import TaskItem from "./TaskItem";

const TaskList = ({ tasks, deleteTask, updateTask }) => {
  const [filter, setFilter] = useState("all");
  const [sortBy, setSortBy] = useState("priority");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedTasks, setSelectedTasks] = useState([]);
  const [showBulkActions, setShowBulkActions] = useState(false);

  // Filter tasks based on current filter
  const filteredTasks = tasks.filter(task => {
    const matchesSearch = task.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         (task.description && task.description.toLowerCase().includes(searchQuery.toLowerCase()));
    
    if (!matchesSearch) return false;
    
    switch (filter) {
      case "completed":
        return task.completed;
      case "pending":
        return !task.completed;
      case "overdue":
        return task.due_date && new Date(task.due_date) < new Date() && !task.completed;
      default:
        return true;
    }
  });

  // Sort tasks
  const sortedTasks = [...filteredTasks].sort((a, b) => {
    switch (sortBy) {
      case "priority":
        const priorityOrder = { urgent: 4, high: 3, medium: 2, low: 1 };
        return priorityOrder[b.priority] - priorityOrder[a.priority];
      case "due_date":
        if (!a.due_date && !b.due_date) return 0;
        if (!a.due_date) return 1;
        if (!b.due_date) return -1;
        return new Date(a.due_date) - new Date(b.due_date);
      case "created_at":
        return new Date(b.created_at) - new Date(a.created_at);
      case "name":
        return a.name.localeCompare(b.name);
      default:
        return 0;
    }
  });

  const handleSelectTask = (taskId) => {
    setSelectedTasks(prev => 
      prev.includes(taskId) 
        ? prev.filter(id => id !== taskId)
        : [...prev, taskId]
    );
  };

  const handleSelectAll = () => {
    if (selectedTasks.length === sortedTasks.length) {
      setSelectedTasks([]);
    } else {
      setSelectedTasks(sortedTasks.map(task => task.id));
    }
  };

  const handleBulkAction = async (action) => {
    if (selectedTasks.length === 0) return;

    try {
      const response = await fetch('http://127.0.0.1:8000/tasks/api/tasks/bulk-update/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          task_ids: selectedTasks,
          action: action
        })
      });

      if (response.ok) {
        // Refresh the task list
        window.location.reload();
        setSelectedTasks([]);
        setShowBulkActions(false);
      }
    } catch (error) {
      console.error('Error performing bulk action:', error);
    }
  };

  const taskStats = {
    total: tasks.length,
    completed: tasks.filter(t => t.completed).length,
    pending: tasks.filter(t => !t.completed).length,
    overdue: tasks.filter(t => t.due_date && new Date(t.due_date) < new Date() && !t.completed).length
  };

  return (
    <div className="task-list-container">
      {/* Statistics */}
      <div className="task-stats">
        <div className="stat-item">
          <span className="stat-number">{taskStats.total}</span>
          <span className="stat-label">Total</span>
        </div>
        <div className="stat-item">
          <span className="stat-number">{taskStats.completed}</span>
          <span className="stat-label">Completed</span>
        </div>
        <div className="stat-item">
          <span className="stat-number">{taskStats.pending}</span>
          <span className="stat-label">Pending</span>
        </div>
        <div className="stat-item">
          <span className="stat-number">{taskStats.overdue}</span>
          <span className="stat-label">Overdue</span>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="task-controls">
        <div className="search-filter">
          <input
            type="text"
            placeholder="Search tasks..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Tasks</option>
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
            <option value="overdue">Overdue</option>
          </select>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="sort-select"
          >
            <option value="priority">Sort by Priority</option>
            <option value="due_date">Sort by Due Date</option>
            <option value="created_at">Sort by Created</option>
            <option value="name">Sort by Name</option>
          </select>
        </div>

        {sortedTasks.length > 0 && (
          <div className="bulk-actions">
            <label className="select-all-label">
              <input
                type="checkbox"
                checked={selectedTasks.length === sortedTasks.length}
                onChange={handleSelectAll}
              />
              Select All
            </label>
            
            {selectedTasks.length > 0 && (
              <div className="bulk-buttons">
                <button
                  onClick={() => handleBulkAction('complete')}
                  className="bulk-btn complete-btn"
                >
                  Complete Selected
                </button>
                <button
                  onClick={() => handleBulkAction('delete')}
                  className="bulk-btn delete-btn"
                >
                  Delete Selected
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Task List */}
      <ul className="task-list">
        {sortedTasks.length > 0 ? (
          sortedTasks.map(task => (
            <TaskItem 
              key={task.id} 
              task={task} 
              deleteTask={deleteTask}
              updateTask={updateTask}
            />
          ))
        ) : (
          <li className="no-tasks">
            {searchQuery || filter !== "all" 
              ? "No tasks match your search/filter criteria." 
              : "No tasks available. Add your first task above!"
            }
          </li>
        )}
      </ul>
    </div>
  );
};

export default TaskList; 