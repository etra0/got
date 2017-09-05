d3.json('./data.json', function(data) {

	// global variables & main definitions of d3
	var actors = [];
	data.forEach(function(d) {
		actors.push(d.actor);
	});

	var margin = {top: 40, right: 20, bottom: 30, left: 120},
		width = 960 - margin.left - margin.right,
		height = 500 - margin.top - margin.bottom;
	//
	// x scale va desde las seasons
	var x_scale = d3.scaleLinear()
		.domain([0, 7])
		.range([0, width]);

	var y_scale = d3.scaleLinear()
		.domain([1, 10])
		.range([0, height - 90]);

	var color_scale = d3.scaleLinear()
		.domain([1, 20])
		.range(['#FE860B', '#0C7E9E'])

	var y_axis = d3.axisLeft(y_scale)
		.tickFormat(function(d, i) {
			return actors[i];
		});

	var x_axis = d3.axisTop(x_scale)
		.ticks(8)
		.tickFormat(function(d, i ) {
			if (!i)
				return ""
			return "Season " + i;
		});

	var canvas = d3.select(".container").append('svg')
		.attr('width', width + margin.left + margin.right)
		.attr('height', height + margin.top + margin.bottom)
		.append('g')
			.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
			

	data.forEach(function (data, index) {
		// De ahora en adelante,
		// data hara referencia a la data global, que contiene
		// death, i_season_n, season_n
		// Ademas, todas las variables dentro de funciones
		// comenzaran con un guion bajo.

		// Es necesario agruparlo para separar cada personaje.
		current_line = canvas.append('g');

		var handle_color = function(_d, _i, circle=true) {
			if (data.death === _i && circle)
				return "white";
			else {
				console.log("current death:", data.death, "supposed death:", _i + 1);
				return color_scale(index);
			}
		}

		// definicion de los puntos finales a ocupar
		var data_points = (function() {
			var _d = [
				{x: 0, y: data.i_season_1},
				{x: 1, y: data.i_season_1, dur: data.season_1},
				{x: 2, y: data.i_season_2, dur: data.season_2},
				{x: 3, y: data.i_season_3, dur: data.season_3},
				{x: 4, y: data.i_season_4, dur: data.season_4},
				{x: 5, y: data.i_season_5, dur: data.season_5},
				{x: 6, y: data.i_season_6, dur: data.season_6},
				{x: 7, y: data.i_season_7, dur: data.season_7}]

			// we clean all the first nodes major than 10
			// TODO: FIXEAR ESTA WEAITA!!
			// buscar alguna forma mas apropiada de 
			// eliminar los nodos de mejor forma
//			for (_i = 0; _i < _d.length; _i++) {
//				if (_d[_i].y <= 10) {
//					for (_j = 0; _j < _i; _j++) {
//						_d[_j].x = _d[_i].x;
//						_d[_j].y = _d[_i].y;
//					}
//
//					break;
//				}
//			}
//
//			var _all_major = true;
//			for (_i = 0; _i < _d.length; _i++) {
//				// if we encounter one variable major than 10, we have
//				// to verify if the next ones are major than 10 too.
//				if (_d[_i].y > 10) {
//					_all_major = true;
//					for (_j = _i; _j < _d.length; _j++) {
//						// if not, we change _all_major to false
//						if (_d[_j].y < 10) {
//							_all_major = false;
//						}
//					}
//					if (_all_major) {
//						for (_j = _i; _j < _d.length; _j++) {
//							_d[_j].x = _d[_i-1].x;
//							_d[_j].y = _d[_i-1].y;
//						}
//					}
//					break;
//				}
//			}

			return _d;
		})();

		var lineFunction = d3.line()
			.x(function(d) { return x_scale(d.x); })
			.y(function(d) { return y_scale(d.y); })
			.curve(d3.curveMonotoneX)

		// LINE PLOT
		current_line.append('path')
			.attr("d", lineFunction(data_points))
			.attr("stroke", function() { return color_scale(index); })
			.attr('stroke-width', 10)
			.on('mouseover', function() {
				var _current = d3.select(this);
				_current.attr('stroke', 'red');

				// TODO: reemplazar por un HOVER
				var _text = d3.select('.character');
				_text.text(data.actor);
			})
			.on('mouseout', (function(_d, _i) {
				var _current = d3.select(this);
				_current.attr('stroke', function() { return handle_color(_d, _i, circle=false); });

				// TODO: reemplazar por un HOVER
				var _text = d3.select('.character');
				_text.text("Game of Thrones");
			}))
			.attr('fill', 'none');

		// Circulos del plot principal
		current_line.selectAll('circle')
			.data(data_points)
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
			.attr('fill', function(_d, _i) { console.log('circle', _i); return handle_color(_d, _i); })
			.attr('stroke', 'black')
			.attr('stroke-width', 2)
			.on('mouseover', (function(_d, _i) { // Para la selection.on, recordar que la funcion debe pasarse entre parentesis
												 // TODO: investigar por que
				var _current = d3.select(this);
				_current.attr('fill', 'red');
				var _text = d3.select('.character');
				console.log("season", _d)
				_text.text(data.actor + " " + _d.dur + " minutos");
			}))
			.on('mouseout', (function(_d, _i) {
				var _current = d3.select(this);
				_current.attr('fill', function() { return handle_color(_d, _i); });
				var _text = d3.select('.character');
				_text.text("Game of Thrones");
			}));

	});
	
	// y_axis
	canvas.append('g')
		.call(y_axis);

	canvas.append('g')
		.attr('transform', 'translate(0, -20)')
		.call(x_axis);
});
