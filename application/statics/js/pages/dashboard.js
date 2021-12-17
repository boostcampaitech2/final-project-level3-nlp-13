let optionsVisitorsProfile  = {
	series: [70, 30],
	labels: ['긍정', '부정'],
	//colors: ['#435ebe','#55c6e8'],
	colors: ['#55c6e8', '#FFCDD2'],
	chart: {
		type: 'donut',
		width: '100%',
		height:'350px'
	},
	legend: {
		position: 'bottom'
	},
	plotOptions: {
		pie: {
			donut: {
				size: '30%'
			}
		}
	}
}

var areaOptions2 = {
	series: [
		{
			name: "긍정",
			data: [
				{x: 5, y: 100},
				{x: 10, y: 110},
				{x: 15, y: 140},
				{x: 20, y: 120},
				{x: 25, y: 90}
			],
		},
		{
			name: "부정",
			data: [
				{x: 5, y: 30},
				{x: 10, y: 20},
				{x: 15, y: 50},
				{x: 20, y: 20},
				{x: 25, y: 10}
			],
		},
	],
	chart: {
		height: 350,
		type: "area",
	},
	colors: ['#55c6e8', '#FFCDD2'],
	dataLabels: {
		enabled: false,
	},
	stroke: {
		curve: "smooth",
	},
	tooltip: {
			x: {
			format: "dd/MM/yy HH:mm",
		},
	},
	// xaxis: {
	// 	type: 'datetime'
	// }
};

var area = new ApexCharts(document.querySelector("#area"), areaOptions2);
var chartVisitorsProfile = new ApexCharts(document.getElementById('chart-visitors-profile'), optionsVisitorsProfile)

area.render();
chartVisitorsProfile.render()