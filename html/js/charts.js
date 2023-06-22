function get_color_palette() {
    return ['rgb(89,13,34)', 'rgb(128,15,47)', 'rgb(164,19,60)', 'rgb(201,24,74)',
        'rgb(255,77,109)', 'rgb(255,117,143)'
    ]
}

function print_doughnut_chart(id, title, labels, ds) {
    const ctx = document.getElementById(id);
    ctx.style.backgroundColor = 'rgba(255,255,255,255)';

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                    data: ds,
                    backgroundColor: get_color_palette()
                }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                },
                colorschemes: {
                    scheme: 'brewer.YlOrRd9'
                },
                title: {
                    display: true,
                    text: title
                }
            }
        },
    });
}

function getOptionsStackedBarChart(title) {
    return  {
        indexAxis: 'y',
        plugins: {
            title: {
                display: true,
                text: title
            },
        },
        responsive: true,
        scales: {
            x: {
                stacked: true,
            },
            y: {
                stacked: true
            }
        }
    }
}

function printStackedBarChart(id, title, axis_labels, labels, values) {
    const ctx = document.getElementById(id);
    ctx.style.backgroundColor = 'rgba(255,255,255,255)';

    ds = [];

    ds.push({
        label: labels[0],
        data: values[0],
        borderWidth: 1
    })

    ds.push({
        label: labels[1],
        data: values[1],
        borderWidth: 1
    })

    printChart(id, axis_labels, ds, getOptionsStackedBarChart(title));
}

function printBarChart(id, title, labels, values) {
    ds = [];
    ds.push({
        label: title,
        data: values,
        borderWidth: 1
    })

    printChart(id, labels, ds);
}

function getDefaultOptions() {
    return {
        indexAxis: 'y',
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
}

function printChart(id, labels, ds, opts = null) {
    const ctx = document.getElementById(id);
    ctx.style.backgroundColor = 'rgba(255,255,255,255)';

    if (opts === null) {
        opts = getDefaultOptions();
    }

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: ds
        },
        options: opts
    });
}