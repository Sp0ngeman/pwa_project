import React, { useState } from "react";

const AddTaskForm = ({ addTask }) => {
  const [taskName, setTaskName] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("other");
  const [priority, setPriority] = useState("medium");
  const [dueDate, setDueDate] = useState("");
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (taskName.trim()) {
      addTask({
        name: taskName,
        description: description,
        category: category,
        priority: priority,
        due_date: dueDate || null
      });
      setTaskName("");
      setDescription("");
      setCategory("other");
      setPriority("medium");
      setDueDate("");
      setShowAdvanced(false);
    }
  };

  const priorityColors = {
    urgent: "#ff4444",
    high: "#ff8800",
    medium: "#ffaa00",
    low: "#44ff44"
  };

  return (
    <form onSubmit={handleSubmit} className="add-task-form">
      <div className="form-header">
        <input
          type="text"
          value={taskName}
          onChange={(e) => setTaskName(e.target.value)}
          placeholder="Add a new task..."
          className="task-input"
          required
        />
        <button type="submit" className="add-btn">
          Add Task
        </button>
      </div>

      <div className="form-options">
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="toggle-advanced-btn"
        >
          {showAdvanced ? "Hide Options" : "Show Options"}
        </button>
      </div>

      {showAdvanced && (
        <div className="advanced-options">
          <div className="form-row">
            <div className="form-group">
              <label>Description:</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Task description (optional)"
                rows="3"
                className="description-input"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Category:</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="category-select"
              >
                <option value="work">Work</option>
                <option value="personal">Personal</option>
                <option value="shopping">Shopping</option>
                <option value="health">Health</option>
                <option value="education">Education</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div className="form-group">
              <label>Priority:</label>
              <div className="priority-buttons">
                {["low", "medium", "high", "urgent"].map((p) => (
                  <button
                    key={p}
                    type="button"
                    className={`priority-btn ${priority === p ? 'active' : ''}`}
                    style={{ backgroundColor: priorityColors[p] }}
                    onClick={() => setPriority(p)}
                  >
                    {p.charAt(0).toUpperCase() + p.slice(1)}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Due Date:</label>
              <input
                type="datetime-local"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="due-date-input"
              />
            </div>
          </div>
        </div>
      )}
    </form>
  );
};

export default AddTaskForm; 