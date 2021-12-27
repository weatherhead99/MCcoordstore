const SVGNS = "http://www.w3.org/2000/svg";

class PlotlyShapeRenderer {
    constructor() {
	this._plotdom = document.createElement('div');

	this._plotobj = null;
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
	if(this._plotobj == null)
	{
	    const data = {x : xarr,
			  y : yarr,
			  type: "scatter",
			  mode : "markers",
			  marker : {size : sizes,
				    symbol: markernames}
			  };
	    console.log("plotobj is null, new plot creating");
	    this._plotobj = Plotly.newPlot(this._plotdom, [data]);
	}
	else
	{
	    	const update = { x : [xarr],
			 y : [yarr],
			 type : "scatter",
			 mode : "markers",
			 "marker.size" : [sizes],
			 "marker.symbol" : [markernames]
		       };
	    Plotly.restyle(this._plotdom, update, 0);
	}

	this._n_items += markernames.length;
	
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

function svg_centred_render_helper(pathitem, target,  width, applyscale=null)
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
	item.setAttributeNS(null,"width", bbox.width);
	item.setAttributeNS(null,"height",bbox.height);
	width = bbox.width;
    }
    else
    {
	item.setAttributeNS(null, "width", width);
	item.setAttributeNS(null, "height", width);
    }

    translatestr += " translate(" + width/2 + "," + width/2 + ")";

    attacheditem.setAttributeNS(null, "transform",translatestr);
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
	
	this._data = { x : [],
		       y : [],
		       text : [],
		       mode: "markers",
		       type: "scatter",
		       marker : {symbol : [],
				 size : [],
				 color : [],
				 line : {width : [],
					 color : []}}};

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
