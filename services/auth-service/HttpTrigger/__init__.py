import azure.functions as func
from azure.functions import AsgiMiddleware
from src.main import app

def main(req: func.HttpRequest, context: func.Context):
    return AsgiMiddleware(app).handle(req, context)
