d3.json('./data.json', function(data) {

	// global variables
	console.log(data)
	var actors = [];
	data.forEach(function(d) {
		actors.push(d.actor);
	});

	var margin = {top: 20, right: 20, bottom: 30, left: 120},
		width = 960 - margin.left - margin.right,
		height = 500 - margin.top - margin.bottom;
	//
	// x scale va desde las seasons
	var x_scale = d3.scaleLinear()
		.domain([0, 7])
		.range([0, width]);

	var y_scale = d3.scaleLinear()
		.domain([1, 10])
		.range([0, height]);

	var color_scale = d3.scaleLinear()
		.domain([1, 20])
		.range(['#FE860B', '#0C7E9E'])

	var axis = d3.axisLeft(y_scale)
		.tickFormat(function(d, i) {
			return actors[i];
		});

	var canvas = d3.select(".container").append('svg')
		.attr('width', width + margin.left + margin.right)
		.attr('height', height + margin.top + margin.bottom)
		.append('g')
			.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
			

	data.forEach(function (d, i) {
		current_line = canvas.append('g');

		var handle_color = function(_d, _i) {
			if (_d.death === _i + 1)
				return "white";
			else {
				console.log(_d.death, _i + 1);
				return color_scale(i);
			}
		}

		var current_data = (function() {
			var _d = [
				{x: 0, y: d.i_season_1},
				{x: 1, y: d.i_season_1},
				{x: 2, y: d.i_season_2},
				{x: 3, y: d.i_season_3},
				{x: 4, y: d.i_season_4},
				{x: 5, y: d.i_season_5},
				{x: 6, y: d.i_season_6},
				{x: 7, y: d.i_season_7}]

			// we clean all the first nodes major than 10
			for (_i = 0; _i < _d.length; _i++) {
				if (_d[_i].y <= 10) {
					for (_j = 0; _j < _i; _j++) {
						_d[_j].x = _d[_i].x;
						_d[_j].y = _d[_i].y;
					}

					break;
				}
			}

			var _all_major = true;
			for (_i = 0; _i < _d.length; _i++) {
				// if we encounter one variable major than 10, we have
				// to verify if the next ones are major than 10 too.
				if (_d[_i].y > 10) {
					_all_major = true;
					for (_j = _i; _j < _d.length; _j++) {
						// if not, we change _all_major to false
						if (_d[_j].y < 10) {
							_all_major = false;
						}
					}
					if (_all_major) {
						console.log(d.actor, _i);
						for (_j = _i; _j < _d.length; _j++) {
							_d[_j].x = _d[_i-1].x;
							_d[_j].y = _d[_i-1].y;
						}
					}
					break;
				}
			}

			return _d;
		})();

		var lineFunction = d3.line()
			.x(function(d) { return x_scale(d.x); })
			.y(function(d) { return y_scale(d.y); })
			.curve(d3.curveMonotoneX)

		// LINE PLOT
		current_line.append('path')
			.attr("d", lineFunction(current_data))
			.attr("stroke", function(d) { return color_scale(i); })
			.attr('stroke-width', 10)
			.attr('fill', 'none');

		current_line.selectAll('circle')
			.data(current_data)
			.enter()
			.append('circle')
			.attr('r', 10)
			.attr('cx', function(d, i) {
				if (d.x > 0)
					return x_scale(d.x);
				else
					return x_scale(-100);
			})
			.attr('cy', function(d) { return y_scale(d.y); })
			.attr('fill', function(_d, _i) { return handle_color(_d, _i); })
			.attr('stroke', 'black')
			.attr('stroke-width', 2)
			.on('mouseover', function(_d, _i) {
				var _current = d3.select(this);
				_current.attr('fill', 'red');
				var _text = d3.select('.character');
				_text.text(d.actor + " " + d['season_' + _i] + " Minutos");
			})
			.on('mouseout', function() {
				var _current = d3.select(this);
				_current.attr('fill', function(_d, _i) { return handle_color(_d, _i); });
				var _text = d3.select('.character');
				_text.text("Game of Thrones");
			});

	});
	canvas.call(axis);
});
