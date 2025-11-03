// src/screens/Patients.jsx
import { useEffect, useState } from "react";
import api from "../api/api";

export default function Patients() {
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    api.get("/patients")
      .then(response => setPatients(response.data))
      .catch(err => console.error("Erro ao buscar pacientes:", err));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>👥 Pacientes</h1>
      {patients.length === 0 ? (
        <p>Nenhum paciente cadastrado.</p>
      ) : (
        <table border="1" cellPadding="10">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>Leito</th>
            </tr>
          </thead>
          <tbody>
            {patients.map((p) => (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td>{p.name}</td>
                <td>{p.bedId}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
