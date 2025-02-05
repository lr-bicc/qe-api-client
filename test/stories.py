from qe_api_client.engine import QixEngine


url = 'ws://localhost:4848/app'
qixe = QixEngine(url=url)

# App ID holen
# doc_id = "f9e79d92-652b-4ba8-8487-84e2825b71c5"     # Sales KPI
doc_id = "Stories.qvf"

# App öffnen
opened_doc = qixe.ega.open_doc(doc_id)
# print(opened_doc)

doc_handle = qixe.get_handle(opened_doc)
print(doc_handle)

child_list_def = {"qData": {"title": "/title", "description": "/description", "children": "/qChildListDef"}}
story = qixe.eaa.create_object(doc_handle, "story02", "story", "qChildListDef", child_list_def)
print(story)

story_handle = qixe.get_handle(story)
print(story_handle)

child_list_def = {"title": "Slide 01", "description": "This is the slide 02", "qInfo": {"qId": "slide01", "qType": "slide"}, "qChildListDef": {"qData": {"title": "/title"}}}
slide = qixe.egoa.create_child(story_handle, child_list_def)
print(slide)