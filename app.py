from fastapi import FastAPI, Form, Request, Response, File, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from jinja2 import Environment, FileSystemLoader, select_autoescape
import uvicorn
import os
import aiofiles
import json
import csv
from src.qanda.utils import llm_pipeline

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Create a Jinja2 environment with caching disabled
jinja_env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape(), cache_size=0)
templates = Jinja2Templates(env=jinja_env)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})


@app.post("/upload")
async def chat(request: Request, pdf_file: bytes = File(), filename: str = Form(...)):
    base_folder = 'static/docs/'
    if not os.path.isdir(base_folder):
        os.makedirs(base_folder)

    pdf_filename = os.path.join(base_folder,filename)

    async with aiofiles.open(pdf_filename,'wb') as asyncfile:
        await asyncfile.write(pdf_file)
        await asyncfile.flush()
    
    response_data = jsonable_encoder(json.dumps({"msg":"success","pdf_filename":pdf_filename}))
    return Response(content=response_data)


def get_csv(file_path):
    questions,answer_chain = llm_pipeline(file_path)

    base_folder = 'static/output'
    if not os.path.isdir(base_folder):
        os.makedirs(base_folder)

    output_file = base_folder+"QA.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Question", "Answer"])

        for question in questions:
            answer = answer_chain.invoke(question)
            csv_writer.writerow([question, answer])

    return output_file


@app.post("/analyze")
async def analyze(request: Request, pdf_filename: str = Form(...)):
    output_file = get_csv(pdf_filename)
    response_data = jsonable_encoder(json.dumps({"msg":"success","output_file":output_file}))
    return Response(content=response_data)


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)