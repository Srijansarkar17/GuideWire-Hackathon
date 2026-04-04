import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Firebase Web Config — values come from frontend/.env (VITE_ prefixed)
// To get your values: Firebase Console → Project Settings → Your apps → Web app
const apiKey = import.meta.env.VITE_FIREBASE_API_KEY;
const messagingSenderId = import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID;
const appId = import.meta.env.VITE_FIREBASE_APP_ID;

const looksLikePlaceholder = (v) =>
  !v ||
  String(v).startsWith("your_") ||
  String(v).includes("_here");

if (
  looksLikePlaceholder(apiKey) ||
  looksLikePlaceholder(messagingSenderId) ||
  looksLikePlaceholder(appId)
) {
  console.error(
    "[Drizzle] Firebase web config is missing or still set to placeholders in frontend/.env.\n" +
      "Set VITE_FIREBASE_API_KEY, VITE_FIREBASE_MESSAGING_SENDER_ID, and VITE_FIREBASE_APP_ID " +
      "from Firebase Console → Project settings → Your apps → Web app (SDK snippet).\n" +
      "Then restart the Vite dev server."
  );
}

const firebaseConfig = {
  apiKey,
  authDomain:        import.meta.env.VITE_FIREBASE_AUTH_DOMAIN     || "drizzle-d76ee.firebaseapp.com",
  projectId:         import.meta.env.VITE_FIREBASE_PROJECT_ID      || "drizzle-d76ee",
  storageBucket:     import.meta.env.VITE_FIREBASE_STORAGE_BUCKET  || "drizzle-d76ee.firebasestorage.app",
  messagingSenderId,
  appId,
};

export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
