const SVGNS = "http://www.w3.org/2000/svg";

class PlotlyShapeRenderer {
    constructor() {
	this._plotdom = document.createElement('div');

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
