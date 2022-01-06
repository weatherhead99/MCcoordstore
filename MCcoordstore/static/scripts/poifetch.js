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

    constructor() {
	this.ordermap = new Map();
    }

    async fetch_pois(initfn, callbackfn, finalfn, sortkey = null)
    {
	let url = new URL("/api/poi", document.URL)
	const params = [["page[number]", "1"], ["include", "user,style"],
			["fields[user]", "displayname"],
			["fields[style]", "name,style"]];

	initfn(this);
	
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
	url.search = new URLSearchParams(params).toString();

	for(;;)
	{
	    const response = await fetch(url, DEFAULT_API_OPTIONS);
	    const rjson = await response.json();

	    callbackfn(this, rjson);

	    if(rjson["links"]["next"] == null)
		break;
	    url = rjson["links"]["next"];
	    
	}

	finalfn(this);
    }
    

}
