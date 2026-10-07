"use strict";

const dashboardData = {
  source: "funnel_analysis_data.csv",
  stages: [
    { name: "Browse", count: 10000, overall: 100 },
    { name: "Add to Cart", count: 7059, overall: 70.59, transition: 70.59 },
    { name: "Checkout", count: 3524, overall: 35.24, transition: 49.92 },
    { name: "Purchase", count: 1080, overall: 10.8, transition: 30.65 },
  ],
  revenue: {
    total: 1176405.78,
    purchases: 1080,
    averageOrderValue: 1089.26,
  },
  segments: {
    device: [
      { name: "Tablet", browse: 3324, purchase: 383, conversion: 11.52 },
      { name: "Mobile", browse: 3345, purchase: 369, conversion: 11.03 },
      { name: "Desktop", browse: 3331, purchase: 328, conversion: 9.85 },
    ],
    channel: [
      { name: "Email", browse: 2489, purchase: 279, conversion: 11.21 },
      { name: "Google Ads", browse: 2560, purchase: 279, conversion: 10.9 },
      { name: "Social Media", browse: 2440, purchase: 265, conversion: 10.86 },
      { name: "Organic", browse: 2511, purchase: 257, conversion: 10.23 },
    ],
    category: [
      { name: "Electronics", browse: 2046, purchase: 229, conversion: 11.19 },
      { name: "Fashion", browse: 2035, purchase: 223, conversion: 10.96 },
      { name: "Home", browse: 1941, purchase: 212, conversion: 10.92 },
      { name: "Sports", browse: 2000, purchase: 215, conversion: 10.75 },
      { name: "Beauty", browse: 1978, purchase: 201, conversion: 10.16 },
    ],
  },
};

const numberFormat = new Intl.NumberFormat("en-US");
const currencyFormat = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});
const percentage = (value) => `${value.toFixed(2)}%`;
const getElement = (id) => document.getElementById(id);

function renderKpis() {
  const values = [
    { label: "Total Browse / Visitors", value: numberFormat.format(dashboardData.stages[0].count), detail: "Browse sessions", icon: "↗", tone: "blue" },
    { label: "Add to Cart", value: numberFormat.format(dashboardData.stages[1].count), detail: "sessions reached", icon: "+", tone: "teal" },
    { label: "Checkout", value: numberFormat.format(dashboardData.stages[2].count), detail: "sessions reached", icon: "↳", tone: "amber" },
    { label: "Purchases", value: numberFormat.format(dashboardData.revenue.purchases), detail: "purchase sessions", icon: "✓", tone: "coral" },
    { label: "Overall Conversion", value: percentage(dashboardData.stages[3].count / dashboardData.stages[0].count * 100), detail: "Browse to Purchase", icon: "%", tone: "navy" },
    { label: "Total Revenue", value: currencyFormat.format(dashboardData.revenue.total), detail: "purchase events", icon: "$", tone: "teal" },
    { label: "Average Order Value", value: currencyFormat.format(dashboardData.revenue.averageOrderValue), detail: "per purchase", icon: "Ø", tone: "blue" },
  ];

  getElement("kpis").innerHTML = values.map((item) => `
    <article class="kpi-card tone-${item.tone}">
      <div class="kpi-topline">
        <span class="kpi-label">${item.label}</span>
        <span class="kpi-icon" aria-hidden="true">${item.icon}</span>
      </div>
      <strong class="kpi-value">${item.value}</strong>
      <span class="kpi-detail">${item.detail}</span>
    </article>
  `).join("");
}

function renderFunnel() {
  const base = dashboardData.stages[0].count;
  const stageColors = ["#253e62", "#4778d0", "#14a89e", "#e3a33b"];
  getElement("funnel-visual").innerHTML = dashboardData.stages.map((stage, index) => `
    <div class="funnel-row">
      <span class="funnel-stage-label">${stage.name}</span>
      <div class="funnel-track">
        <div class="funnel-bar" style="width:${stage.count / base * 100}%;background:${stageColors[index]}">
          ${numberFormat.format(stage.count)}
        </div>
      </div>
      <span class="funnel-share">${percentage(stage.count / base * 100)}</span>
    </div>
  `).join("");

  const transitionNames = ["—", "Browse → Add to Cart", "Add to Cart → Checkout", "Checkout → Purchase"];
  getElement("funnel-table-body").innerHTML = dashboardData.stages.map((stage, index) => {
    const previous = dashboardData.stages[index - 1];
    const dropped = previous ? previous.count - stage.count : null;
    const droppedPercent = previous ? dropped / previous.count * 100 : null;
    return `
      <tr>
        <td class="stage-name-cell">${stage.name}</td>
        <td>${numberFormat.format(stage.count)}</td>
        <td>${index === 0 ? "—" : percentage(stage.transition)}</td>
        <td class="${previous ? "drop-cell" : ""}">${previous ? `${numberFormat.format(dropped)} · ${percentage(droppedPercent)}` : "—"}</td>
      </tr>
    `;
  }).join("");

  getElement("hero-conversion").textContent = percentage(
    dashboardData.stages[3].count / dashboardData.stages[0].count * 100,
  );
}

