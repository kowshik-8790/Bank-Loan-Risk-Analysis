// Bank Loan Risk Analysis Dashboard - Interactive Controller

const loanMetrics = {
  overall: {
    applications: 10000,
    approved: 9685,
    approvalRate: 96.85,
    funded: 190823500.0,
    collected: 168832347.37,
    defaultRate: 13.83,
    loss: 18190869.04
  },
  monthly: [
    { ym: "2023-Q1", funded: 13500000, defaultRate: 12.1 },
    { ym: "2023-Q2", funded: 14800000, defaultRate: 12.8 },
    { ym: "2023-Q3", funded: 15900000, defaultRate: 13.2 },
    { ym: "2023-Q4", funded: 18200000, defaultRate: 13.7 },
    { ym: "2024-Q1", funded: 14500000, defaultRate: 13.4 },
    { ym: "2024-Q2", funded: 16200000, defaultRate: 13.9 },
    { ym: "2024-Q3", funded: 17800000, defaultRate: 14.1 },
    { ym: "2024-Q4", funded: 20500000, defaultRate: 14.5 },
    { ym: "2025-Q1", funded: 16100000, defaultRate: 13.8 },
    { ym: "2025-Q2", funded: 17900000, defaultRate: 14.0 },
    { ym: "2025-Q3", funded: 19400000, defaultRate: 14.3 },
    { ym: "2025-Q4", funded: 22023500, defaultRate: 14.8 }
  ],
  quality: {
    labels: ["Good Loans (Fully Paid & Current)", "Bad Loans (Charged Off / Default)"],
    values: [164219500.0, 26604000.0]
  },
  grades: [
    { grade: "A", loans: 2213, funded: 43737500.0, rate: 7.40, fico: 798.8, defaults: 90, defaultRate: 4.07, loss: 928400.0, tier: "Prime" },
    { grade: "B", loans: 2998, funded: 58002500.0, rate: 11.56, fico: 730.2, defaults: 268, defaultRate: 8.94, loss: 3125600.0, tier: "Near-Prime" },
    { grade: "C", loans: 2432, funded: 48486000.0, rate: 15.57, fico: 685.3, defaults: 397, defaultRate: 16.32, loss: 5192300.0, tier: "Moderate" },
    { grade: "D", loans: 1354, funded: 27714000.0, rate: 19.54, fico: 650.8, defaults: 335, defaultRate: 24.74, loss: 4981400.0, tier: "Subprime" },
    { grade: "E", loans: 551, funded: 10363000.0, rate: 23.48, fico: 621.4, defaults: 191, defaultRate: 34.66, loss: 3124800.0, tier: "High Risk" },
    { grade: "F", loans: 137, funded: 2520500.0, rate: 27.70, fico: 599.2, defaults: 58, defaultRate: 42.34, loss: 838369.04, tier: "Critical Risk" }
  ]
};

let trendChart, qualityChart, gradeChart;

function initCharts() {
  // 1. Monthly Originations & Default Rate
  const ctxTrend = document.getElementById('monthlyTrendChart').getContext('2d');
  trendChart = new Chart(ctxTrend, {
    type: 'bar',
    data: {
      labels: loanMetrics.monthly.map(m => m.ym),
      datasets: [
        {
          label: 'Capital Funded ($)',
          data: loanMetrics.monthly.map(m => m.funded),
          backgroundColor: '#0B2545',
          borderRadius: 4,
          yAxisID: 'y'
        },
        {
          label: 'Default Rate %',
          data: loanMetrics.monthly.map(m => m.defaultRate),
          type: 'line',
          borderColor: '#EF4444',
          backgroundColor: '#EF4444',
          borderWidth: 3,
          tension: 0.3,
          pointRadius: 4,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { position: 'top', labels: { boxWidth: 12 } },
        tooltip: {
          callbacks: {
            label: function(ctx) {
              if (ctx.datasetIndex === 0) return 'Funded: $' + (ctx.raw / 1000000).toFixed(2) + 'M';
              return 'Default Rate: ' + ctx.raw.toFixed(2) + '%';
            }
          }
        }
      },
      scales: {
        y: {
          grid: { color: '#E2E8F0' },
          ticks: { callback: v => '$' + (v / 1000000).toFixed(0) + 'M' }
        },
        y1: {
          position: 'right',
          grid: { drawOnChartArea: false },
          ticks: { callback: v => v + '%' }
        }
      }
    }
  });

  // 2. Loan Quality Donut Chart
  const ctxQuality = document.getElementById('loanQualityDonutChart').getContext('2d');
  qualityChart = new Chart(ctxQuality, {
    type: 'doughnut',
    data: {
      labels: loanMetrics.quality.labels,
      datasets: [{
        data: loanMetrics.quality.values,
        backgroundColor: ['#10B981', '#EF4444'],
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 12 } },
        tooltip: {
          callbacks: {
            label: ctx => {
              const val = ctx.raw;
              const total = loanMetrics.quality.values.reduce((a, b) => a + b, 0);
              const pct = ((val / total) * 100).toFixed(1);
              return `${ctx.label}: $${(val / 1000000).toFixed(2)}M (${pct}%)`;
            }
          }
        }
      },
      cutout: '65%'
    }
  });

  // 3. Default Rate by Grade Chart
  const ctxGrade = document.getElementById('gradeDefaultChart').getContext('2d');
  gradeChart = new Chart(ctxGrade, {
    type: 'bar',
    data: {
      labels: loanMetrics.grades.map(g => 'Grade ' + g.grade),
      datasets: [{
        label: 'Default Rate (%)',
        data: loanMetrics.grades.map(g => g.defaultRate),
        backgroundColor: ['#10B981', '#0284C7', '#F59E0B', '#EA580C', '#DC2626', '#991B1B'],
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: ctx => `Default Rate: ${ctx.raw}%` } }
      },
      scales: {
        y: {
          grid: { color: '#E2E8F0' },
          ticks: { callback: v => v + '%' }
        }
      }
    }
  });
}

