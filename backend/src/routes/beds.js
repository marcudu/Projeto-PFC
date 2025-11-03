const express = require('express');
const router = express.Router();
const { Bed, Patient } = require('../models');

router.get('/', async (req, res) => {
  const beds = await Bed.findAll({ include: [{ model: Patient, as: 'occupiedBy' }]});
  res.json(beds);
});

router.post('/', async (req, res) => {
  const { ward, number, notes } = req.body;
  const bed = await Bed.create({ ward, number, notes });
  res.status(201).json(bed);
});

router.put('/:id', async (req, res) => {
  const id = req.params.id;
  const bed = await Bed.findByPk(id);
  if (!bed) return res.status(404).send('Not found');
  await bed.update(req.body);
  res.json(bed);
});

// ocupar leito (vincular paciente)
router.post('/:id/occupy', async (req, res) => {
  const bed = await Bed.findByPk(req.params.id);
  if (!bed) return res.status(404).send('Bed not found');
  if (bed.status === 'occupied') return res.status(400).send('Bed already occupied');
  const { name, age } = req.body;
  const patient = await Patient.create({ name, age });
  await bed.update({ status: 'occupied', patientId: patient.id });
  res.json({ bed, patient });
});

// liberar leito
router.post('/:id/release', async (req, res) => {
  const bed = await Bed.findByPk(req.params.id);
  if (!bed) return res.status(404).send('Bed not found');
  if (bed.status !== 'occupied') return res.status(400).send('Bed not occupied');
  const patient = await Patient.findByPk(bed.patientId);
  await bed.update({ status: 'available', patientId: null });
  if (patient) await patient.destroy();
  res.json({ bed });
});

module.exports = router;
