import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyBbSWhxS-8S_bXKBo2krvKLLBMTXV_JYpo",
  authDomain: "ai-math-tutor-8a0b7.firebaseapp.com",
  projectId: "ai-math-tutor-8a0b7",
  storageBucket: "ai-math-tutor-8a0b7.appspot.com", // Fixed here
  messagingSenderId: "889171754251",
  appId: "1:889171754251:web:e31ab803afa3ab5e9bf60e",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

export { auth, googleProvider };
