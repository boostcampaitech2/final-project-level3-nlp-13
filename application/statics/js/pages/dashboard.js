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

var areaOptions = {
	series: [
	  {
		name: "긍정",
		data: [31, 40, 28, 51, 42, 109, 100],
	  },
	  {
		name: "부정",
		data: [11, 32, 45, 32, 34, 52, 41],
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
	xaxis: {
	  type: "datetime",
	  categories: [
		"2018-09-19T00:00:00.000Z",
		"2018-09-19T01:30:00.000Z",
		"2018-09-19T02:30:00.000Z",
		"2018-09-19T03:30:00.000Z",
		"2018-09-19T04:30:00.000Z",
		"2018-09-19T05:30:00.000Z",
		"2018-09-19T06:30:00.000Z",
	  ],
	},
	tooltip: {
	  x: {
		format: "dd/MM/yy HH:mm",
	  },
	},
  };
 
var area = new ApexCharts(document.querySelector("#area"), areaOptions);
var chartVisitorsProfile = new ApexCharts(document.getElementById('chart-visitors-profile'), optionsVisitorsProfile)

area.render();
chartVisitorsProfile.render()