let rawLoanData = [];
let purposeChart, riskGradeChart;

fetch('loans_data.json')
  .then(res => res.json())
  .then(data => {
    rawLoanData = data;
    initLoanDashboard();
  })
  .catch(err => {
    console.error('Error loading loan json:', err);
  });

function initLoanDashboard() {
  document.getElementById('statusSlicer').addEventListener('change', updateLoanDashboard);
  document.getElementById('riskSlicer').addEventListener('change', updateLoanDashboard);
  document.getElementById('purposeSlicer').addEventListener('change', updateLoanDashboard);

  updateLoanDashboard();
  updateCalc();
}

function updateLoanDashboard() {
  const statusFilter = document.getElementById('statusSlicer').value;
  const riskFilter = document.getElementById('riskSlicer').value;
  const purposeFilter = document.getElementById('purposeSlicer').value;

  const filtered = rawLoanData.filter(d => {
    const sMatch = statusFilter === 'All' || d.loan_status === statusFilter;
    const rMatch = riskFilter === 'All' || d.risk_grade === riskFilter;
    const pMatch = purposeFilter === 'All' || d.loan_purpose === purposeFilter;
    return sMatch && rMatch && pMatch;
  });

  // Calculate KPIs
  const totalApps = filtered.length;
  const approvedApps = filtered.filter(d => d.loan_status === 'Approved').length;
  const rejectedApps = totalApps - approvedApps;
  const appRate = totalApps > 0 ? (approvedApps / totalApps) * 100 : 0;
  const rejRate = totalApps > 0 ? (rejectedApps / totalApps) * 100 : 0;

  const totalLoanVal = filtered.reduce((a, b) => a + b.loan_amount, 0);
  const avgLoan = totalApps > 0 ? totalLoanVal / totalApps : 0;
  const avgInc = totalApps > 0 ? filtered.reduce((a, b) => a + b.applicant_income, 0) / totalApps : 0;

  document.getElementById('kpiApproval').innerText = `${appRate.toFixed(1)}%`;
  document.getElementById('kpiRejection').innerText = `${rejRate.toFixed(1)}%`;
  document.getElementById('kpiTotalVal').innerText = `$${(totalLoanVal / 1000000).toFixed(2)}M`;
  document.getElementById('kpiAvgLoan').innerText = `$${Math.round(avgLoan).toLocaleString()}`;
  document.getElementById('kpiAvgInc').innerText = `$${Math.round(avgInc).toLocaleString()}`;

  renderLoanCharts(filtered);
  renderLoanTable(filtered.slice(0, 15));
}

function renderLoanCharts(data) {
  // Loan purpose breakdown
  const purposeMap = {};
  data.forEach(d => {
    purposeMap[d.loan_purpose] = (purposeMap[d.loan_purpose] || 0) + 1;
  });

  if (purposeChart) purposeChart.destroy();
  const ctx1 = document.getElementById('purposeChart').getContext('2d');
  purposeChart = new Chart(ctx1, {
    type: 'bar',
    data: {
      labels: Object.keys(purposeMap),
      datasets: [{ label: 'Application Count', data: Object.values(purposeMap), backgroundColor: '#48cae4', borderRadius: 6 }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: '#90e0ef' } }, y: { ticks: { color: '#90e0ef' } } } }
  });

  // Risk grade breakdown
  const riskMap = { 'Grade A (Low Risk)': 0, 'Grade B (Moderate Risk)': 0, 'Grade C (Elevated Risk)': 0, 'Grade D/F (High Risk)': 0 };
  data.forEach(d => {
    if (riskMap[d.risk_grade] !== undefined) riskMap[d.risk_grade]++;
  });

  if (riskGradeChart) riskGradeChart.destroy();
  const ctx2 = document.getElementById('riskGradeChart').getContext('2d');
  riskGradeChart = new Chart(ctx2, {
    type: 'doughnut',
    data: {
      labels: Object.keys(riskMap),
      datasets: [{ data: Object.values(riskMap), backgroundColor: ['#06d6a0', '#48cae4', '#ffd166', '#ef476f'] }]
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: '#90e0ef' } } } }
  });
}

function renderLoanTable(sample) {
  const tbody = document.getElementById('loanTableBody');
  tbody.innerHTML = '';
  sample.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${row.application_id}</strong></td>
      <td>$${row.applicant_income.toLocaleString()}</td>
      <td>$${row.loan_amount.toLocaleString()}</td>
      <td>${row.credit_score}</td>
      <td>${row.dti_ratio}%</td>
      <td><span class="badge-app ${row.loan_status === 'Approved' ? 'badge-approved' : 'badge-rejected'}">${row.loan_status}</span></td>
      <td>${row.risk_grade}</td>
    `;
    tbody.appendChild(tr);
  });
}

function updateCalc() {
  const credit = parseInt(document.getElementById('iCredit').value);
  const dti = parseInt(document.getElementById('iDTI').value);

  const title = document.getElementById('calcGradeTitle');
  const rec = document.getElementById('calcRecommendation');

  if (credit >= 720 && dti < 25) {
    title.style.color = '#06d6a0';
    title.innerText = 'Grade A (Low Risk - Auto Approval)';
    rec.innerText = 'Prime applicant tier. Low probability of default (<1.2%). Qualified for lowest interest rate.';
  } else if (credit >= 660 && dti < 35) {
    title.style.color = '#48cae4';
    title.innerText = 'Grade B (Moderate Risk - Standard Approval)';
    rec.innerText = 'Standard underwriting tier. Meets regulatory DTI and FICO requirements.';
  } else if (credit >= 600 && dti < 42) {
    title.style.color = '#ffd166';
    title.innerText = 'Grade C (Elevated Risk - Review Required)';
    rec.innerText = 'Secondary collateral or co-signer required due to higher debt-to-income ratio.';
  } else {
    title.style.color = '#ef476f';
    title.innerText = 'Grade D/F (High Risk - Rejection Flag)';
    rec.innerText = 'High risk profile exceeding financial stress test limits. Recommended for rejection.';
  }
}
