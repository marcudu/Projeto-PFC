const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  return sequelize.define('Patient', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    name: { type: DataTypes.STRING, allowNull: false },
    age: { type: DataTypes.INTEGER },
    admissionDate: { type: DataTypes.DATE, defaultValue: DataTypes.NOW }
  }, {
    tableName: 'patients'
  });
};
