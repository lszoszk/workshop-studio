I'll add a bar chart showing the number of recommendations and observations per year on the Overview tab. Here's the edit:

```edit
<<<<<<< SEARCH
    </div>

    <div class="figure">
      <h4>FIG.02 Records per year by mechanism</h4>
      <div class="chart-container">
        <canvas id="timeline-chart"></canvas>
      </div>
      <div class="chart-legend">
        <div class="chart-legend-item"><div class="chart-legend-dot" style="background: var(--upr);"></div> Universal Periodic Review</div>
        <div class="chart-legend-item"><div class="chart-legend-dot" style="background: var(--treaty);"></div> Treaty bodies</div>
        <div class="chart-legend-item"><div class="chart-legend-dot" style="background: var(--special);"></div> Special Procedures</div>
      </div>
      <div class="source">Source: records per year per mechanism in the current filter.</div>
    </div>
=======
    </div>

    <div class="figure">
      <h4>FIG.02 Recommendations and observations per year</h4>
      <div class="chart-container">
        <canvas id="type-chart"></canvas>
      </div>
      <div class="chart-legend">
        <div class="chart-legend-item"><div class="chart-legend-dot" style="background: rgba(155, 35, 53, 0.8);"></div> Recommendations</div>
        <div class="chart-legend-item"><div class="chart-legend-dot" style="background: rgba(155, 35, 53, 0.4);"></div> Concerns/Observations</div>
        <div class="chart-legend-item"><div class="chart-legend-dot" style="background: rgba(155, 35, 53, 0.2);"></div> Other</div>
      </div>
      <div class="source">Source: records per year per type in the current filter.</div>
    </div>

    <div class="figure">
      <h4>FIG.03 Records per year by mechanism</h4>
      <div class="chart-container">
        <canvas id="timeline-chart"></canvas>
      </div>
      <div class="chart-legend">
        <div class="chart-legend-item"><div class="chart-legend-dot" style="background: var(--upr);"></div> Universal Periodic Review</div>
        <div class="chart-legend-item"><div class="chart-legend-dot" style="background: var(--treaty);"></div> Treaty bodies</div>
        <div class="chart-legend-item"><div class="chart-legend-dot" style="background: var(--special);"></div> Special Procedures</div>
      </div>
      <div class="source">Source: records per year per mechanism in the current filter.</div>
    </div>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
  // Timeline chart
  const timelineData = {};
  const allYears = [...new Set(records.map(r => r.year))].sort((a, b) => a - b);
  allYears.forEach(year => {
    timelineData[year] = {
      'Universal Periodic Review': 0,
      'Treaty bodies': 0,
      'Special Procedures': 0
    };
  });
  filteredRecords.forEach(record => {
    timelineData[record.year][record.mechanism]++;
  });
  const timelineCtx = document.getElementById('timeline-chart').getContext('2d');
  if (window.timelineChart) window.timelineChart.destroy();
  window.timelineChart = new Chart(timelineCtx, {
    type: 'bar',
    data: {
      labels: allYears,
      datasets: [
        {
          label: 'Universal Periodic Review',
          data: allYears.map(year => timelineData[year]['Universal Periodic Review']),
          backgroundColor: 'rgba(194, 65, 12, 0.8)',
          borderWidth: 0
        },
        {
          label: 'Treaty bodies',
          data: allYears.map(year => timelineData[year]['Treaty bodies']),
          backgroundColor: 'rgba(15, 118, 110, 0.8)',
          borderWidth: 0
        },
        {
          label: 'Special Procedures',
          data: allYears.map(year => timelineData[year]['Special Procedures']),
          backgroundColor: 'rgba(124, 58, 237, 0.8)',
          borderWidth: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (context) => `${context.dataset.label}: ${context.parsed.y.toLocaleString()}`
          }
        }
      },
      scales: {
        x: {
          stacked: true,
          title: { display: true, text: 'Year' }
        },
        y: {
          stacked: true,
          title: { display: true, text: 'Records' }
        }
      }
    }
  });
=======
  // Type chart (recommendations and observations per year)
  const typeData = {};
  const allYears = [...new Set(records.map(r => r.year))].sort((a, b) => a - b);
  allYears.forEach(year => {
    typeData[year] = {
      'Recommendations': 0,
      'Concerns/Observations': 0,
      'Other': 0
    };
  });
  filteredRecords.forEach(record => {
    const type = record.type === 'Recommendations' ? 'Recommendations' :
                 record.type === 'Concerns/Observations' ? 'Concerns/Observations' : 'Other';
    typeData[record.year][type]++;
  });
  const typeCtx = document.getElementById('type-chart').getContext('2d');
  if (window.typeChart) window.typeChart.destroy();
  window.typeChart = new Chart(typeCtx, {
    type: 'bar',
    data: {
      labels: allYears,
      datasets: [
        {
          label: 'Recommendations',
          data: allYears.map(year => typeData[year]['Recommendations']),
          backgroundColor: 'rgba(155, 35, 53, 0.8)',
          borderWidth: 0
        },
        {
          label: 'Concerns/Observations',
          data: allYears.map(year => typeData[year]['Concerns/Observations']),
          backgroundColor: 'rgba(155, 35, 53, 0.4)',
          borderWidth: 0
        },
        {
          label: 'Other',
          data: allYears.map(year => typeData[year]['Other']),
          backgroundColor: 'rgba(155, 35, 53, 0.2)',
          borderWidth: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (context) => `${context.dataset.label}: ${context.parsed.y.toLocaleString()}`
          }
        }
      },
      scales: {
        x: {
          stacked: true,
          title: { display: true, text: 'Year' }
        },
        y: {
          stacked: true,
          title: { display: true, text: 'Records' }
        }
      }
    }
  });

  // Timeline chart
  const timelineData = {};
  allYears.forEach(year => {
    timelineData[year] = {
      'Universal Periodic Review': 0,
      'Treaty bodies': 0,
      'Special Procedures': 0
    };
  });
  filteredRecords.forEach(record => {
    timelineData[record.year][record.mechanism]++;
  });
  const timelineCtx = document.getElementById('timeline-chart').getContext('2d');
  if (window.timelineChart) window.timelineChart.destroy();
  window.timelineChart = new Chart(timelineCtx, {
    type: 'bar',
    data: {
      labels: allYears,
      datasets: [
        {
          label: 'Universal Periodic Review',
          data: allYears.map(year => timelineData[year]['Universal Periodic Review']),
          backgroundColor: 'rgba(194, 65, 12, 0.8)',
          borderWidth: 0
        },
        {
          label: 'Treaty bodies',
          data: allYears.map(year => timelineData[year]['Treaty bodies']),
          backgroundColor: 'rgba(15, 118, 110, 0.8)',
          borderWidth: 0
        },
        {
          label: 'Special Procedures',
          data: allYears.map(year => timelineData[year]['Special Procedures']),
          backgroundColor: 'rgba(124, 58, 237, 0.8)',
          borderWidth: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (context) => `${context.dataset.label}: ${context.parsed.y.toLocaleString()}`
          }
        }
      },
      scales: {
        x: {
          stacked: true,
          title: { display: true, text: 'Year' }
        },
        y: {
          stacked: true,
          title: { display: true, text: 'Records' }
        }
      }
    }
  });
>>>>>>> REPLACE
```