import React from 'react';

function Header({ title }) {
  return (
    <header className="header">
      <h1>{title}</h1>
      <div className="user-info">
        Welcome, User
      </div>
    </header>
  );
}

export default Header; 