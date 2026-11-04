I added FIG.03 "Recommendations and observations per year" under FIG.02, a horizontal bar chart with two series (Recommendations, Observations/Other) ranked by total records per year. The chart shows every year from the first to the last, so empty years are visible gaps.

```edit
<<<<<<< SEARCH
    <div class="fig">
      <h3>FIG.02 Records per year by mechanism</h3>
      <div class="chart-container">
        <canvas id="timeline-chart"></canvas>
      </div>
      <div class="source">Source: year and mechanism fields in the data.</div>
    </div>
=======
    <div class="fig">
      <h3>FIG.02 Records per year by mechanism</h3>
      <div class="chart-container">
        <canvas id="timeline-chart"></canvas>
      </div>
      <div class="source">Source: year and mechanism fields in the data.</div>
    </div>

    <div class="fig">
      <h3>FIG.03 Recommendations and observations per year</h3>
      <div class="chart-container">
        <canvas id="type-chart"></canvas>
      </div>
      <div class="source">Source: year and type fields in the data.</div>
    </div>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    // Timeline
    if (window.timelineChart) window.timelineChart.destroy();
    const timelineCtx = timelineChartCanvas.getContext('2d');
=======
    // Timeline
    if (window.timelineChart) window.timelineChart.destroy();
    const timelineCtx = timelineChartCanvas.getContext('2d');

    // Type chart
    if (window.typeChart) window.typeChart.destroy();
    const typeCtx = document.getElementById('type-chart').getContext('2d');
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    window.timelineChart = new Chart(timelineCtx, {
      type: 'bar',
      data: {
        labels: timelineLabels,
        datasets: [
          {
            label: 'Universal Periodic Review',
            data: uprData,
            backgroundColor: '#c2410c',
            borderColor: '#c2410c',
            borderWidth: 1
          },
          {
            label: 'Treaty bodies',
            data: treatyData,
            backgroundColor: '#0f766e',
            borderColor: '#0f766e',
            borderWidth: 1
          },
          {
            label: 'Special Procedures',
            data: specialData,
            backgroundColor: '#7c3aed',
            borderColor: '#7c3aed',
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: (context) => `${context.dataset.label}: ${context.raw.toLocaleString()} records`
            }
          }
        },
        scales: {
          x: { stacked: true },
          y: {
            stacked: true,
            beginAtZero: true,
            ticks: {
              callback: (value) => value.toLocaleString()
            }
          }
        }
      }
    });
=======
    window.timelineChart = new Chart(timelineCtx, {
      type: 'bar',
      data: {
        labels: timelineLabels,
        datasets: [
          {
            label: 'Universal Periodic Review',
            data: uprData,
            backgroundColor: '#c2410c',
            borderColor: '#c2410c',
            borderWidth: 1
          },
          {
            label: 'Treaty bodies',
            data: treatyData,
            backgroundColor: '#0f766e',
            borderColor: '#0f766e',
            borderWidth: 1
          },
          {
            label: 'Special Procedures',
            data: specialData,
            backgroundColor: '#7c3aed',
            borderColor: '#7c3aed',
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: (context) => `${context.dataset.label}: ${context.raw.toLocaleString()} records`
            }
          }
        },
        scales: {
          x: { stacked: true },
          y: {
            stacked: true,
            beginAtZero: true,
            ticks: {
              callback: (value) => value.toLocaleString()
            }
          }
        }
      }
    });

    // Type chart
    const typeData = {};
    filteredRecords.forEach(r => {
      if (!typeData[r.year]) typeData[r.year] = { Recommendations: 0, 'Observations/Other': 0 };
      if (r.type === 'Recommendations') {
        typeData[r.year].Recommendations++;
      } else {
        typeData[r.year]['Observations/Other']++;
      }
    });
    const typeLabels = years;
    const recData = [];
    const obsData = [];
    typeLabels.forEach(year => {
      recData.push(typeData[year]?.Recommendations || 0);
      obsData.push(typeData[year]?.['Observations/Other'] || 0);
    });
    const typeTotals = typeLabels.map((year, i) => recData[i] + obsData[i]);
    const typeRanking = typeLabels.map((year, i) => ({ year, total: typeTotals[i] }))
      .sort((a, b) => b.total - a.total || a.year - b.year)
      .map(item => item.year);
    const sortedRecData = typeRanking.map(year => recData[typeLabels.indexOf(year)]);
    const sortedObsData = typeRanking.map(year => obsData[typeLabels.indexOf(year)]);
    const sortedTypeLabels = typeRanking.map(year => year.toString());

    window.typeChart = new Chart(typeCtx, {
      type: 'bar',
      data: {
        labels: sortedTypeLabels,
        datasets: [
          {
            label: 'Recommendations',
            data: sortedRecData,
            backgroundColor: '#9b2335',
            borderColor: '#9b2335',
            borderWidth: 1
          },
          {
            label: 'Observations/Other',
            data: sortedObsData,
            backgroundColor: '#d9d2c3',
            borderColor: '#d9d2c3',
            borderWidth: 1
          }
        ]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: (context) => `${context.dataset.label}: ${context.raw.toLocaleString()} records`
            }
          }
        },
        scales: {
          x: {
            stacked: true,
            beginAtZero: true,
            ticks: {
              callback: (value) => value.toLocaleString()
            }
          },
          y: {
            stacked: true
          }
        }
      }
    });
>>>>>>> REPLACE
```