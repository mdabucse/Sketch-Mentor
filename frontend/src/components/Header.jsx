import { useState, useEffect, useRef } from 'react';
import { useAuthState } from 'react-firebase-hooks/auth';
import { signInWithPopup, signOut } from 'firebase/auth';
import { auth, googleProvider } from '../firebase';
import { useNavigate } from 'react-router-dom';
import "../css/Header.css";

function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [user, loading, error] = useAuthState(auth);
  const [profileOpen, setProfileOpen] = useState(false);
  const initialRender = useRef(true);
  const navigate = useNavigate();

  useEffect(() => {
    console.log("User object:", user);
    if (error) {
      console.error("Firebase Auth Error:", error);
    }
  }, [user, error]);

  const handleLogin = async () => {
    try {
      await signInWithPopup(auth, googleProvider);
      navigate('/sketch-mentor');
    } catch (err) {
      console.error("Error signing in with Google", err);
    }
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
      navigate('/');
    } catch (err) {
      console.error("Error signing out", err);
    }
  };

  const toggleProfile = () => {
    setProfileOpen((prev) => !prev);
  };

  useEffect(() => {
    if (initialRender.current) {
      initialRender.current = false;
      return;
    }

    const handleClickOutside = (event) => {
      if (
        profileOpen &&
        !event.target.closest('.profile-popup') &&
        !event.target.closest('.profile')
      ) {
        setProfileOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [profileOpen]);

  const getAvatarLetter = () => {
    return user?.displayName ? user.displayName.charAt(0).toUpperCase() : '?';
  };

  return (
    <header className="header fixed-header">
      <div className="logo-container">
        <div className="logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 18L12 9L21 18" stroke="black" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            <path d="M3 14L12 5L21 14" stroke="black" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <span id='logo_name'>Sketch Mentor</span>
        </div>
      </div>

      <nav className="nav">
        <ul className="nav-items">
          {!user && <li><button onClick={handleLogin} className="login-btn">Login</button></li>}
        </ul>

        <div className="profile" onClick={toggleProfile}>
          {loading ? (
            <div className="loading-spinner">Loading...</div>
          ) : error ? (
            <div>Error</div>
          ) : user?.photoURL ? (
            <img
              src={user.photoURL}
              alt={user.displayName || 'Profile'}
              className="avatar"
              title={profileOpen ? 'Close profile' : 'Open profile'}
              onError={(e) => {
                console.error("Error loading image", e);
                e.target.src = '/default-avatar.png';
                e.target.onerror = null;
              }}
            />
          ) : (
            <div className="avatar initial-avatar">{getAvatarLetter()}</div>
          )}
        </div>

        <button
          className={`mobile-menu-btn ${menuOpen ? 'active' : ''}`}
          onClick={() => setMenuOpen((prev) => !prev)}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>
      </nav>

      {menuOpen && (
        <div className="mobile-menu">
          <ul>
            <li><a href="#pricing">Pricing</a></li>
            <li><a href="#labs">Labs</a></li>
            {user ? (
              <li><button onClick={handleLogout} className="login-btn">Logout</button></li>
            ) : (
              <li><button onClick={handleLogin} className="login-btn">Login with Google</button></li>
            )}
            <li><a href="#enter">Enter</a></li>
          </ul>
        </div>
      )}

      {profileOpen && user && (
        <div className="profile-popup">
          <div className="profile-popup-content">
            <button className="close-popup" onClick={toggleProfile}>X</button>
            <h2>Profile Information</h2>
            {user.photoURL ? (
              <img
                src={user.photoURL}
                alt={user.displayName || 'Profile'}
                className="popup-avatar"
                onError={(e) => {
                  console.error("Error loading image", e);
                  e.target.src = '/default-avatar.png';
                  e.target.onerror = null;
                }}
              />
            ) : (
              <div className="popup-avatar initial-avatar">{getAvatarLetter()}</div>
            )}
            <p>Name: {user.displayName || 'N/A'}</p>
            <p>Email: {user.email || 'N/A'}</p>
            <button onClick={handleLogout} className="logout-btn">Logout</button>
          </div>
        </div>
      )}
    </header>
  );
}

export default Header;