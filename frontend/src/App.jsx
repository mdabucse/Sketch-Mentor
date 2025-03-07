import { useAuthState } from 'react-firebase-hooks/auth';
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import DeepTutorSection from './components/DeepTutorSection';
import UserDashboard from './components/UserDashboard';
import { auth } from './firebase';

function App() {
  const [user] = useAuthState(auth);
  
  return (
    <div className="app">
      <Header />
      <main>
        {user ? (
          <UserDashboard />
        ) : (
          <>
            <HeroSection />
            <DeepTutorSection />
          </>
        )}
      </main>
    </div>
  )
}

export default App