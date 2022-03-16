var fechaCaledario = null;
var enviar = true;

function editarCapitulo(nombre,url,id){
	document.formCapitulo.nombre.value=nombre;
	document.formCapitulo.id_capitulo.value=id;
	document.formCapitulo.action=url;
}

function agregaTitulo(id_titulo) {
	document.formTitulo.id_titulo.value = id_titulo;
}

function editaTitulo(nombre,url,id){
	document.formTitulo.nombre.value=nombre;
	document.formTitulo.id_titulo.value=id;
	document.formTitulo.action=url;
}
function guardaTitulo() {
	document.formTitulo.submit();
}

function agregaSubtitulo(id_subtitulo) {
	document.formSubtitulo.id_subtitulo.value = id_subtitulo;
}
function editaSubtitulo(nombre,url,id){
	document.formSubtitulo.nombre.value=nombre;
	document.formSubtitulo.id_subtitulo.value=id;
	document.formSubtitulo.action=url;
}
function guardarSubtitulo() {
	document.formSubtitulo.submit();
}

function agregaFecha(tipo, id) {
	enviar = true;
	var form = document.formAgenda;
	form.tipo.value = tipo;
	form.id_tipo.value = id;
}
function eliminaFecha(tipo, id, url) {

	var form = document.formAgenda;
	form.tipo.value = tipo;
	form.id_tipo.value = id;
	form.action = url;
	form.submit();

}

function soloMuestra() {
	enviar = false;
}
function setHora(hora){
	if (enviar){
		var form = document.formAgenda;
		form.fecha.value = fechaCaledario+" "+hora;
		form.submit();
	}
}

function setFecha(fecha){
	var  hoy = new Date()

	fechaHoy = new Date(hoy);
	fechaSel = new Date(fecha)
	fechaSel.setDate (fechaSel.getDate() + 1);

	if (fechaSel < fechaHoy){
		alert("La fecha de entrega no puede ser antes del día de hoy");
		document.getElementById("btnMes").click();

		return false;
	}
	else{
		fechaCaledario = fecha;
	}
}

function nuevoEntregable(tipo, id) {
	enviar = true;
	var form = document.formEntregable;
	form.tipo.value = tipo;
	form.id_tipo.value = id;
}

function muestraEntregable(url,fecha,fechaEntrega,archivo,titulo, porcentaje) {
	var form = document.formMuestraEntregable;
	form.fecha.value = fecha;
	form.fecha_entrega.value = fechaEntrega;

	document.getElementById('link_entregable').href=url;

	document.getElementById('link_entregable').innerText=archivo;
	document.getElementById('tituloModalMuestra').innerText=titulo;
	document.getElementById('porcentaje').innerText = porcentaje;

	document.getElementById('porcentaje').style.width = porcentaje+"%";

}

function revisaEntregable(tipo,id,url,fecha,fechaEntrega,archivo,titulo,porcentaje) {
	var form = document.formEvaluarEntregable;
	form.fecha.value = fecha;
	form.fecha_entrega.value = fechaEntrega;
	document.getElementById('link_entregable').href=url;

	document.getElementById('link_entregable').innerText=archivo;
	document.getElementById('tituloModalMuestra').innerText+=titulo;
	form.id_tipo.value = id;
	form.tipo.value = tipo;
	form.porcentaje.value=porcentaje;
}

function mueveCapitulo(id,url,orden){
	document.formCapitulo.id_capitulo.value = id;
	document.formCapitulo.action = url;
	document.formCapitulo.orden.value = orden;
	document.formCapitulo.submit();

}

function mueveTitulo(id,url,orden){
	document.formTitulo.id_titulo.value = id;
	document.formTitulo.action = url;
	document.formTitulo.orden.value = orden;
	document.formTitulo.submit();

}

function mueveSubtitulo(id,url,orden){
	document.formSubtitulo.id_subtitulo.value = id;
	document.formSubtitulo.action = url;
	document.formSubtitulo.orden.value = orden;
	document.formSubtitulo.submit();

}

