const grafanaPort = 3000;
const dashboardPath = 'd-solo/degeyfhf3uqdcb/statistiche?orgId=1&from=1742584046229&to=1742605646229&timezone=browser&refresh=5s&panelId=2&__feature.dashboardSceneSolo';
const primoGrafanaUrl = `http://${SERVER_IP}:${grafanaPort}/${dashboardPath}`;

document.getElementById("primoIframe").src = primoGrafanaUrl;

const secondoDashboardPath = 'd-solo/degeyfhf3uqdcb/statistiche?orgId=1&from=1742531672738&to=1742553272738&timezone=browser&refresh=5s&panelId=1&__feature.dashboardSceneSolo';
const secondoGrafanaUrl = `http://${SERVER_IP}:${grafanaPort}/${secondoDashboardPath}`;

document.getElementById("secondoIframe").src = secondoGrafanaUrl;

const terzoDashboardPath = 'd-solo/degeyfhf3uqdcb/statistiche?orgId=1&from=1742803884741&to=1742825484741&timezone=browser&refresh=5s&panelId=3&__feature.dashboardSceneSolo'
const terzoGrafanaUrl = `http://${SERVER_IP}:${grafanaPort}/${terzoDashboardPath}`;

document.getElementById("terzoIframe").src = terzoGrafanaUrl;

// const quartoDashBoardPath = 'd-solo/degeyfhf3uqdcb/statistiche?orgId=1&from=1742803949065&to=1742825549065&timezone=browser&refresh=5s&panelId=4&__feature.dashboardSceneSolo'
// const quartoGrafanaUrl = `http://${SERVER_IP}:${grafanaPort}/${quartoDashBoardPath}`;
// document.getElementById("quartoIframe").src = quartoGrafanaUrl;
