/* Agrega un requerimiento al arreglo */
function addReq()
{
	var new_req = $( "#txt_add_req" ).val();
	$( "#txt_add_req" ).val("");
	req.push( new_req );
	printReq();
}

/* Imprimer el arreglo en el html */
function printReq()
{
	var html = "<input type='hidden' name='count' value='" + req.length + "'>";
	for( var i = 0; i < req.length; i++ )
	{
		html += "<li>" + req[i] + "&nbsp;<a id='" + i + "' href='#' onclick='removeItem(this.id);'>Eliminar</a><input type = 'hidden' name='req_" + i + "' value = '" + req[i] + "'</li>";
	}
	$( "#table" ).html( html );
}

/* Borra un elemento */
function removeItem( id )
{
	req.splice( id, 1 );
	printReq();
}

var req = new Array();
