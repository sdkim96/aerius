from .views import *

def set_routes(app: FastAPI):
    # app.post("/items/", response_model=Item)(create_item_endpoint)
    # app.get("/items/{item_id}", response_model=Item)(read_item_endpoint)
    app.post("/chatbot/")(post_query)