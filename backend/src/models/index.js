const { Sequelize } = require('sequelize');
const path = require('path');

const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: path.join(__dirname, '..', '..', 'data', 'hospital.sqlite'),
  logging: false
});

const Bed = require('./bed')(sequelize);
const Patient = require('./patient')(sequelize);

// Relações
Bed.belongsTo(Patient, { as: 'occupiedBy', foreignKey: 'patientId' });
Patient.hasOne(Bed, { foreignKey: 'patientId' });

module.exports = { sequelize, Bed, Patient };
