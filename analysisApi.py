import pandas as pd
import numpy as np
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.formparsers import MultiPartParser
from io import BytesIO
import io, base64

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Setting spool size to 10MB, This allows files below 10MB to be processed in Memory, else Disk.
# MultiPartParser.spool_max_size = 10 * 1024 * 1024
MultiPartParser.spool_max_size = 70 * 1024 * 1024

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

    dfQuantitative = []
    dfQualitative = []

    for i in df.columns:
        if pd.api.types.is_numeric_dtype(df[i]):
            dfQuantitative.append(i)
        else:
            dfQualitative.append(i)

    availableColumns = dfQualitative + dfQuantitative

    return JSONResponse(content={"availableColumns": availableColumns, "qualitative": dfQualitative, "quantitative": dfQuantitative})

@fast.post('/plot')
async def plots(request: Request, file: UploadFile = File(...)):
    fileContent = await file.read()
    bytesContent = BytesIO(fileContent)
    formContent = await request.form()
    colInput = formContent.get("input_text") #

    # splitCols = colInput.split(',')
    tempX, tempy = map(str, colInput.split(','))
    tempX = tempX.strip()
    tempy = tempy.strip()

    # str(x, y)
    # x, y = splitCols[0], splitCols[1]
    # print(x, y)
    # y: numerical/quantitative, x: qualitative.

    df = pd.read_csv(bytesContent)

    dfQuantitative = []
    dfQualitative = []

    for i in df.columns:
        if pd.api.types.is_numeric_dtype(df[i]):
            dfQuantitative.append(i)
        else:
            dfQualitative.append(i)


    if tempX in dfQualitative:
        x = tempX
        y = tempy
    else:
        y = tempX
        x = tempy

    x = np.array(df[x])
    y = np.array(df[y])

    Nx = len(x)
    Ny = len(y)
    
    # Line Plot
    fig, ax = plt.subplots()
    ax.plot(x, y, markevery=10) #df["Name"] -> df[dfQualitative[0]], Expects series and not an array.

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    imgBytes = buf.read()
    img64 = base64.b64encode(imgBytes).decode('utf-8')

    # Bar Plot

    barFig, barAx = plt.subplots()

    buf2 = io.BytesIO()

    barAx.bar(x, y, width=1)
    barFig.savefig(buf2, format='png')
    plt.close(barFig)
    buf2.seek(0)

    barImgbytes = buf2.read()
    barImg64 = base64.b64encode(barImgbytes).decode('utf-8')


    # Pie Plot
    # Pie charts need numerical data to make and respective lables as well.

    # pieFig, pieAx = plt.subplots()
    # pieAx.pie(df[y], labels=df[x])
    # pieAx.axis("equal")

    # buf3 = io.BytesIO()
    # pieFig.savefig(buf3, format='png')
    # plt.close(pieFig)
    # buf3.seek(0)

    # pieImgbytes = buf3.read()
    # pieImg64 = base64.b64encode(pieImgbytes).decode('utf-8')

    # Scatter

    ScatterFig, ScatterAx = plt.subplots()

    buf4 = io.BytesIO()

    sampleSize = 3000
    sampleSize = min(sampleSize, Nx, Ny)
    indices = np.random.choice(len(x), sampleSize, replace=False)

    ScatterAx.scatter(x[indices], y[indices], alpha=0.5)
    # ScatterAx.scatter(x, y)
    ScatterFig.savefig(buf4, format='png')
    plt.close(ScatterFig)
    buf4.seek(0)

    scatterImgbytes = buf4.read()
    scatterImg64 = base64.b64encode(scatterImgbytes).decode('utf-8')
    
    # Histogram

    histFig, histAx = plt.subplots()
    
    buf5 = io.BytesIO()
    
    histAx.hist(y, bins=10)
    histFig.savefig(buf5, format='png')
    plt.close(histFig)
    buf5.seek(0)

    histImgBytes = buf5.read()
    histImg64 = base64.b64encode(histImgBytes).decode('utf-8')

    # print(pieImg64.__sizeof__() + barImg64.__sizeof__() + img64.__sizeof__()) #72730 bytes for testFile.

    return JSONResponse(content={"plot1": f"data:img/png;base64,{img64}", "plot2": f"data:img/png;base64,{barImg64}", "plot3": f"data:img/png;base64,{"pieImg64"}", "plot4": f"data:img/png;base64,{scatterImg64}", "plot5": f"data:img/png;base64,{histImg64}","availableColumns": dfQualitative + dfQuantitative})