const { sequelize, Bed } = require('./src/models');

async function seed() {
  await sequelize.sync({ force: true });
  await Bed.bulkCreate([
    { ward: 'Enfermaria A', number: 'A-101' },
    { ward: 'Enfermaria A', number: 'A-102' },
    { ward: 'UTI', number: 'U-01', status: 'maintenance' }
  ]);
  console.log('Seed done');
  process.exit(0);
}

seed();
