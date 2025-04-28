import React, { useContext, useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import '../styles/components/Sidebar.css';
import { AuthContext } from '../context/AuthContext';

const Sidebar = () => {
  const { user } = useContext(AuthContext);
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);
  const [isExpanded, setIsExpanded] = useState(false);

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  // Handle sidebar toggle on mobile
  const toggleSidebar = () => {
    if (isMobile) {
      setIsExpanded(!isExpanded);
    }
  };

  // Close sidebar when clicking outside on mobile
  useEffect(() => {
    const handleClickOutside = (event) => {
      const sidebar = document.querySelector('.sidebar');
      if (isMobile && isExpanded && sidebar && !sidebar.contains(event.target)) {
        setIsExpanded(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isMobile, isExpanded]);

  return (
    <aside className={`sidebar ${isExpanded ? 'expanded' : ''}`}>
      {isMobile && (
        <button className="sidebar-toggle" onClick={toggleSidebar}>
          {isExpanded ? (
            <i className="fas fa-times"></i>
          ) : 
          (
            <i className=""></i>
          )}
        </button>
      )}
      
      <h2 className="sidebar-logo">TuneViewer</h2>
      
      <nav className="sidebar-nav">
        <NavLink to="/" className="nav-item" onClick={toggleSidebar}>
          <i className="fas fa-home"></i>
          <span>Главная</span>
        </NavLink>
        
        <NavLink to="/search" className="nav-item" onClick={toggleSidebar}>
          <i className="fas fa-search"></i>
          <span>Поиск</span>
        </NavLink>
        
        <NavLink to="/playlists" className="nav-item" onClick={toggleSidebar}>
          <i className="fas fa-list"></i>
          <span>Плейлисты</span>
        </NavLink>
        
        <NavLink to="/profile" className="nav-item" onClick={toggleSidebar}>
          <i className="fas fa-user"></i>
          <span>Профиль</span>
        </NavLink>
        
        <NavLink to="/about" className="nav-item" onClick={toggleSidebar}>
          <i className="fas fa-info-circle"></i>
          <span>О нас</span>
        </NavLink>
        
        {user.isAuthenticated && user.role === 'admin' && (
          <NavLink to="/admin" className="nav-item_admin" onClick={toggleSidebar}>
            <i className="fas fa-shield-alt"></i>
            <span>Админ-панель</span>
          </NavLink>
        )}
      </nav>
    </aside>
  );
};

export default Sidebar;