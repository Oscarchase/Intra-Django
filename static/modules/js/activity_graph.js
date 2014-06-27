google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);

function drawChart() {
    var data = google.visualization.arrayToDataTable([
        ['Task', 'Hours per Day'],
        ['Non registered', places - registered],
        ['Registered', registered],
    ]);

    var options = {
        backgroundColor: 'transparent',
        width: 350,
        height: 200,
        title: 'Registered student',
        colors: ['#c0010b', '#00acc0'],
        is3D: true
    };

    var chart = new google.visualization.PieChart($('#piechart')[0]);
    chart.draw(data, options);
}