function mostrarModal(id,urlDestino){
	$.ajax({
		data : {'id':id},
		url : urlDestino,
		type : 'get',
		success: function(data){
		var html=""
		    if (data.tipo_notificacion == 1){
		        html = "<h1>Notificación</h1><p>El usuario "+data.usuario_crea+data.descripcion+"</p>";
			    html += "<a href='/usuarios/"+data.id_accion+"/Evaluar/' type='button' class='btn btn-primary'>Revisar</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
			    html += "<button type='button' class='btn btn-primary' data-dismiss='modal'>Aceptar</button>";
		    }
		    if (data.tipo_notificacion == 2){
		        html = "<h1>Notificación</h1><p>El usuario "+data.usuario_crea+data.descripcion+"</p>";
			    html += "<a href='/plantillas/entregables' type='button' class='btn btn-primary'>Revisar</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
			    html += "<button type='button' class='btn btn-primary' data-dismiss='modal'>Aceptar</button>";
		    }
		    if (data.tipo_notificacion == 3){
		        html = "<h1>Notificación</h1><p>El usuario "+data.usuario_crea+data.descripcion+"</p>";
			    html += "<a href='/plantillas/entregables/' type='button' class='btn btn-primary'>Revisar</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
			    html += "<button type='button' class='btn btn-primary' data-dismiss='modal'>Aceptar</button>";
		    }
		    if (data.tipo_notificacion == 4){
		        html = "<h1>Notificación</h1><p>El usuario "+data.usuario_crea+data.descripcion+"</p>";
			    html += "<button type='button' class='btn btn-primary' data-dismiss='modal' >Aceptar</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
			    html += "<button type='button' class='btn btn-primary' data-dismiss='modal' onclick='cancelarAsesor("+data.usuario_crea_id+")'>Cancelar</button>";
		    }
		    if (data.tipo_notificacion == 5){
		        html = "<h1>Notificación</h1><p>El usuario "+data.usuario_crea+data.descripcion+"</p>";
			    html += "<a href='/plantillas/"+data.id_accion+"/verPlantillaLeer' type='button' class='btn btn-primary'>Revisar</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
			    html += "<button type='button' class='btn btn-primary' data-dismiss='modal'>Aceptar</button>";
		    }
		    if (data.tipo_notificacion == 6){
		        html = "<h1>Notificación</h1><p>El usuario "+data.usuario_crea+data.descripcion+"</p>";
			    html += "<button type='button' class='btn btn-primary' data-dismiss='modal'>Aceptar</button>";
		    }
		    if (data.tipo_notificacion == 7){
		        html = "<h1>Notificación</h1><p>El usuario "+data.usuario_crea+data.descripcion+"</p>";
			    html += "<button type='button' class='btn btn-primary' data-dismiss='modal' >Aceptar</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
			    html += "<button type='button' class='btn btn-primary' data-dismiss='modal' onclick='cancelarTesista("+data.usuario_crea_id+")'>Cancelar</button>";
		    }
		    if (data.tipo_notificacion == 8){
		        html = "<h1>Notificación</h1><p>El usuario "+data.usuario_crea+data.descripcion+"</p>";
			    html += "<button type='button' class='btn btn-primary' data-dismiss='modal'>Aceptar</button>";
		    }
		    if (data.tipo_notificacion == 9){
		        html = "<h1>Notificación</h1><p>El usuario "+data.usuario_crea+data.descripcion+"</p>";
			    html += "<button type='button' class='btn btn-primary' data-dismiss='modal'>Aceptar</button>";
		    }
		    if (data.tipo_notificacion == 10){
		        html = "<h1>Notificación</h1><p>El usuario "+data.usuario_crea+data.descripcion+"</p>";
			    html += "<button type='button' class='btn btn-primary' data-dismiss='modal'>Aceptar</button>";
		    }
		    if (data.tipo_notificacion == 11){
		        html = "<h1>Notificación</h1><p>El usuario "+data.usuario_crea+data.descripcion+"</p>";
			    html += "<button type='button' class='btn btn-primary' data-dismiss='modal'>Aceptar</button>";
		    }
		    console.log(data);
			$('#divMostrar').html(html);
		},
		error : function(xhr,errmsg,err) {
	        console.log(xhr.responseText);
	    }
	});

}

function cancelarAsesor(idAsesor){
	$.ajax({
		data : {'idAsesor':idAsesor},
		url : "/notificaciones/cancelar_asesor",
		type : 'get',
		success: function(data){

		},
		error : function(xhr,errmsg,err) {
	        console.log(xhr.responseText);
	    }
	});

}

function cancelarTesista(idTesista){
	$.ajax({
		data : {'idTesista':idTesista},
		url : "/notificaciones/cancelar_tesista",
		type : 'get',
		success: function(data){

		},
		error : function(xhr,errmsg,err) {
	        console.log(xhr.responseText);
	    }
	});

}