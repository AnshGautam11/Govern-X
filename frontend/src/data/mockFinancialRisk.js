export const mockFinancialRisk = {
  confidenceLevel: 0.95,
  valueAtRisk: 12400000,
  expectedLoss: 4800000,
  maxLoss: 28700000,
  annualizedExposure: 9600000,
  totalAssetValue: 52300000,
  assetsAtRisk: 14,
  distribution: [6, 10, 18, 28, 42, 56, 48, 36, 24, 14],
  breakdown: [
    { category: 'Servers', value: 14200000, exposure: 31, risk: 3200000 },
    { category: 'Databases', value: 11800000, exposure: 22, risk: 2700000 },
    { category: 'Endpoints', value: 8600000, exposure: 18, risk: 1400000 },
    { category: 'Cloud resources', value: 15400000, exposure: 29, risk: 4100000 },
    { category: 'Applications', value: 2300000, exposure: 9, risk: 900000 },
  ],
};
