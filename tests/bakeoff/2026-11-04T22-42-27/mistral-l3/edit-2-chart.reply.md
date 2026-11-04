I'll add a bar chart showing the number of recommendations and observations per year on the Overview tab.

```edit
<<<<<<< SEARCH
      <div class="chart-container">
        <h3 class="chart-title"><span class="fig">FIG.02</span> Records per year by mechanism</h3>
        <div style="position: relative; height: 300px;">
          <canvas id="timeline-chart"></canvas>
        </div>
        <div class="chart-legend">
          <span><span class="dot upr"></span> UPR</span>
          <span><span class="dot treaty"></span> Treaty bodies</span>
          <span><span class="dot special"></span> Special Procedures</span>
        </div>
        <div class="chart-note">Source: <a id="timeline-chart-source">UN human rights recommendations and observations</a></div>
      </div>
=======
      <div class="chart-container">
        <h3 class="chart-title"><span class="fig">FIG.02</span> Recommendations and observations per year</h3>
        <div style="position: relative; height: 300px;">
          <canvas id="type-chart"></canvas>
        </div>
        <div class="chart-legend">
          <span><span class="dot" style="background-color: #9b2335;"></span> Recommendations</span>
          <span><span class="dot" style="background-color: #0f766e;"></span> Concerns/Observations</span>
          <span><span class="dot" style="background-color: #6b665e;"></span> Other</span>
        </div>
        <div class="chart-note">Source: <a id="type-chart-source">UN human rights recommendations and observations</a></div>
      </div>

      <div class="chart-container">
        <h3 class="chart-title"><span class="fig">FIG.03</span> Records per year by mechanism</h3>
        <div style="position: relative; height: 300px;">
          <canvas id="timeline-chart"></canvas>
        </div>
        <div class="chart-legend">
          <span><span class="dot upr"></span> UPR</span>
          <span><span class="dot treaty"></span> Treaty bodies</span>
          <span><span class="dot special"></span> Special Procedures</span>
        </div>
        <div class="chart-note">Source: <a id="timeline-chart-source">UN human rights recommendations and observations</a></div>
      </div>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    // Timeline chart
    const timelineData = {};
    const allYears = Array.from({ length: maxYear - minYear + 1 }, (_, i) => minYear + i);
    allYears.forEach(year => {
      timelineData[year] = { upr: 0, treaty: 0, special: 0 };
    });
    filtered.forEach(r => {
      const key = r.mechanism === 'Universal Periodic Review' ? 'upr' : r.mechanism === 'Treaty bodies' ? 'treaty' : 'special';
      timelineData[r.year][key]++;
    });

    const timelineChartCtx = document.getElementById('timeline-chart').getContext('2d');
    if (window.timelineChart) window.timelineChart.destroy();
    window.timelineChart = new Chart(timelineChartCtx, {
      type: 'bar',
      data: {
        labels: allYears.map(y => y.toString()),
        datasets: [
          {
            label: 'UPR',
            data: allYears.map(y => timelineData[y].upr),
            backgroundColor: '#c2410c'
          },
          {
            label: 'Treaty bodies',
            data: allYears.map(y => timelineData[y].treaty),
            backgroundColor: '#0f766e'
          },
          {
            label: 'Special Procedures',
            data: allYears.map(y => timelineData[y].special),
            backgroundColor: '#7c3aed'
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
              label: ctx => `${ctx.dataset.label}: ${ctx.raw.toLocaleString()}`
            }
          }
        },
        scales: {
          x: {
            stacked: true,
            grid: { display: false }
          },
          y: {
            stacked: true,
            beginAtZero: true,
            ticks: {
              callback: value => value.toLocaleString()
            }
          }
        }
      }
    });
=======
    // Type chart (recommendations/observations per year)
    const typeData = {};
    const allYears = Array.from({ length: maxYear - minYear + 1 }, (_, i) => minYear + i);
    allYears.forEach(year => {
      typeData[year] = { recommendations: 0, concerns: 0, other: 0 };
    });
    filtered.forEach(r => {
      if (r.type === 'Recommendations') {
        typeData[r.year].recommendations++;
      } else if (r.type === 'Concerns/Observations') {
        typeData[r.year].concerns++;
      } else {
        typeData[r.year].other++;
      }
    });

    const typeChartCtx = document.getElementById('type-chart').getContext('2d');
    if (window.typeChart) window.typeChart.destroy();
    window.typeChart = new Chart(typeChartCtx, {
      type: 'bar',
      data: {
        labels: allYears.map(y => y.toString()),
        datasets: [
          {
            label: 'Recommendations',
            data: allYears.map(y => typeData[y].recommendations),
            backgroundColor: '#9b2335'
          },
          {
            label: 'Concerns/Observations',
            data: allYears.map(y => typeData[y].concerns),
            backgroundColor: '#0f766e'
          },
          {
            label: 'Other',
            data: allYears.map(y => typeData[y].other),
            backgroundColor: '#6b665e'
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
              label: ctx => `${ctx.dataset.label}: ${ctx.raw.toLocaleString()}`
            }
          }
        },
        scales: {
          x: {
            grid: { display: false }
          },
          y: {
            beginAtZero: true,
            ticks: {
              callback: value => value.toLocaleString()
            }
          }
        }
      }
    });

    // Timeline chart (records per year by mechanism)
    const timelineData = {};
    allYears.forEach(year => {
      timelineData[year] = { upr: 0, treaty: 0, special: 0 };
    });
    filtered.forEach(r => {
      const key = r.mechanism === 'Universal Periodic Review' ? 'upr' : r.mechanism === 'Treaty bodies' ? 'treaty' : 'special';
      timelineData[r.year][key]++;
    });

    const timelineChartCtx = document.getElementById('timeline-chart').getContext('2d');
    if (window.timelineChart) window.timelineChart.destroy();
    window.timelineChart = new Chart(timelineChartCtx, {
      type: 'bar',
      data: {
        labels: allYears.map(y => y.toString()),
        datasets: [
          {
            label: 'UPR',
            data: allYears.map(y => timelineData[y].upr),
            backgroundColor: '#c2410c'
          },
          {
            label: 'Treaty bodies',
            data: allYears.map(y => timelineData[y].treaty),
            backgroundColor: '#0f766e'
          },
          {
            label: 'Special Procedures',
            data: allYears.map(y => timelineData[y].special),
            backgroundColor: '#7c3aed'
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
              label: ctx => `${ctx.dataset.label}: ${ctx.raw.toLocaleString()}`
            }
          }
        },
        scales: {
          x: {
            stacked: true,
            grid: { display: false }
          },
          y: {
            stacked: true,
            beginAtZero: true,
            ticks: {
              callback: value => value.toLocaleString()
            }
          }
        }
      }
    });
>>>>>>> REPLACE
```