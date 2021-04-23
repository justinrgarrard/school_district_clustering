margin = {top: 0, right: 0, bottom: 0, left: 0},
    width = window.innerWidth,
    height = 500;


var svg1 = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + (margin.left) + "," + margin.top +")")
    //.style('transform', 'translate(50%, 50%)')
    .style("display", "block")
    .style("margin", "auto")

d3.select("#chart").attr("align","center");

promises = [d3.json("data/us.json"), d3.csv("data/csv_to_json3.csv"), d3.csv("data/processed_features_labeled.csv"), d3.csv("data/median_clusters.csv")]

var projection = d3.geoAlbersUsa()
    .translate([width/2, height/2])
    .scale(1000)

var path = d3.geoPath().projection(projection)



Promise.all(promises).then(function(data) {



    var us = data[0]
    var nest = d3.nest()
        .key(function(d) { return d.leaid; }).sortKeys(d3.ascending)
        .key(function(d) { return d.year; }).sortKeys(d3.ascending)
        .entries(data[1])

    var nest_for_plot = d3.nest()
        .key(function(d) { return d.year; }).sortKeys(d3.ascending)
        .key(function(d) { return d.cluster; }).sortKeys(d3.ascending)
        .entries(data[1])
    console.log(nest_for_plot)

    pos = nest.map(function(e) { return e.key; }).indexOf('100002');


    var processed_features = d3.nest()
        .key(function(d) { return d.leaid; }).sortKeys(d3.ascending)
        .key(function(d) { return d.year; }).sortKeys(d3.ascending)
        .entries(data[2])
    console.log(processed_features)


    var median_clusters = data[3]

    //var names = nest.values[0].values[0].name
    let result = nest.map(a => [a.values[0].values[0].name, a.key]);
    let result2 = nest.map(a => a.values[0].values[0].name);

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
    var clusters;
    var table;
    var cluster_data;
    var lists;
    var oldyr  = document.getElementById('years').value
    var oldind = document.getElementById('indicators').value
    var oldamt = document.getElementById('showamt').value
    var displayed;
    var keepids;
    var keep2;

    // Stolen from https://stackoverflow.com/questions/2901102/how-to-print-a-number-with-commas-as-thousands-separators-in-javascript
    function numberWithCommas(x) {
        var y = Math.round(parseFloat(x) * 100) / 100
        return y.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);
    var compare = function(a, b){
        if(parseFloat(a) > parseFloat(b)){
            return "Greater than Median of Cluster"
        }else if (parseFloat(a) < parseFloat(b)){
            return "Less than Median of Cluster"
        }else{
            return "Same as Median of Cluster"
        }
    }
    var appendSelected = function (a){
        if (selected != null){
            selected.remove();
            locktip.remove();
            table.remove();
            table1.remove();

        }



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
        } else if(indicator=="cluster") {
            el = document.getElementById("cluster").innerHTML
        }

        filterDistricts(year, indicator, showamt)
        for (i=0; i<a.values.length; i++){
            if(a.values[i].key == year){
                ind_val = a.values[i].values[0][ind_name]
            }
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
            .attr("opacity",".75")
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
                //.style("left", (projection([a.values[0].values[0].long, a.values[0].values[0].lat])[0] + 55) + "px")
                //.style("top", (projection([a.values[0].values[0].long, a.values[0].values[0].lat])[1] + 155) + "px")
                .style("left", (d3.event.pageX + 15) + "px")
                .style("top", (d3.event.pageY - 28) + "px")
                .style("opacity", .9);

        test = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("opacity", 0)
            .html("<p><strong>" + a.values[0].values[0].name +"</strong><br> " + a.values[0].values[0].city + ", " + a.values[0].values[0].state + "<br>" + "LEAid: " + a.key +"</p>")


        var medians;
        for (i=0; i<processed_features.length; i++) {
            for (j = 0; j < processed_features[i].values.length; j++) {
                if (processed_features[i].key == a.key){
                    if (processed_features[i].values[j].key == year) {
                        cluster_data = processed_features[i].values[j].values[0]
                    }
                }
            }
        }

        for (i=0; i<median_clusters.length; i++) {
            if (parseInt(median_clusters[i].label) == cluster_data.label){
                if (parseInt(median_clusters[i].year) == cluster_data.year) {
                    medians = median_clusters[i]
                }
            }
        }

        keep2 = mapColors(keep2)
        plotDistrictsandGradient(keep2)

        var columns1 = [a.values[0].values[0].name + ' - ' + year];
        var rows1 = [['Part of cluster: ' + medians['cluster_name']], [medians['cluster_desc']], ['*Represents ~75% of districts; **25th and 75th percentile of math and reading midpoints']]
        table1 = d3.select('body').append('table').attr("class", "table").style("border-color", "blue").style("border-style", "solid")
        var titles1 = d3.keys(columns1);
        var headers1 = table1.append('thead').append('tr')
            .selectAll('th')
            .data(titles1).enter()
            .append('th')
            .text(function (d) {
                return columns1[d];
            })

        var rows12 = table1.append('tbody').selectAll('tr')
            .data(rows1).enter()
            .append('tr');
        rows12.selectAll('td')
            .data(function (d) {
                return d.map(function (k) {
                    return { 'value': k, 'name': d.indexOf(k)};
                });
            }).enter()
            .append('td')
            .attr('data-th', function (d) {
                return d.name;
            })
            .text(function (d) {
                return d.value;
            });

        var columns = ['Type', 'Enrollment', 'Number of Schools', 'Full-Time Equivalent of Teachers', '# of Special Ed Students', 'Total Revenue ($)', 'Total Expenses ($)', 'Reading % proficient midpoint', 'Math % proficient midtpoint'];
        var rows2 = [[a.values[0].values[0].name, numberWithCommas(cluster_data['enrollment_x']), numberWithCommas(cluster_data['number_of_schools']), numberWithCommas(cluster_data['teachers_total_fte']), numberWithCommas(cluster_data['spec_ed_students']), numberWithCommas(cluster_data['rev_total']), numberWithCommas(cluster_data['exp_total']), cluster_data['read_test_pct_prof_midpt'], cluster_data['math_test_pct_prof_midpt']], ['Median of Cluster', numberWithCommas(medians['enrollment_x']), numberWithCommas(medians['number_of_schools']), numberWithCommas(medians['teachers_total_fte']), numberWithCommas(medians['spec_ed_students']), numberWithCommas(medians['rev_total']), numberWithCommas(medians['exp_total']), medians['read_test_pct_prof_midpt'], medians['math_test_pct_prof_midpt']], ['', compare(cluster_data['enrollment_x'], medians['enrollment_x']), compare(cluster_data['number_of_schools'], medians['number_of_schools']), compare(cluster_data['teachers_total_fte'], medians['teachers_total_fte']), compare(cluster_data['spec_ed_students'], medians['spec_ed_students']), compare(cluster_data['rev_total'], medians['rev_total']), compare(cluster_data['exp_total'], medians['exp_total']), compare(cluster_data['read_test_pct_prof_midpt'], medians['read_test_pct_prof_midpt']), compare(cluster_data['math_test_pct_prof_midpt'], medians['math_test_pct_prof_midpt'])]]


        table = d3.select('body').append('table').attr("class", "table").style("border-color", "blue").style("border-style", "solid")
        var titles = d3.keys(columns);
        var headers = table.append('thead').append('tr')
            .selectAll('th')
            .data(titles).enter()
            .append('th')
            .text(function (d) {
                return columns[d];
            })


        var rows = table.append('tbody').selectAll('tr')
            .data(rows2).enter()
            .append('tr');
        rows.selectAll('td')
            .data(function (d) {
                return d.map(function (k) {
                    return { 'value': k, 'name': d.indexOf(k)};
                });
            }).enter()
            .append('td')
            .attr('data-th', function (d) {
                return d.name;
            })
            .text(function (d) {
                return d.value;
            });


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
    //stolen from  https://stackoverflow.com/questions/19269545/how-to-get-a-number-of-random-elements-from-an-array
    function getRandom(arr, n) {
        var result = new Array(n),
            len = arr.length,
            taken = new Array(len);
        if (n > len)
            throw new RangeError("getRandom: more elements taken than available");
        while (n--) {
            var x = Math.floor(Math.random() * len);
            result[n] = arr[x in taken ? taken[x] : x];
            taken[x] = --len in taken ? taken[len] : len;
        }
        return result;
    }

    var mapColors = function(e){
        keep3 = e.map(function (d) {
            var y = d.values
            var z = y.map(x => Object.values(x)[0])
            //console.log(selected)

            if (selected == null){
                col = pickHex([238, 238, 0], [38, 166, 91], keepids.indexOf(d.key) / keepids.length)
                d['color'] = 'rgb(' + col[0] + ',' + col[1] + ',' + col[2] + ')'
            }else{
                if (cluster_data != null){
                    if (y[z.indexOf(year)].values[0].label == cluster_data.label) {
                        d['color'] = 'rgb(' + 0 + ',' + 0 + ',' + 255 + ')'
                    }else {
                        col = pickHex([238, 238, 0], [38, 166, 91], keepids.indexOf(d.key) / keepids.length)
                        d['color'] = 'rgb(' + col[0] + ',' + col[1] + ',' + col[2] + ')'
                    }
                }else {
                    col = pickHex([238, 238, 0], [38, 166, 91], keepids.indexOf(d.key) / keepids.length)
                    d['color'] = 'rgb(' + col[0] + ',' + col[1] + ',' + col[2] + ')'
                }
            }
            return d
        })
        return keep3
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
        } else if(ind=="cluster") {
            ind_name = "label"
        }
        // filter for the leaids and indicator values to sort on
        if (ind_name!="label" || ind_name == "label") {


            arr = []
            count = 0
            nest.forEach(function (d) {
                d.values.forEach(function (c) {
                    if (c.key == yr) {
                        val = parseFloat(c.values[0][ind_name])
                        if (isNaN(val) || val < 0) {
                            count = count + 1
                        } else {
                            arr.push([d.key, val])
                        }
                    }
                })
            })
            arr.sort((a, b) => a[1] - b[1])
            if ((count / arr.length) > .1) {
                alert(count / arr.length + " percent of data on this indicator and year is missing.")
            } else if (arr.length == 0) {
                alert("This indicator does not exist in this year")
            }

            every_x_district = Math.floor(arr.length / amt)
            if (arr.length / amt < 1) {
                alert("Only " + arr.length + " School Districts available for this year and indicator.")
            }
            filtered = []
            for (i = 0; i < arr.length; i = i + every_x_district) {
                filtered.push(arr[i])
            }
            while (filtered.length > amt) {
                filtered.splice(Math.floor(Math.random() * filtered.length), 1);

            }

            filtered.unshift[arr[0]]
            filtered.push[arr.length - 1]
            //pickHex(rgb(238, 238, 0), rgb(38, 166, 91), weight)
            keepids = filtered.map(function (x) {
                return x[0]
            })
            var keep = nest.filter(d => keepids.includes(d.key))
            keep2 = mapColors(keep)
            plotDistrictsandGradient(keep2)
        }
        // ************ UNCOMMENT THIS SECTION TO USE SPECIFIC COLORS FOR CLUSTERS - REMEMBER TO REMOVE BRACKET ABOVE AND CHANGE IF STATEMENT *********
        // }else{
        //     arr = []
        //     arr2 = []
        //     for (i = 0; i < 16; i++) {
        //         arr2.push([])
        //     }
        //     colors = ['#ff4d4d', '#ff0000', '#800000', '#4d0000', '#ffff99', '#ffff4d', '#e6e600', '#b3b300', '#85e085', '#47d147', '#29a329', '#196619', '#99b3ff', '#4d79ff', '#0039e6', '#001a66','#ff9933', '#ff0000']
        //     count = 0
        //     for (i=0; i<nest.length; i++){
        //         for (j=0; j< nest[i].values.length; j++) {
        //             if (nest[i].values[j].key == yr) {
        //                 w = nest[i]
        //
        //                 val2 = w.values[j].values[0].cluster
        //                 val = parseInt(val2)
        //                 w['color'] = colors[val-1]
        //                 if (isNaN(val) || val == null) {
        //                     count = count + 1
        //                 } else {
        //                     arr.push(w)
        //                     arr2[val-1].push(w)
        //                 }
        //             }
        //         }
        //     }
        //
        //     clusters = []
        //     lists = []
        //     every_x_district = Math.floor(arr.length / amt)
        //     console.log(every_x_district)
        //     arr2.forEach(function(d){
        //         clust_amt = Math.ceil((d.length/arr.length)*amt)
        //         filt = getRandom(d, clust_amt)
        //         lists.push(filt)
        //         filt.forEach(function(e){clusters.push(e)})
        //     })
        //     for (i=0; i<arr.length; i++){
        //         for (j=0; j< arr[i].values.length; j++) {
        //             if (arr[i].values[j].key == yr) {
        //                 w = arr[i]
        //                 val = parseInt(w.values[j].values[0].cluster)
        //                 w['prop'] = (1 - (arr2[val-1].length/arr.length))/2
        //
        //             }
        //         }
        //     }
        //     console.log(arr)
        //     console.log(arr2)
        //     console.log(clusters)
        //     console.log(lists)
        //     plotDistrictsandGradient(clusters)
        // }

    }


    document.addEventListener('keyup', someFunction, false);

    var states = topojson.feature(us, us.objects.states).features
    svg1.selectAll(".state")
        .data(states)
        .enter().append("path")
        .attr("class", "state")
        .attr("align", "center")
        .attr("d", path)



    var plotDistrictsandGradient = function (a) {
        if (displayed != null){
            displayed.remove()
        }
        if (a == null){
            a = nest
        }
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
                if(indicator == "cluster"){
                    return .75 //+ .75*(d.prop)
                }else{
                    if(d.color == null){
                        return ".75"
                    }else{
                        //val = .25 + .75*(1-(a.length/15000))
                        return ".75"
                    }
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
                    if(indicator == "cluster"){
                        return 5 //2*((6-colors.indexOf(d.color)) + 1)
                    }else {
                        return 5 //Math.floor(2 + 6*(1-(a.length/15000)))
                    }
                }
            })
            .on("mouseover", function () {
                const selection = d3.select(this)
                var selected = this.__data__;
                selection
                    .transition()
                    .duration(10)
                    .style("opacity", .25)
                    .style("fill", "turquoise")
                    .attr("r", function(d) {
                    //     return 5
                    // })
                        if (d.color == null) {
                            return "5"
                        } else {
                            if(indicator == "cluster"){
                                return 5 //2*((6-colors.indexOf(d.color)) + 1)
                            }else {
                                return 5 //Math.floor(2 + 6*(1-(a.length/15000)))
                            }
                        }
                    })
                tooltip.transition()
                    .duration(250)
                    .style("opacity", .9);
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
                            if(indicator == "cluster"){
                                return 5//2*((6-colors.indexOf(d.color)) + 1)
                            }else {
                                return 5//Math.floor(2 + 6*(1-(a.length/15000)))
                            }
                        }
                    })
                    .style("opacity", function(d){
                        if(indicator == "cluster"){
                            return .75 //+ .75*(d.prop)
                        }else{
                            if(d.color == null){
                                return ".75"
                            }else{
                                val = .75 //+ .75*(1-(a.length/15000))
                                return val
                            }
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






