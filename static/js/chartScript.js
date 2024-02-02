function createChart(canvas, type, data, options){
    if (options) {
        new Chart(
            document.getElementById(canvas),
            {
                type: type,
                data: data,
                options: options
            }
        );
    }
    else {
        new Chart(
            document.getElementById(canvas),
            {
                type: type,
                data: data
            }
        );
    }
}

