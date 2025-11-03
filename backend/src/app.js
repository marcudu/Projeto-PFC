const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
const { sequelize } = require('./models');
const bedsRouter = require('./routes/beds');

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.use('/api/beds', bedsRouter);

app.get('/', (req,res)=> res.send('Hospital Bed Manager API'));

const PORT = process.env.PORT || 4000;

async function start() {
  // cria pasta data se não existir
  const fs = require('fs');
  const dataDir = path.join(__dirname, '..', 'data');
  if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir);

  await sequelize.sync(); // cria tabelas automaticamente
  app.listen(PORT, ()=> console.log(`API rodando em http://localhost:${PORT}`));
}

start();
