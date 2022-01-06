const cached_styles = new Map();
const rdr = new PlotlyShapeRenderer();

async function updatestylepreview(formelem) {
      const styleid = Number(formelem.value);
      if(! cached_styles.has(styleid))
      {
	  const url = new URL("/api/style/" + String(styleid), document.URL);
	  URL.search = new URLSearchParams([["fields[style]",
					     "style"]]).toString();

	  const options = {method : "GET",
			   headers : {"Accept" : "application/vnd.api+json"},
			   credentials : "same-origin"};
	  const response =  await fetch(url, options);
	  const rjson = await response.json();
	  const symbol = rjson["data"]["attributes"]["style"]["marker.symbol"];
	  const size = Number(rjson["data"]["attributes"]["style"]["marker.size"]);
	  const idx = rdr.add_style(symbol, size);
	  const pathitem = rdr.render_one_svg(idx);
	  svg_style_helper(pathitem, rjson["data"]["attributes"]["style"]);
	  const data = { renderid : idx,
			 svgpath : pathitem}
	  cached_styles.set(styleid, data);
      }

      const styledata = cached_styles.get(styleid);

      const tgt = document.getElementById("stylepreview");
      tgt.innerHTML = "";
      const svgitem = svg_centred_render_helper(styledata.svgpath, tgt, -1,
      null, 10);
      
  }

