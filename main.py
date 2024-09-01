from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
import pandas as pd
from io import StringIO
import random as rd
import secrets

app = FastAPI()

# Security setup (if needed for future endpoints)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Example root endpoint
@app.get("/")
async def root():
    return {"example": "hello", 'data': 0}

# Random number endpoint without limit
@app.get("/random")
async def get_random():
    rn: int = rd.randint(0, 100)
    return {'number': rn, 'limit': 100}

# Random number endpoint with a custom limit
@app.get("/random/{limit}")
async def get_random_limit(limit: int):
    rn: int = rd.randint(0, limit)
    return {'number': rn, 'limit': limit}

# Function to modify rows
def modify_rows(row):
    modified_rows = []
    modified_rows.append({
        'ID': row['ID'],
        'Item Tax Template (Taxes)': "Philippines Tax Exempt - ADC",
        'Tax Category (Taxes)': "Vat-In"
    })
    modified_rows.append({
        'ID': "",
        'Item Tax Template (Taxes)': "Senior Citizen Tax Ex",
        'Tax Category (Taxes)': "Senior Vat-Ex"
    })
    modified_rows.append({
        'ID': "",
        'Item Tax Template (Taxes)': "Zero Rated Ex - ADC",
        'Tax Category (Taxes)': "Zero Rated"
    })
    return modified_rows

# CSV processing endpoint
@app.post("/process-csv/")
async def process_csv(file: UploadFile = File(...)):
    # Read the uploaded file
    content = await file.read()
    df = pd.read_csv(StringIO(content.decode('utf-8')))
    
    # Apply the modify_rows function
    new_rows = df.apply(modify_rows, axis=1).explode().reset_index(drop=True)
    
    # Create a new DataFrame with the modified rows
    df_modified = pd.DataFrame(new_rows.tolist())
    
    # Convert the modified DataFrame to CSV
    output = StringIO()
    df_modified.to_csv(output, index=False)
    output.seek(0)
    
    # Return the CSV as a downloadable response
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=modified_file.csv"})

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