function renderTable() {
  const tbody = document.getElementById('gradeTableBody');
  tbody.innerHTML = '';

  loanMetrics.grades.forEach(g => {
    let tierClass = 'tier-moderate';
    if (g.tier === 'Prime' || g.tier === 'Near-Prime') tierClass = 'tier-prime';
    if (g.tier === 'Subprime') tierClass = 'tier-subprime';
    if (g.tier === 'High Risk' || g.tier === 'Critical Risk') tierClass = 'tier-critical';

    const row = document.createElement('tr');
    row.innerHTML = `
      <td><strong>Grade ${g.grade}</strong></td>
      <td>${g.loans.toLocaleString()}</td>
      <td>$${(g.funded / 1000000).toFixed(2)}M</td>
      <td>${g.rate.toFixed(2)}%</td>
      <td>${g.fico.toFixed(1)}</td>
      <td>${g.defaults.toLocaleString()}</td>
      <td><strong style="color: ${g.defaultRate > 20 ? '#DC2626' : '#0F172A'}">${g.defaultRate.toFixed(2)}%</strong></td>
      <td>$${(g.loss / 1000000).toFixed(2)}M</td>
      <td><span class="grade-pill ${tierClass}">${g.tier}</span></td>
    `;
    tbody.appendChild(row);
  });
}

function applyFilters() {
  const grade = document.getElementById('gradeFilter').value;
  const purpose = document.getElementById('purposeFilter').value;
  const term = document.getElementById('termFilter').value;

  let mult = 1.0;
  if (grade !== 'All') mult *= 0.28;
  if (purpose !== 'All') mult *= 0.35;
  if (term !== 'All') mult *= 0.50;

  const currentApps = Math.round(loanMetrics.overall.applications * mult);
  const currentFunded = loanMetrics.overall.funded * mult;
  const currentCollected = loanMetrics.overall.collected * mult;
  const currentLoss = loanMetrics.overall.loss * mult;

  document.getElementById('kpiApps').textContent = currentApps.toLocaleString();
  document.getElementById('kpiFunded').textContent = '$' + (currentFunded / 1000000).toFixed(2) + 'M';
  document.getElementById('kpiCollected').textContent = '$' + (currentCollected / 1000000).toFixed(2) + 'M';
  document.getElementById('kpiLoss').textContent = '$' + (currentLoss / 1000000).toFixed(2) + 'M';
}

function setupListeners() {
  document.getElementById('gradeFilter').addEventListener('change', applyFilters);
  document.getElementById('purposeFilter').addEventListener('change', applyFilters);
  document.getElementById('termFilter').addEventListener('change', applyFilters);

  document.getElementById('resetBtn').addEventListener('click', () => {
    document.getElementById('gradeFilter').value = 'All';
    document.getElementById('purposeFilter').value = 'All';
    document.getElementById('termFilter').value = 'All';
    applyFilters();
  });
}

window.addEventListener('DOMContentLoaded', () => {
  initCharts();
  renderTable();
  setupListeners();
});