function renderBars(containerId, items, options = {}) {
  const max = options.max ?? Math.max(...items.map((item) => item.value));
  const tones = options.tones ?? ["", "teal", "amber", "coral", "navy"];
  const labelWidth = options.labelWidth;
  getElement(containerId).innerHTML = items.map((item, index) => {
    const fill = Math.min(100, item.value / max * 100);
    const label = labelWidth ? `${item.label}` : item.label;
    return `
      <div class="bar-row">
        <span class="bar-label" title="${label}">${label}</span>
        <div class="bar-track" role="img" aria-label="${label}: ${item.ariaValue ?? item.value}">
          <div class="bar-fill ${tones[index % tones.length]}" style="width:${fill}%"></div>
        </div>
        <span class="bar-value">${item.valueLabel ?? percentage(item.value)}</span>
      </div>
    `;
  }).join("");
}

function renderAnalysis() {
  const transitions = dashboardData.stages.slice(1).map((stage, index) => ({
    label: `${dashboardData.stages[index].name} → ${stage.name}`,
    value: stage.transition,
  }));
  renderBars("stage-conversion-chart", transitions, { max: 100 });

  const dropoffs = dashboardData.stages.slice(1).map((stage, index) => {
    const previous = dashboardData.stages[index];
    const count = previous.count - stage.count;
    const rate = count / previous.count * 100;
    return {
      label: `${previous.name} → ${stage.name}`,
      value: count,
      valueLabel: `${numberFormat.format(count)} · ${percentage(rate)}`,
      ariaValue: `${numberFormat.format(count)} sessions, ${percentage(rate)}`,
    };
  });
  renderBars("dropoff-chart", dropoffs, {
    max: Math.max(...dropoffs.map((item) => item.value)) * 1.12,
    tones: ["coral"],
  });

  const largestByCount = [...dropoffs].sort((a, b) => b.value - a.value)[0];
  const highestRate = dashboardData.stages.slice(1).reduce((highest, stage, index) => {
    const previous = dashboardData.stages[index];
    const lost = previous.count - stage.count;
    const rate = lost / previous.count * 100;
    return rate > highest.rate ? { label: `${previous.name} → ${stage.name}`, count: lost, rate } : highest;
  }, { rate: -1 });

  getElement("largest-loss").textContent = `${largestByCount.label}: ${numberFormat.format(largestByCount.value)} sessions`;
  getElement("highest-dropoff-rate").textContent = `${highestRate.label}: ${percentage(highestRate.rate)} (${numberFormat.format(highestRate.count)} sessions)`;

  const segmentConfigs = [
    ["device-chart", dashboardData.segments.device, ["", "teal", "amber"]],
    ["channel-chart", dashboardData.segments.channel, ["teal", "", "amber", "coral"]],
    ["category-chart", dashboardData.segments.category, ["amber", "", "teal", "coral", "navy"]],
  ];
  for (const [id, segments, tones] of segmentConfigs) {
    renderBars(id, segments.map((segment) => ({
      label: segment.name,
      value: segment.conversion,
      valueLabel: percentage(segment.conversion),
      ariaValue: `${percentage(segment.conversion)} conversion, ${numberFormat.format(segment.purchase)} purchases from ${numberFormat.format(segment.browse)} Browse sessions`,
    })), { max: 13, tones });
  }
}

function renderRevenue() {
  getElement("revenue-total").textContent = currencyFormat.format(dashboardData.revenue.total);
  getElement("revenue-purchases").textContent = numberFormat.format(dashboardData.revenue.purchases);
  getElement("revenue-aov").textContent = currencyFormat.format(dashboardData.revenue.averageOrderValue);
}

function renderInsights() {
  const best = (segments) => [...segments].sort((a, b) => b.conversion - a.conversion)[0];
  const device = best(dashboardData.segments.device);
  const channel = best(dashboardData.segments.channel);
  const category = best(dashboardData.segments.category);
  const dropoffs = dashboardData.stages.slice(1).map((stage, index) => {
    const previous = dashboardData.stages[index];
    return { name: `${previous.name} → ${stage.name}`, count: previous.count - stage.count };
  });
  const largestLoss = [...dropoffs].sort((a, b) => b.count - a.count)[0];
  const insights = [
    `<strong>${percentage(dashboardData.stages[3].count / dashboardData.stages[0].count * 100)}</strong> of Browse sessions reached Purchase.`,
    `The largest absolute loss is <strong>${numberFormat.format(largestLoss.count)} sessions</strong> from ${largestLoss.name}.`,
    `<strong>${device.name}</strong> leads device conversion at ${percentage(device.conversion)}; <strong>${channel.name}</strong> leads channel conversion at ${percentage(channel.conversion)}.`,
    `<strong>${category.name}</strong> has the highest product-category conversion at ${percentage(category.conversion)}.`,
  ];
  getElement("business-insights").innerHTML = insights.map((text) => `<li><span>${text}</span></li>`).join("");
}

renderKpis();
renderFunnel();
renderAnalysis();
renderRevenue();
renderInsights();
