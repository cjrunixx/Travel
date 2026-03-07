import { FormEvent, useCallback, useMemo, useState } from "react";
import { login, register } from "./api/authApi";
import { TripPlannerPage } from "./pages/TripPlanner";
import { TripResultsPage } from "./pages/TripResults";
import type { TripPlanRequest, TripPlanResponse } from "./api/tripApi";
import { planTrip } from "./api/tripApi";

function AuthForm({ onAuth }: { onAuth: (token: string) => void }) {
  const [isRegister, setIsRegister] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const result = isRegister
        ? await register({ name, email, password })
        : await login({ email, password });
      onAuth(result.access_token);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Auth failed");
    } finally {
      setLoading(false);
    }
  };

  const switchMode = () => { setIsRegister(!isRegister); setError(null); };

  return (
    <div className="auth-wrap animate-in">
      <div className="auth-card">
        <h2>{isRegister ? "Create Account" : "Welcome Back"}</h2>
        <p className="auth-sub">
          {isRegister ? "Start planning your next adventure." : "Sign in to access your travel plans."}
        </p>

        <form className="form-grid" onSubmit={handleSubmit}>
          {isRegister && (
            <div className="field">
              <label className="field-label">Full Name</label>
              <input
                id="name"
                value={name}
                placeholder="John Doe"
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
          )}
          <div className="field">
            <label className="field-label">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              placeholder="you@example.com"
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="field">
            <label className="field-label">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              placeholder="••••••••"
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && (
            <div className="error-box">
              <span>⚠</span> {error}
            </div>
          )}

          <button
            id="auth-submit"
            type="submit"
            className="btn btn-primary btn-full"
            disabled={loading}
            style={{ marginTop: 4 }}
          >
            {loading ? (
              <><div className="spinner" /> Please wait...</>
            ) : (
              isRegister ? "Create Account →" : "Sign In →"
            )}
          </button>
        </form>

        <div className="divider" />

        <p style={{ textAlign: "center", fontSize: 14, color: "var(--text-3)" }}>
          {isRegister ? "Already have an account?" : "Don't have an account?"}{" "}
          <button type="button" className="btn-link" onClick={switchMode}>
            {isRegister ? "Sign in" : "Register"}
          </button>
        </p>
      </div>
    </div>
  );
}

export default function App() {
  const [token, setToken] = useState<string | null>(() => sessionStorage.getItem("token"));
  const [tripResult, setTripResult] = useState<TripPlanResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const hasResults = useMemo(() => tripResult !== null, [tripResult]);

  const handleAuth = useCallback((newToken: string) => {
    sessionStorage.setItem("token", newToken);
    setToken(newToken);
  }, []);

  const handleLogout = useCallback(() => {
    sessionStorage.removeItem("token");
    setToken(null);
    setTripResult(null);
    setError(null);
  }, []);

  const handlePlanTrip = async (payload: TripPlanRequest) => {
    if (!token) return;
    setLoading(true);
    setError(null);
    setTripResult(null);
    try {
      const response = await planTrip(payload, token);
      setTripResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to plan trip");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="app-shell">
      <header className="app-header">
        <div className="header-brand">
          <h1>✈ Travel Planner</h1>
          <div className="header-tagline">
            <span>🏙 Cities</span>
            <span>🚆 Transport</span>
            <span>🏨 Hotels</span>
            <span>🎡 Attractions</span>
          </div>
        </div>
        {token && (
          <button id="logout-btn" className="btn btn-ghost" onClick={handleLogout}>
            Sign Out
          </button>
        )}
      </header>

      {!token ? (
        <AuthForm onAuth={handleAuth} />
      ) : (
        <>
          <TripPlannerPage onSubmit={handlePlanTrip} loading={loading} />
          {error && (
            <div className="error-box animate-in" style={{ marginBottom: 16 }}>
              <span>⚠</span> {error}
            </div>
          )}
          {loading && !hasResults && (
            <div className="card loading-overlay animate-in">
              <div className="spinner spinner-lg" style={{ width: 40, height: 40, borderWidth: 3 }} />
              <p>Planning your perfect trip…</p>
            </div>
          )}
          {hasResults && tripResult && !loading && (
            <TripResultsPage result={tripResult} />
          )}
        </>
      )}
    </main>
  );
}
