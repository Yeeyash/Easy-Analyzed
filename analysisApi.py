import pandas as pd
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.formparsers import MultiPartParser
from io import BytesIO
import io, base64

import matplotlib.pyplot as plt

# Setting spool size to 10MB, This allows files below 10MB to be processed in Memory, else Disk.
MultiPartParser.spool_max_size = 10 * 1024 * 1024

fast = FastAPI()

fast.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@fast.post('/')
async def generateGraph(request: Request, file: UploadFile = File(...)):
    fileContent = await file.read()
    bytesContent = BytesIO(fileContent)

    # formContent = await request.form()

    df = pd.read_csv(bytesContent)

    fig, ax = plt.subplots()
    ax.plot(df["Name"], df["Sports"])

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    imgBytes = buf.read()
    img64 = base64.b64encode(imgBytes).decode('utf-8')

    return JSONResponse(content={"plot": f"data:img/png;base64,{img64}"})
