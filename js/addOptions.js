function loadComboBox()
{
	var text = "";
	for( var i = 0; i < arquitecture.length; i++ )
	{
		text += "<option value=" + i + ">" + arquitecture[i] + "</option>";
	}
	$("#arq").html(text);

	text = "";
	for( var i = 0; i < language.length; i++ )
	{
		text += "<option value=" + i + ">" + language[i] + "</option>";
	}
	$("#language").html(text);
}

var arquitecture = ["MVC", "Layer", "Objec Oriented"];
var language = ["C++", "C#", "JAVA", "Python", "COBOL"];