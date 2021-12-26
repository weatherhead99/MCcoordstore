class PlotlyShapeRenderer {
    constructor() {
	this._plotdom = document.createElement('div');
	this._renderdom = document.createElement('svg');

	Plotly.newPlot(this._plotdom, [{x : [0], y : [0]}]);
	this._n_items = 0;
    }

    replace_styles(markernames, sizes)
    {
	const xarr = Array.from(Array(markernames.length).keys());
	const yarr = Array(markernames.length).fill(1);

	const update = { x : [xarr],
			 y : [yarr],
			 type : "scatter",
			 mode : "markers",
			 "marker.size" : [sizes],
			 "marker.symbol" : [markernames]
		       };

	Plotly.restyle(this._plotdom, update, 0);
	
    }

    render_svg() {
	const svgitems = this._plotdom.querySelectorAll("path.point");
	console.log("n svgitems")
	console.log(svgitems.length);
	var paths = new Array();
	for(const [k,v] of Object.entries(svgitems))
	    paths.push(v.attributes.d.value);
	
    }

    get plotdom() { return this._plotdom;}

}

function test () {
    console.log("test");
}

