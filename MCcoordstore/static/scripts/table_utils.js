  function convertUTCdtToLocal(st) {
  dt = new Date(st.trim());
  return dt.toLocaleString();
  };

function sortTable(tabid, trclass) {
    var shouldSwitch;
    var ascending = true;
    var nswitches = 0;
    var table = document.getElementById(tabid);
    var switching = true;
    var rows = table.getElementsByClassName("tr_poiid");
    while(switching) {
	switching = false;
	for(var i=0; i < (table.rows.length -2); i++)
	{
	    shouldSwitch = false;
	    var x = rows[i].getElementsByClassName(trclass)[0];
	    var y = rows[i+1].getElementsByClassName(trclass)[0];

	    if(x.hasAttribute("data-isnum") && x.attributes["data-isnum"].value == 1)
	    {
		if(ascending)
		{
		    if(Number(x.innerHTML) > Number(y.innerHTML))
		    {
			shouldSwitch = true;
			break;
		    }
		}
		else
		{
		    if(Number(x.innerHTML) < Number(y.innerHTML))
		    {
			shouldSwitch = true;
			break;
		    }
		}
		    
	    }
	    else{
		if(ascending)
		{
		    if(x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
			shouldSwitch = true;
			break;
		    }
		}
		else
		{
		    if(x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
			shouldSwitch = true;
			break;
		    }
		}
	    }
	    
	}
	if(shouldSwitch) {
	    rows[i].parentNode.insertBefore(rows[i+1], rows[i]);
	    switching = true;
	    nswitches++;
	}
	else
	{
	    if (nswitches ==0 && ascending)
	    {
		ascending = false;
		switching = true;
	    }
	}
      }    
  };
