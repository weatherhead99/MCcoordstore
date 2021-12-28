const SVGNS = "http://www.w3.org/2000/svg";
const DEFAULT_DATA =  { x : [],
			y : [],
			text : [],
			mode: "markers",
			type: "scatter",
			marker : {symbol : [],
				  size : [],
				  color : [],
				  opacity: [],
				  line : {width : [],
					  color : []}}};

class PlotlyShapeRenderer {
    constructor(svg_padding = 0) {
	this._plotdom = document.createElement('div');

	this._plotobj = null;
	this._n_items = 0;
	this._padding = svg_padding;

    }

    get_plot_data(markernames, sizes)
    {
	const data = { type : "scatter",
		       mode : "markers" };

	if(sizes.hasOwnProperty("length"))
	{
	    console.log("array marker names");
	    console.log(markernames);
	    const xarr = Array.from(Array(markernames.length).keys()).map(x=> x+this._n_items);
	    const yarr = Array(markernames.length).fill(1);
	    data["x"] = xarr;
	    data["y"] = yarr;

	    data["marker"] = { symbol : markernames,
			       size : sizes};
	    
	}
	else
	{
	    data["x"] = [this._n_items];
	    data["y"] = [1];
	    data["marker"] = { symbol : [markernames],
			       size : [sizes]};
	}

	return data;
    }

    get_plot_update(markernames, sizes)
    {
	if(sizes.hasOwnProperty("length"))
	{
	    const xarr = Array.from(Array(markernames.length).keys()).map(x=> x+this._n_items);
	    const yarr = Array(markernames.length).fill(1);
	    return { x : [xarr],
		     y : [yarr],
		     "marker.size" : [sizes],
		     "marker.symbol" : [markernames]};
	    
	}

	else
	{
	    console.log("single item");
	    return { x : [[this._n_items]],
		     y : [[1]],
		     "marker.size" : [[sizes]],
		     "marker.symbol" : [[markernames]]}
	}
	
    }

    update_idxs(newitems)
    {
	if(newitems.hasOwnProperty("length"))
	{
	    const idxstart = this._n_items;
	    const idxs = Array.from(Array(newitems.length).keys()).map(x=> x+ idxstart);
	    this._n_items += newitems.length;
	    return idxs;
	}

	const idx = this._n_items;
	this._n_items += 1;
	return idx;

    }

    _style_logic(markernames, sizes, fun)
    {
	if(this._plotobj == null)
	{
	    console.log("null plotobj");
	    const data = this.get_plot_data(markernames, sizes);
	    this._plotobj = Plotly.newPlot(this._plotdom, [data]);
	}
	else
	{
	    console.log("already existing plotobj");
	    const update = this.get_plot_update(markernames, sizes);
	    fun(this._plotdom, update);
	}

	return this.update_idxs(sizes);
    }
    
    add_style(markername, size)
    {
	const fun = function(dom, data) {
	    Plotly.extendTraces(dom, data, [0]);
	};
	return this._style_logic(markername, size, fun);
    }
    
    replace_styles(markernames, sizes)
    {
	this._n_items = 0;
    	const fun = function(dom, data)  {
	    Plotly.restyle(dom, data, 0);
	};
	return this._style_logic(markernames, sizes, fun);
    }

    render_one_svg(idx) {
	const item_in = this._plotdom.querySelectorAll("path.point")[idx];
	const path = item_in.attributes.d.value;
	const svgitem = document.createElementNS(SVGNS, "path");
	svgitem.setAttributeNS(null, "class", "rendersym");
	svgitem.setAttributeNS(null, "d", path);

	return svgitem;
    }

    get plotdom() { return this._plotdom;}
    get renderdom() { return this._renderdom;}
};

function svg_style_helper(pathitem, styledata)
{
    pathitem.setAttributeNS(null, "fill", styledata["marker.color"]);
    pathitem.setAttributeNS(null, "stroke", styledata["marker.line.color"]);
    pathitem.setAttributeNS(null, "opacity", styledata["marker.opacity"]);
    pathitem.setAttributeNS(null, "stroke-width", styledata["marker.line.width"]);

}

function svg_centred_render_helper(pathitem, target,  width, applyscale=null, padding=0)
{
    const item = document.createElementNS(SVGNS, "svg");

    let translatestr = "";
    if(applyscale != null)
    {
	translatestr +=  "scale(" + applyscale + ")";
    }

    const attacheditem = item.appendChild(pathitem);
    target.appendChild(item);

    
    if(width < 0)
    {
	item.setAttributeNS(null,"width", 10000);
	item.setAttributeNS(null,"height", 10000);
	const bbox = attacheditem.getBBox();
	item.setAttributeNS(null,"width", bbox.width + padding);
	item.setAttributeNS(null,"height",bbox.height + padding);
	width = bbox.width + padding;
    }
    else
    {
	item.setAttributeNS(null, "width", width + padding);
	item.setAttributeNS(null, "height", width + padding);
    }

    translatestr += " translate(" + width/2 + "," + width/2 + ")";

    attacheditem.setAttributeNS(null, "transform",translatestr);
    return item;
}

class PlotlyCoordMapRenderer
{
    constructor(title, width, plotdom)
    {
	this._layout = {autosize : true,
			automargin : true,
			title : title,
			xaxis : {title : "X"},
			yaxis : {title : "Z"},
			width : width};

	//need a deep copy of the default data 
	this._data = JSON.parse(JSON.stringify(DEFAULT_DATA));

	this._config = {responsive : true,
			modeBarButtonsToRemove : ["select2d", "lasso2d"],
			scrollZoom : true};
	
	this._plotdom = plotdom;
	Plotly.newPlot(this._plotdom, [this._data], this._layout, this._config);
    }

    plotPoint(x, y, txt, style)
    {
	const update = { x : [[x]],
			 y : [[y]],
			 text : [[txt]]};

	Object.entries(style).map(
	    function ([key,idx]) {
		update[[key]] = [[idx]];
	    });

	Plotly.extendTraces(this._plotdom, update, [0]);
	
    }

    clearPlot()
    {
	this._data.x.length = 0;
	this._data.y.length = 0;
    }


};

class PlotlyStyleRenderer
{
    constructor(divtarget, symwidth)
    {
	this._divtarget = divtarget;
	this._symwidth = symwidth;
	this._iotarr = Array.from(Array(symwidth).keys());

	this._data = JSON.parse(JSON.stringify(DEFAULT_DATA));
	this._data.marker.size = 20;
	this._data.marker.line.width = 5;
	
	this._layout = {
	    autosize : true,
	    xaxis : {visible: false, automargin: true},
	    yaxis : {visible: false, automargin: true},
	    width: "50%",
	    margin : {
		l : 0,
		r : 0,
		t : 0,
		b : 0,
		pad : 4}
	    
	};
    }

    plot_all_possible_symbols()
    {
	const marker = Plotly.PlotSchema.get().traces.scatter.attributes.marker;
	const symstrings = marker.symbol.values.filter(x => typeof(x)=="string" && Number.isNaN(Number(x)) == true);
	const nrows = Math.floor(symstrings.length / this._symwidth);

	var symslice = 0;
	for(let i =0 ; i < nrows -1; i++)
	{
	    this._data.x.push(...this._iotarr);
	    this._data.y.push(...Array(this._symwidth).fill(i));
	    this._data.marker.symbol.push(...symstrings.slice(symslice,
							      symslice + this._symwidth));
	    this._data.text.push(...symstrings.slice(symslice, symslice + this._symwidth));
	    symslice += this._symwidth;
	}

	Plotly.newPlot(this._divtarget, [this._data], this._layout);

    }



};
