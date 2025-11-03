const { DataTypes } = require('sequelize');

module.exports = (sequelize) => {
  return sequelize.define('Bed', {
    id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
    ward: { type: DataTypes.STRING, allowNull: false }, // ex: "Enfermaria A"
    number: { type: DataTypes.STRING, allowNull: false }, // ex: "A-101"
    status: { type: DataTypes.ENUM('available','occupied','maintenance'), defaultValue: 'available' },
    notes: { type: DataTypes.TEXT, allowNull: true }
  }, {
    tableName: 'beds'
  });
};
