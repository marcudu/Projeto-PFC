// src/components/Navbar.jsx
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav style={styles.nav}>
      <h2 style={styles.title}>Hospital Bed Manager</h2>
      <div style={styles.links}>
        <Link to="/" style={styles.link}>🏠 Início</Link>
        <Link to="/beds" style={styles.link}>🛏️ Leitos</Link>
        <Link to="/patients" style={styles.link}>👥 Pacientes</Link>
      </div>
    </nav>
  );
}

const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "10px 20px",
    backgroundColor: "#007bff",
    color: "white",
  },
  title: { margin: 0 },
  links: { display: "flex", gap: "15px" },
  link: { color: "white", textDecoration: "none", fontWeight: "bold" },
};
