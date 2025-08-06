import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TaskStats = ({ tasks }) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchStats();
  }, [tasks]);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://127.0.0.1:8000/tasks/api/tasks/stats/');
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateProgress = () => {
    if (!stats || stats.total === 0) return 0;
    return Math.round((stats.completed / stats.total) * 100);
  };

  const getPriorityColor = (priority) => {
    const colors = {
      urgent: '#ff4444',
      high: '#ff8800',
      medium: '#ffaa00',
      low: '#44ff44'
    };
    return colors[priority] || '#666';
  };

  const getCategoryIcon = (category) => {
    const icons = {
      work: '💼',
      personal: '👤',
      shopping: '🛒',
      health: '🏥',
      education: '📚',
      other: '📝'
    };
    return icons[category] || '📝';
  };

  if (loading) {
    return (
      <div className="stats-loading">
        <div className="spinner"></div>
        <p>Loading statistics...</p>
      </div>
    );
  }

  if (!stats) {
    return null;
  }

  const progress = calculateProgress();

  return (
    <div className="task-stats-container">
      <h3>Task Analytics</h3>
      
      {/* Progress Overview */}
      <div className="progress-section">
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        <div className="progress-text">
          {progress}% Complete ({stats.completed}/{stats.total} tasks)
        </div>
      </div>

      {/* Quick Stats */}
      <div className="quick-stats">
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <div className="stat-value">{stats.total}</div>
            <div className="stat-label">Total Tasks</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <div className="stat-value">{stats.completed}</div>
            <div className="stat-label">Completed</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">⏳</div>
          <div className="stat-content">
            <div className="stat-value">{stats.pending}</div>
            <div className="stat-label">Pending</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <div className="stat-value">{stats.overdue}</div>
            <div className="stat-label">Overdue</div>
          </div>
        </div>
      </div>

      {/* Priority Breakdown */}
      <div className="breakdown-section">
        <h4>Tasks by Priority</h4>
        <div className="priority-breakdown">
          {Object.entries(stats.by_priority).map(([priority, count]) => (
            <div key={priority} className="priority-item">
              <div 
                className="priority-indicator" 
                style={{ backgroundColor: getPriorityColor(priority) }}
              ></div>
              <div className="priority-info">
                <span className="priority-name">{priority}</span>
                <span className="priority-count">{count} tasks</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Category Breakdown */}
      <div className="breakdown-section">
        <h4>Tasks by Category</h4>
        <div className="category-breakdown">
          {Object.entries(stats.by_category).map(([category, count]) => (
            <div key={category} className="category-item">
              <div className="category-icon">
                {getCategoryIcon(category)}
              </div>
              <div className="category-info">
                <span className="category-name">{category}</span>
                <span className="category-count">{count} tasks</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Productivity Insights */}
      <div className="insights-section">
        <h4>Productivity Insights</h4>
        <div className="insights">
          {progress >= 80 && (
            <div className="insight positive">
              🎉 Great job! You're making excellent progress on your tasks.
            </div>
          )}
          {stats.overdue > 0 && (
            <div className="insight warning">
              ⚠️ You have {stats.overdue} overdue task{stats.overdue > 1 ? 's' : ''}. 
              Consider prioritizing these items.
            </div>
          )}
          {stats.pending > stats.completed && (
            <div className="insight info">
              📝 You have more pending tasks than completed ones. 
              Focus on completing a few tasks to build momentum.
            </div>
          )}
          {stats.total === 0 && (
            <div className="insight info">
              🚀 Ready to get started? Add your first task to begin tracking your progress!
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TaskStats; 