const DEFAULT_API_OPTIONS = {method : "GET",
			     headers : {"Accept" : "application/vnd.api+json"},
			     credentials : "same-origin"};


function lookupRelationship(poiitem, jsondata, relname, attrname=null)
{
    var relid = poiitem["relationships"][relname]["data"]["id"];
    var reltype = poiitem["relationships"][relname]["data"]["type"];
    var flt = jsondata["included"].filter( x=> (x["id"] == relid && x["type"]
						== reltype));
    if(flt.length > 1)
	throw "logic error: multiple duplicate relationships found";
    if(flt.length == 0)
	throw "logic error: no results found!";
    if(attrname != null)
	return flt[0]["attributes"][attrname];
    else
	return flt[0]["attributes"];
}      


class POITable {

    constructor(filters = null, includevars = null) {
	this.ordermap = new Map();
	this.filters = filters;
	this.style_data = new Map();
	this.includes = includevars;
    }

    construct_params() {		
	const params = [["page[number]", "1"] ];
	if(this.includes != null)
	{
	    const paramout = {"include" : []};
	    for(const [objtype, fieldlist] of Object.entries(this.includes))
	    {
		paramout["include"].push(objtype);
		let st = "fields[" + objtype + "]";
		paramout[st] = fieldlist;
	    }

	    for(const [k,v] of Object.entries(paramout))
	    {
		params.push([k, paramout[k].join(",")]);
	    }
	}
	return params;
    }


    initfn() {};
    callbackfn(rjson) {};
    finalfn() {};
    
    async fetch_pois(sortkey = null)
    {
	let url = new URL("/api/poi", document.URL)

	const params = this.construct_params();
	this.initfn();
	
	if(sortkey != null)
	{
	    if( !(sortkey  in this.ordermap))
	    {
		this.ordermap[sortkey] = true;
	    }
	    else if(this.ordermap[sortkey])
	    {
		this.ordermap[sortkey] = false;
		sortkey = "-" + sortkey;
	    }
	    else
	    {
		this.ordermap[sortkey] = true;
	    }
	    params.push(["sort", String(sortkey)]);
	}

	if(this.filters != null)
	{
	    params.push(["filter[objects]", JSON.stringify(this.filters)]);
	}
	
	url.search = new URLSearchParams(params).toString();

	for(;;)
	{
	    const response = await fetch(url, DEFAULT_API_OPTIONS);
	    const rjson = await response.json();

	    if(rjson.hasOwnProperty("errors"))
	    {
		throw rjson["errors"]; 
	    }

	    this.callbackfn(rjson);
	    for(const item of rjson["included"].filter(x=>x["type"]=="style"))
	    {
		const styleid = Number(item["id"]);
		if(! this.style_data.has(styleid))
		{
		    const stylestyle = item["attributes"]["style"];
		    this.style_data.set(styleid, stylestyle);
		}

	    }

	    if(rjson["links"]["next"] == null)
		break;
	    url = rjson["links"]["next"];
	    
	}

	this.finalfn();
    }
    

}
