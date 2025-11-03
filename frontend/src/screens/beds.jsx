// src/screens/Beds.jsx
import { useEffect, useState } from "react";
import api from "../api/api";

export default function Beds() {
  const [beds, setBeds] = useState([]);

  useEffect(() => {
    api.get("/beds")
      .then(response => setBeds(response.data))
      .catch(err => console.error("Erro ao buscar leitos:", err));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>🛏️ Leitos Cadastrados</h1>
      {beds.length === 0 ? (
        <p>Nenhum leito cadastrado.</p>
      ) : (
        <table border="1" cellPadding="10">
          <thead>
            <tr>
              <th>ID</th>
              <th>Setor</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {beds.map((bed) => (
              <tr key={bed.id}>
                <td>{bed.id}</td>
                <td>{bed.sector}</td>
                <td>{bed.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
