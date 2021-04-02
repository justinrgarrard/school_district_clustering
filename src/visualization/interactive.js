margin = {top: 0, right: 0, bottom: 0, left: 0},
    width = 1200,
    height = 600;


var svg1 = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top +")");

promises = [d3.json("data/us.json"), d3.csv("data/csv_to_json2.csv")]

var projection = d3.geoAlbersUsa()
    .translate([width/2, height/2])
    .scale(1000)

var path = d3.geoPath().projection(projection)



Promise.all(promises).then(function(data) {


    console.log(data[0])
    console.log(data[1])
    var us = data[0]
    var nest = d3.nest()
        .key(function(d) { return d.leaid; }).sortKeys(d3.ascending)
        .key(function(d) { return d.year; }).sortKeys(d3.ascending)
        .entries(data[1])
    console.log(nest)
    pos = nest.map(function(e) { return e.key; }).indexOf('100002');
    console.log(pos)

    //var names = nest.values[0].values[0].name
    let result = nest.map(a => [a.values[0].values[0].name, a.key]);
    let result2 = nest.map(a => a.values[0].values[0].name);
    console.log(result[0])
    console.log(result2)
    console.log("TEST")

    new autoComplete({
        selector: 'input[name="q"]',
        minChars: 2,
        source: function(term, suggest){
            term = term.toLowerCase();
            var choices = result2
            var matches = [];
            for (i=0; i<choices.length; i++) {
                if (~choices[i].toLowerCase().indexOf(term)) matches.push(choices[i])
            }
            suggest(matches);
        }
    });

    var year;
    var district;
    var indicator;
    var ind_name;
    var selected;
    var showamt;
    var locktip;
    var oldyr  = document.getElementById('years').value
    var oldind = document.getElementById('indicators').value
    var oldamt = document.getElementById('showamt').value
    var displayed;
    tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);
    var appendSelected = function (a){
        if (selected != null){
            selected.remove();
            locktip.remove();
        }

        for (i=0; i<a.values.length; i++){
            if(a.values[i].key == year){
                ind_val = a.values[i].values[0][ind_name]
                console.log(ind_val)
                console.log(a.values[i].values[0][ind_name])
            }
        }
        console.log('"'+indicator+'"')
        t = '"'+indicator+'"'
        console.log(t)

        if(indicator=="numschools"){
            el = document.getElementById("numschools").innerHTML
        } else if(indicator=="math"){
            el = document.getElementById("math").innerHTML
        } else if(indicator=="eng"){
            el = document.getElementById("eng").innerHTML
        } else if(indicator=="totalrev"){
            el = document.getElementById("totalrev").innerHTML
        } else if(indicator=="enroll"){
            el = document.getElementById("enroll").innerHTML
        } else if(indicator=="teacherfte") {
            el = document.getElementById("teacherfte").innerHTML
        }

        // console.log(a.values[a.values.indexOf(year)].values[0][ind_name])
        selected = svg1.append("circle")
            .attr("class", "selected")
            .attr("r", 13)
            .attr("cx", function(d){
                var coords = projection([a.values[0].values[0].long, a.values[0].values[0].lat])
                return coords[0]
            })
            .attr("cy", function(d){
                var coords = projection([a.values[0].values[0].long, a.values[0].values[0].lat])
                return coords[1]
            })
            .attr("opacity",".25")
            .attr("fill", "Blue")
        locktip = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("opacity", 0)
                //  "<br>" + ind_name + ": " + a
            .html(function(){
                if(ind_val == null){
                    return "<p><strong>" + a.values[0].values[0].name +"</strong><br> " + a.values[0].values[0].city + ", " + a.values[0].values[0].state + "<br>" + "LEAid: " + a.key +"</p>"
                }else{
                    return "<p><strong>" + a.values[0].values[0].name +"</strong><br> " + a.values[0].values[0].city + ", " + a.values[0].values[0].state + "<br>" + "LEAid: " + a.key +"<br>" + el + ": " + ind_val + "</p>"
                }
            })
                .style("left", (projection([a.values[0].values[0].long, a.values[0].values[0].lat])[0] + 15) + "px")
                .style("top", (projection([a.values[0].values[0].long, a.values[0].values[0].lat])[1] + 155) + "px")
                .style("opacity", .9);

    }
    var someFunction = function (d=null) {
        // Do something...
        district = document.getElementById('q').value
        year = document.getElementById('years').value
        indicator = document.getElementById('indicators').value
        showamt = document.getElementById('showamt').value
        if(oldyr != year || oldind != indicator || oldamt != showamt){
            filterDistricts(year, indicator, showamt)
        }
        oldyr = year
        oldind = indicator
        oldamt = showamt

        if (d.values==null) {
            ind = result2.indexOf(district)

            if (ind > -1) {
                appendSelected(nest[ind])
            }
        }else{
            appendSelected(d)
        }
    };

    // Taken from https://stackoverflow.com/questions/30143082/how-to-get-color-value-from-gradient-by-percentage-with-javascript
    function pickHex(color1, color2, weight) {
        var w1 = weight;
        var w2 = 1 - w1;
        var rgb = [Math.round(color1[0] * w1 + color2[0] * w2),
            Math.round(color1[1] * w1 + color2[1] * w2),
            Math.round(color1[2] * w1 + color2[2] * w2)];
        return rgb;
    }


    var filterDistricts = function (yr, ind, amt) {
        // Do something...
        if(ind=="numschools"){
            ind_name = "number_of_schools"
        } else if(ind=="math"){
            ind_name = "math_test_pct_prof_midpt"
        } else if(ind=="eng"){
            ind_name = "read_test_pct_prof_midpt"
        } else if(ind=="totalrev"){
            ind_name = "rev_total"
        } else if(ind=="enroll"){
            ind_name = "enrollment_x"
        } else if(ind=="teacherfte") {
            ind_name = "teachers_total_fte"
        }

        // filter for the leaids and indicator values to sort on
        arr = []
        count = 0
        nest.forEach(function(d){
            d.values.forEach(function(c){
                if(c.key == yr){
                    val = parseFloat(c.values[0][ind_name])
                    if(isNaN(val) || val < 0){
                        count = count+1
                    }else{
                        arr.push([d.key, val])
                    }
                }
            })
        })
        arr.sort((a,b) => a[1] - b[1])
        if ((count/arr.length) > .1){
            alert(count/arr.length + " percent of data on this indicator and year is missing.")
        }else if(arr.length == 0){
            alert("This indicator does not exist in this year")
        }

        every_x_district = Math.floor(arr.length/amt)
        if(arr.length/amt < 1){
            alert("Only " + arr.length + " School Districts available for this year and indicator.")
        }
        filtered = []
        for (i=0; i<arr.length; i=i+every_x_district){
            filtered.push(arr[i])
        }
        while(filtered.length > amt){
            filtered.splice(Math.floor(Math.random()*filtered.length), 1);

        }

        filtered.unshift[arr[0]]
        filtered.push[arr.length-1]
        //pickHex(rgb(238, 238, 0), rgb(38, 166, 91), weight)
        var keepids = filtered.map(function(x) {return x[0]})
        var keep = nest.filter(d => keepids.includes(d.key))
        keep2 = keep.map(function(d){
            col = pickHex([238, 238, 0], [38, 166, 91], keepids.indexOf(d.key)/keepids.length)
            d['color'] = 'rgb(' + col[0] + ',' + col[1] + ',' + col[2] + ')'
            return d
        })
        console.log(filtered)
        console.log(keep2)
        plotDistrictsandGradient(keep2)

    }


    document.addEventListener('keyup', someFunction, false);

    var states = topojson.feature(us, us.objects.states).features
    svg1.selectAll(".state")
        .data(states)
        .enter().append("path")
        .attr("class", "state")
        .attr("d", path)


    var plotDistrictsandGradient = function (a) {
        if (displayed != null){
            displayed.remove()
        }
        if (a == null){
            a = nest
        }
        console.log(a)
        displayed = svg1.selectAll(".district")
            .data(a)
            .enter().append("circle")
            .attr("class", "district")
            .attr("cx", function (d) {
                var coords = projection([d.values[0].values[0].long, d.values[0].values[0].lat])
                return coords[0]
            })
            .attr("cy", function (d) {
                var coords = projection([d.values[0].values[0].long, d.values[0].values[0].lat])
                return coords[1]
            })
            .attr("opacity", function(d){
                if(d.color == null){
                    return ".25"
                }else{
                    val = .25 + .75*(1-(a.length/15000))
                    return val
                }
            })
            .attr("fill", function(d){
                if(d.color == null){
                    return "black"
                }else{
                    return d.color
                }
            })
            .attr("r", function(d) {
                if (d.color == null) {
                    return "2"
                } else {
                    return Math.floor(2 + 6*(1-(a.length/15000)))
                }
            })
            .on("mouseover", function () {
                const selection = d3.select(this)
                var selected = this.__data__;
                selection
                    .transition()
                    .duration(10)
                    .style("opacity", 1)
                    .style("fill", "turquoise")
                    .attr("r", function(d) {
                        if (d.color == null) {
                            return "5"
                        } else {
                            return Math.floor(2 + 6*(1-(a.length/15000)))
                        }
                    })
                tooltip.transition()
                    .duration(250)
                    .style("opacity", 1);
                tooltip.html("<p><strong>" + selected.values[0].values[0].name + "</strong><br> " + selected.values[0].values[0].city + ", " + selected.values[0].values[0].state + "<br>" + "LEAid: " + selected.key + "</p>")
                    .style("left", (d3.event.pageX + 15) + "px")
                    .style("top", (d3.event.pageY - 28) + "px")
                    .style("opacity", .9);
            })
            .on("mouseout", function () {
                const selection = d3.select(this)
                selection
                    .transition()
                    .delay("100")
                    .duration("10")
                    .style("r", function(d) {
                        if (d.color == null) {
                            return "2"
                        } else {
                            return Math.floor(2 + 6*(1-(a.length/15000)))
                        }
                    })
                    .style("opacity", function(d) {
                        if (d.color == null) {
                            return ".25"
                        } else {
                            val = .25 + .75*(1-(a.length/15000))
                            return val
                        }
                    })
                    .style("fill", function(d){
                        if(d.color == null){
                            return "black"
                        }else{
                            return d.color
                        }
                    })
                tooltip.transition()
                    .duration(250)
                    .style("opacity", 0);
            })
            .on("click", function () {
                someFunction(this.__data__);
            })
    }
    plotDistrictsandGradient(nest)
})






