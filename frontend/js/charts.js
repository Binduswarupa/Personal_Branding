/**
 * ============================================
 * Charts Module (Chart.js)
 * LinkedIn Branding Assistant
 * ============================================
 */

function getChartColors() {
    const theme = document.documentElement.getAttribute('data-theme');
    const isDark = theme === 'dark';
    return {
        text: isDark ? '#F1F5F9' : '#0F172A',
        grid: isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)',
        primary: '#0A66C2',
        accent: '#38BDF8',
        success: '#22C55E',
        warning: '#F59E0B',
        danger: '#EF4444',
        bgPrimary: 'rgba(10,102,194,0.2)',
        bgAccent: 'rgba(56,189,248,0.2)'
    };
}

// ── Radar Chart ─────────────────────────────

function initRadarChart(labels, values) {
    const ctx = document.getElementById('radarChart');
    if (!ctx) return;

    // Destroy existing chart
    if (window._radarChart) window._radarChart.destroy();

    const colors = getChartColors();

    window._radarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels.map(l => l.charAt(0).toUpperCase() + l.slice(1)),
            datasets: [{
                label: 'Your Score',
                data: values,
                backgroundColor: colors.bgPrimary,
                borderColor: colors.primary,
                borderWidth: 2,
                pointBackgroundColor: colors.primary,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20,
                        color: colors.text,
                        backdropColor: 'transparent',
                        font: { size: 10 }
                    },
                    grid: { color: colors.grid },
                    pointLabels: {
                        color: colors.text,
                        font: { size: 11, weight: '600' }
                    }
                }
            },
            plugins: {
                legend: {
                    labels: { color: colors.text, font: { size: 12 } }
                }
            }
        }
    });
}

// ── Doughnut Chart ──────────────────────────

function initDoughnutChart(elementId, value, label) {
    const ctx = document.getElementById(elementId);
    if (!ctx) return;

    const colors = getChartColors();
    const color = value >= 70 ? colors.success : value >= 40 ? colors.warning : colors.danger;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: [label, 'Remaining'],
            datasets: [{
                data: [value, 100 - value],
                backgroundColor: [color, colors.grid],
                borderWidth: 0,
                cutout: '78%'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            }
        }
    });
}

// ── Bar Chart ───────────────────────────────

function initBarChart(elementId, labels, values) {
    const ctx = document.getElementById(elementId);
    if (!ctx) return;

    const colors = getChartColors();

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Score',
                data: values,
                backgroundColor: [
                    colors.bgPrimary, colors.bgAccent,
                    'rgba(34,197,94,0.2)', 'rgba(245,158,11,0.2)',
                    'rgba(239,68,68,0.2)'
                ],
                borderColor: [
                    colors.primary, colors.accent,
                    colors.success, colors.warning, colors.danger
                ],
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true, max: 100,
                    ticks: { color: colors.text },
                    grid: { color: colors.grid }
                },
                x: {
                    ticks: { color: colors.text },
                    grid: { display: false }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}
