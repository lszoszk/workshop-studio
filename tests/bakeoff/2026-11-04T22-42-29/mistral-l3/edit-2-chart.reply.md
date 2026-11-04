I'll add a bar chart showing the number of recommendations and observations per year to the Overview tab. This will give a clear visual of how the volume has changed over time.

```edit
<<<<<<< SEARCH
      <figure class="figure">
        <figcaption class="figure-title">FIG.02 Records per year by mechanism</figcaption>
        <div class="figure-content">
          <div class="figure-chart">
            <canvas id="timeline-chart"></canvas>
          </div>
          <div class="timeline-legend">
            <div class="timeline-legend-item">
              <div class="timeline-legend-dot upr"></div>
              <span>Universal Periodic Review</span>
            </div>
            <div class="timeline-legend-item">
              <div class="timeline-legend-dot treaty-bodies"></div>
              <span>Treaty bodies</span>
            </div>
            <div class="timeline-legend-item">
              <div class="timeline-legend-dot special-procedures"></div>
              <span>Special Procedures</span>
            </div>
          </div>
        </div>
        <div class="figure-source">Source: Universal Human Rights Index</div>
      </figure>
=======
      <figure class="figure">
        <figcaption class="figure-title">FIG.02 Records per year</figcaption>
        <div class="figure-content">
          <div class="figure-chart">
            <canvas id="records-per-year-chart"></canvas>
          </div>
        </div>
        <div class="figure-source">Source: Universal Human Rights Index</div>
      </figure>

      <figure class="figure">
        <figcaption class="figure-title">FIG.03 Records per year by mechanism</figcaption>
        <div class="figure-content">
          <div class="figure-chart">
            <canvas id="timeline-chart"></canvas>
          </div>
          <div class="timeline-legend">
            <div class="timeline-legend-item">
              <div class="timeline-legend-dot upr"></div>
              <span>Universal Periodic Review</span>
            </div>
            <div class="timeline-legend-item">
              <div class="timeline-legend-dot treaty-bodies"></div>
              <span>Treaty bodies</span>
            </div>
            <div class="timeline-legend-item">
              <div class="timeline-legend-dot special-procedures"></div>
              <span>Special Procedures</span>
            </div>
          </div>
        </div>
        <div class="figure-source">Source: Universal Human Rights Index</div>
      </figure>
>>>>>>> REPLACE
```

```edit
<<<<<<< SEARCH
    function updateTimelineChart() {
      const years = Array.from({ length: yearMax - yearMin + 1 }, (_, i) => yearMin + i);
      const mechanisms = ['Universal Periodic Review', 'Treaty bodies', 'Special Procedures'];
      const counts = {};

      mechanisms.forEach(m => {
        counts[m] = {};
        years.forEach(y => counts[m][y] = 0);
      });

      filteredRecords.forEach(r => {
        counts[r.mechanism][r.year]++;
      });

      const datasets = mechanisms.map(m => ({
        label: m,
        data: years.map(y => counts[m][y]),
        backgroundColor: m === 'Universal Periodic Review' ? '#c2410c' : m === 'Treaty bodies' ? '#0f766e' : '#7c3aed'
      }));

      const ctx = document.getElementById('timeline-chart').getContext('2d');
      if (window.timelineChart) window.timelineChart.destroy();
      window.timelineChart = new Chart(ctx, {
        type: 'bar',
        data: { labels: years, datasets },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (context) => `${context.dataset.label}: ${context.parsed.y} records`
              }
            }
          },
          scales: {
            x: {
              stacked: true,
              ticks: { color: '#666' },
              grid: { color: '#eee' }
            },
            y: {
              stacked: true,
              beginAtZero: true,
              ticks: {
                color: '#666',
                callback: (value) => value.toLocaleString()
              },
              grid: { color: '#eee' }
            }
          }
        }
      });
    }

    function updateRecordsTable() {
=======
    function updateRecordsPerYearChart() {
      const years = Array.from({ length: yearMax - yearMin + 1 }, (_, i) => yearMin + i);
      const counts = {};

      years.forEach(y => counts[y] = 0);
      filteredRecords.forEach(r => counts[r.year]++);

      const ctx = document.getElementById('records-per-year-chart').getContext('2d');
      if (window.recordsPerYearChart) window.recordsPerYearChart.destroy();
      window.recordsPerYearChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: years,
          datasets: [{
            data: years.map(y => counts[y]),
            backgroundColor: '#9b2335',
            borderWidth: 0,
            borderRadius: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (context) => `${context.parsed.y} records`
              }
            }
          },
          scales: {
            x: {
              ticks: { color: '#666' },
              grid: { color: '#eee' }
            },
            y: {
              beginAtZero: true,
              ticks: {
                color: '#666',
                callback: (value) => value.toLocaleString()
              },
              grid: { color: '#eee' }
            }
          }
        }
      });
    }

    function updateTimelineChart() {
      const years = Array.from({ length: yearMax - yearMin + 1 }, (_, i) => yearMin + i);
      const mechanisms = ['Universal Periodic Review', 'Treaty bodies', 'Special Procedures'];
      const counts = {};

      mechanisms.forEach(m => {
        counts[m] = {};
        years.forEach(y => counts[m][y] = 0);
      });

      filteredRecords.forEach(r => {
        counts[r.mechanism][r.year]++;
      });

      const datasets = mechanisms.map(m => ({
        label: m,
        data: years.map(y => counts[m][y]),
        backgroundColor: m === 'Universal Periodic Review' ? '#c2410c' : m === 'Treaty bodies' ? '#0f766e' : '#7c3aed'
      }));

      const ctx = document.getElementById('timeline-chart').getContext('2d');
      if (window.timelineChart) window.timelineChart.destroy();
      window.timelineChart = new Chart(ctx, {
        type: 'bar',
        data: { labels: years, datasets },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: (context) => `${context.dataset.label}: ${context.parsed.y} records`
              }
            }
          },
          scales: {
            x: {
              stacked: true,
              ticks: { color: '#666' },
              grid: { color: '#eee' }
            },
            y: {
              stacked: true,
              beginAtZero: true,
              ticks: {
                color: '#666',
                callback: (value) => value.toLocaleString()
              },
              grid: { color: '#eee' }
            }
          }
        }
      });
    }

    function updateUI() {
      const matchingCount = filteredRecords.length;
      matchingCountEl.textContent = matchingCount;
      matchingBarEl.style.width = `${(matchingCount / totalCount) * 100}%`;

      updateFilterChips();
      updateHeadlineNumbers();
      updateThemeChart();
      updateRecordsPerYearChart();
      updateTimelineChart();
      updateRecordsTable();
      updateCheckPanel();
      updateSampleCards();
    }
>>>>>>> REPLACE
```