import { useEffect, useState } from 'react';
import { useAuthState } from 'react-firebase-hooks/auth';
import { auth } from '../firebase';

function UserDashboard() {
  const [user] = useAuthState(auth);
  const [notes, setNotes] = useState([]);
  
  useEffect(() => {
    // Here you would normally fetch user's notes from Firestore
    // For this example, we'll just use mock data
    if (user) {
      setNotes([
        { id: 1, title: 'Introduction to Physics', date: '2025-03-01' },
        { id: 2, title: 'Advanced Mathematics', date: '2025-03-03' },
        { id: 3, title: 'Biology Concepts', date: '2025-03-05' }
      ]);
    }
  }, [user]);
  
  if (!user) return null;
  
  return (
    <section className="dashboard-section">
      <div className="dashboard-header">
        <h2>Welcome, {user.displayName}!</h2>
        <p>Your learning journey continues here.</p>
      </div>
      
      <div className="dashboard-content">
        <div className="recent-notes">
          <h3>Recent Notes</h3>
          {notes.length > 0 ? (
            <ul className="notes-list">
              {notes.map(note => (
                <li key={note.id} className="note-item">
                  <span className="note-title">{note.title}</span>
                  <span className="note-date">{note.date}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="no-notes">You haven't created any notes yet.</p>
          )}
          
          <button className="create-note-btn">
            Create New Note
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 1V15M1 8H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            </svg>
          </button>
        </div>
      </div>
    </section>
  );
}

export default UserDashboard;