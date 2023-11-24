apiUrl = "/NCMetrics";
base = "https://landshark.name";
metricNameKey = "metricName";
startTimeKey = "startTime";
endTimeKey = "endTime";

const ctx = document.getElementById('metrics');
const chart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: []
        },
        options: {
            scales: {
                x: {
                    type: "time"
                }
            },
            animation: false,
            plugins: {
                legend: {
                    position: "bottom",
                    align: "end"
                },
                title: {
                    text: "NC Player Count",
                    display: true,
                    font: {
                        size: 50
                    }
                }
            }
        }
    });

function buildURL(metricName, startTime, endTime) {
    url = new URL(apiUrl, base);
    query = new URLSearchParams();
    query.append(metricNameKey, metricName);
    query.append(startTimeKey, startTime);
    query.append(endTimeKey, endTime);

    return url.toString() + "?" + query.toString();
}

async function makeRequest(url, config) {
    request = new Request(url)

    try {
        response = await fetch(request)
        if(response.status === 200) {
            updateChart(await response.json(), config);
        }
        else {
            console.log("error happened", response, response.text());
        }
    } catch (error) {
        console.log("error happened", error);
    }
}

function updateChart(response, config) {
    datapoints = response["data"].map(dp => {return {x: new Date(dp["time"]*1000), y:convertToNumber(dp["playerCount"])}});
    dataConfig = {
        label: config.date,
        data: datapoints
    }
    chart.data.datasets = [dataConfig]
	chart.update();
};

function convertToNumber(str) {
    const parsed = parseInt(str, 10);
    if (isNaN(parsed)) { return 0 };
    return parsed;
}

async function getDataHandler(metricName) {

    startTime = new Date(document.getElementById("date").value+"T00:00");
    config = {
        date: document.getElementById("date").value,
        metricName: metricName,
        startTime: startTime.getTime()/1000,
        endTime: startTime + 24*60*60
    }
    url = buildURL(metricName, config.startTime, config.endTime);
    await makeRequest(url, config);
}