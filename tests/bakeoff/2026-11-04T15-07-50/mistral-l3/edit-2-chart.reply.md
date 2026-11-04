I'll add a bar chart showing the number of recommendations and observations per year to the Overview tab. This will be FIG.03, placed after the existing timeline chart.

```edit
<<<<<<< SEARCH
    <div class="figure">
      <div class="figure-title">FIG.02</div>
      <h2 class="figure-subtitle">Records per year by mechanism</h2>
      <div class="chart-container">
        <canvas id="timeline-chart"></canvas>
      </div>
      <p class="figure-source">Source: computed from the filtered set. Empty years are gaps in the data.</p>
    </div>
=======
    <div class="figure">
      <div class="figure-title">FIG.02</div>
      <h2 class="figure-subtitle">Records per year by mechanism</h2>
      <div class="chart-container">
        <canvas id="timeline-chart"></canvas>
      </div>
      <p class="figure-source">Source: computed from the filtered set. Empty years are gaps in the data.</p>
    </div>

    <div class="figure">
      <div class="figure-title">FIG.03</div>
      <h2 class="figure-subtitle">Recommendations and observations per year</h2>
      <div class="chart-container">
        <canvas id="type-chart"></canvas>
      </div>
      <p class="figure-source">Source: computed from the filtered set. Empty years are gaps in the data.</p>
    </div>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
      // Timeline chart
      const years = [...new Set(records.map(r => r.year))].sort((a, b) => a - b);
      const mechanisms = ['Universal Periodic Review', 'Treaty bodies', 'Special Procedures'];
      const timelineData = {};
      mechanisms.forEach(m => {
        timelineData[m] = {};
        years.forEach(y => {
          timelineData[m][y] = 0;
        });
      });
      filteredRecords.forEach(r => {
        timelineData[r.mechanism][r.year]++;
      });

      const datasets = mechanisms.map(m => ({
        label: m,
        data: years.map(y => timelineData[m][y]),
        backgroundColor: m === 'Universal Periodic Review' ? '#c2410c' : m === 'Treaty bodies' ? '#0f766e' : '#7c3aed'
      }));

      if (timelineChart) timelineChart.destroy();
      timelineChart = new Chart(timelineChartCanvas, {
        type: 'bar',
        data: {
          labels: years,
          datasets: datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: context => `${context.dataset.label}: ${context.raw} records`
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
              title: { display: true, text: 'Records' },
              ticks: {
                callback: value => value.toLocaleString()
              }
            }
          }
        }
      });
=======
      // Timeline chart
      const years = [...new Set(records.map(r => r.year))].sort((a, b) => a - b);
      const mechanisms = ['Universal Periodic Review', 'Treaty bodies', 'Special Procedures'];
      const timelineData = {};
      mechanisms.forEach(m => {
        timelineData[m] = {};
        years.forEach(y => {
          timelineData[m][y] = 0;
        });
      });
      filteredRecords.forEach(r => {
        timelineData[r.mechanism][r.year]++;
      });

      const datasets = mechanisms.map(m => ({
        label: m,
        data: years.map(y => timelineData[m][y]),
        backgroundColor: m === 'Universal Periodic Review' ? '#c2410c' : m === 'Treaty bodies' ? '#0f766e' : '#7c3aed'
      }));

      if (timelineChart) timelineChart.destroy();
      timelineChart = new Chart(timelineChartCanvas, {
        type: 'bar',
        data: {
          labels: years,
          datasets: datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: context => `${context.dataset.label}: ${context.raw} records`
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
              title: { display: true, text: 'Records' },
              ticks: {
                callback: value => value.toLocaleString()
              }
            }
          }
        }
      });

      // Type chart (recommendations vs observations)
      const typeChartCanvas = document.getElementById('type-chart');
      const typeData = {};
      ['Recommendations', 'Concerns/Observations', 'Other'].forEach(t => {
        typeData[t] = {};
        years.forEach(y => {
          typeData[t][y] = 0;
        });
      });
      filteredRecords.forEach(r => {
        typeData[r.type][r.year]++;
      });

      const typeDatasets = [
        {
          label: 'Recommendations',
          data: years.map(y => typeData['Recommendations'][y]),
          backgroundColor: 'rgba(155, 35, 53, 0.8)',
          borderColor: 'rgba(155, 35, 53, 1)',
          borderWidth: 1
        },
        {
          label: 'Concerns/Observations',
          data: years.map(y => typeData['Concerns/Observations'][y]),
          backgroundColor: 'rgba(100, 100, 100, 0.8)',
          borderColor: 'rgba(100, 100, 100, 1)',
          borderWidth: 1
        },
        {
          label: 'Other',
          data: years.map(y => typeData['Other'][y]),
          backgroundColor: 'rgba(200, 200, 200, 0.8)',
          borderColor: 'rgba(200, 200, 200, 1)',
          borderWidth: 1
        }
      ];

      if (window.typeChart) window.typeChart.destroy();
      window.typeChart = new Chart(typeChartCanvas, {
        type: 'bar',
        data: {
          labels: years,
          datasets: typeDatasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                usePointStyle: true,
                padding: 20
              }
            },
            tooltip: {
              callbacks: {
                label: context => `${context.dataset.label}: ${context.raw} records`
              }
            }
          },
          scales: {
            x: {
              title: { display: true, text: 'Year' }
            },
            y: {
              title: { display: true, text: 'Records' },
              ticks: {
                callback: value => value.toLocaleString()
              }
            }
          }
        }
      });
>>>>>>> REPLACE
```