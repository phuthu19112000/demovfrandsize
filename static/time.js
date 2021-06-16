var nods = document.getElementsByClassName('aligh');
for (var i = 0; i < nods.length; i++)
{
    nods[i].attributes['src'].value += "?a=" + Math.random();
}
