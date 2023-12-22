#%%
from pydiamonds.python_helpers import activate_ipython_magics
from llm_assistant import find_same_from_end, is_AI_called 
activate_ipython_magics()

last_text =  "Jól van, talán most már látható lesz. Látható lesz most már. Mennyire működik a jelenszéd."
text =  "Jól van, talán most már látható lesz. Látható lesz most már? Mennyire működik a jelenszín?"
# difference_in_last_text, difference_in_text = find_same_from_end(last_text, text)
# is_AI_called(text)
is_AI_called("Milyen az időjárás? Itt vagy Robot uram?", "Yes")
is_AI_called("Jól van, talán most már látható lesz. Mennyi 10 + 20? Itt vagy Robot uram?", "Yes")
is_AI_called("Milyen az időjárás? Can you answer?", "No")
# is_AI_called("Jól van, talán most már látható lesz. Látható lesz most már? Mennyire működik a jelenség? Itt Siri?")
is_AI_called("Jól van, talán most már látható lesz. Látható lesz most már? Mennyire működik a jelenség, Siri ", "Yes")
is_AI_called("Jól van, talán most már látható lesz. Mennyi 10 + 20? Siri? ", "Yes")
is_AI_called("Jól van, talán most már látható lesz. Mennyi 10 + 20 összege, AI Assistant? ", "Yes")
is_AI_called("Jól van, talán most már látható lesz. Mennyi 10 + 20 összege, Intelligencia? ", "Yes")
is_AI_called("Jól van, talán most már látható lesz. Látható lesz most már? Mennyire működik a jelenség?", "No")

text = "Talán most már látható lesz. Látható lesz most már. Mennyire mérkedik. Kérlek szépen jó példákat!"
is_AI_called(text, "No/Y?")
is_AI_called("A padláson maradt egy csomag, majd holnap le kéne hozni", "No")
is_AI_called("A padláson maradt egy csomag, majd holnap le kéne hozni. Rendben majd lehozom!", "No")

text = "Yes. Na, most már tényleg szeretném látni a helyet, mikor az érkezik. Jól van, talán most már látható lesz. Látható lesz most már."
is_AI_called(text, "No")
#%%
last_text =  "Jól van, talán most már látható lesz. Látható lesz most már? Mennyire működik a jelenszín?"
text = "Talán most már látható lesz. Látható lesz most már. Mennyire mérkedik. Kérlek szépen jó példákat."
difference_in_last_text, difference_in_text = find_same_from_end(last_text, text)
#%%
last_text = "Jó, és regisztrál. Yes. Na. Most már tényleg szeretném látni a helyet."
text =  "Jó, és regiszter. Yes. Na. Most már tényleg szeretném látni a helyet, mikor azért..."
# difference_in_last_text, difference_in_text = find_same_from_end(last_text, text)
is_AI_called(text)

last_text =  "Jól van, talán most már látható lesz. Látható lesz most már."
text =  "Jól van, talán most már látható lesz. Látható lesz most már. Mennyire lehet."
# difference_in_last_text, difference_in_text = find_same_from_end(last_text, text)
is_AI_called(text)


last_text =  "Jól van, talán most már látható lesz. Látható lesz most már. Mennyire lehet."
text =  "Jól van, talán most már látható lesz. Látható lesz most már? Mennyire működik?"
# difference_in_last_text, difference_in_text = find_same_from_end(last_text, text)
is_AI_called(text)

ltxt =  "Jó, és regiszter. Yes. Na. Most már tényleg szeretném látni a helyet. Jól van. Talán most már látható lesz."
text =  "Jó, és regisztráljuk. Na, most már tényleg szeretném látni a helyet. Jól van, talán most már látható lesz."
# difference_in_last_text, difference_in_text = find_same_from_end(ltxt, text)
is_AI_called(text)

last_text =  "Jó, és regisztráljuk. Na, most már tényleg szeretném látni a helyet. Jól van, talán most már látható lesz."
text =  "Jó, és regiszter, yes. Na, most már tényleg szeretném látni a helyet, meg azért nem tudom, hogy mit csinálok. Jól van, talán most már látható lesz."
# difference_in_last_text, difference_in_text = find_same_from_end(last_text, text)
is_AI_called(text)


last_text =  "Jó, és regiszter, yes. Na, most már tényleg szeretném látni a helyet, meg azért nem tudom, hogy mit csinálok. Jól van, talán most már látható lesz."
text =  "Na, most már tényleg szeretném látni a helyet. Jól van, talán most már látható lesz. Látható lesz most már."
# difference_in_last_text, difference_in_text = find_same_from_end(last_text, text)
is_AI_called(text)

