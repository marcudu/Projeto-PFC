// src/api/api.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:4000", // endereço do seu backend
});

export default api;
