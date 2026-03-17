# Dataset routes handle the uploading and management of datasets.
# The /upload endpoint allows users to upload a dataset file, which is then processed and stored in the database.
# The endpoint accepts a file upload and uses the Dataset model to save metadata about the uploaded dataset, such as the filename and upload timestamp. 
# The actual file handling (e.g., saving the file to disk or cloud storage) would be implemented in the route handler, but is not shown in this snippet.


from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import pandas as pd
import shutil
import os
import re

from app.database import get_db
from app.models.dataset import Dataset
from app.models.column import DatasetColumn
from app.utils.classifier import classify_column
from app.utils.classifier import detect_sensitive_data
from rapidfuzz import fuzz


router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"]
)

UPLOAD_FOLDER = "uploads"


@router.post("/upload")
def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file_path = f"{UPLOAD_FOLDER}/{file.filename}"

    # -----------------------------
    # STEP 1: Save uploaded file
    # -----------------------------
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -----------------------------
    # STEP 2: Save dataset metadata in database
    # -----------------------------
    dataset = Dataset(filename=file.filename)
    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    # Store column processing results
    columns_result = []

    # -----------------------------
    # STEP 3: Detect file type
    # -----------------------------
    if file.filename.endswith(".csv"):

        df = pd.read_csv(file_path)

        # -----------------------------
        # STEP 4: Column Processing Loop
        # -----------------------------
        for column in df.columns:

            # Detect category based on column name
            category = classify_column(column)

            # Get sample value from column
            sample_value = None
            if not df[column].dropna().empty:
                sample_value = df[column].dropna().iloc[0]

            # Detect sensitive data type
            detected_type = detect_sensitive_data(sample_value)

            # Save column info in database
            column_entry = DatasetColumn(
                dataset_id=dataset.id,
                column_name=column,
                detected_type=detected_type,
                Category=category
            )

            db.add(column_entry)

            # Store result for API response
            columns_result.append({
                "column_name": column,
                "category": category,
                "detected_type": detected_type,
                "sample_value": str(sample_value)
            })

    # -----------------------------
    # STEP 5: Excel File Processing
    # -----------------------------
    elif file.filename.endswith(".xlsx"):

        sheets = pd.read_excel(file_path, sheet_name=None)

        # Loop through each sheet
        for sheet_name, df in sheets.items():

            # Column Processing Loop
            for column in df.columns:

                # Detect category based on column name
                category = classify_column(column)

                # Get sample value from column
                sample_value = None
                if not df[column].dropna().empty:
                    sample_value = df[column].dropna().iloc[0]

                # Detect sensitive data type
                detected_type = detect_sensitive_data(sample_value)

                # Save column info in database
                column_entry = DatasetColumn(
                    dataset_id=dataset.id,
                    column_name=f"{sheet_name}.{column}",
                    detected_type=detected_type,
                    Category=category
                )

                db.add(column_entry)

                # Store result for API response
                columns_result.append({
                    "sheet": sheet_name,
                    "column_name": column,
                    "category": category,
                    "detected_type": detected_type,
                    "sample_value": str(sample_value)
                })

     # =============================
    # EXCEL FILE PROCESSING
    # =============================
    elif file.filename.endswith(".xlsx"):

        sheets = pd.read_excel(file_path, sheet_name=None)

        for sheet_name, df in sheets.items():

            for column in df.columns:

                # Detect category
                category = classify_column(column)

                # Get sample value
                sample_value = None
                if not df[column].dropna().empty:
                    sample_value = df[column].dropna().iloc[0]

                # Detect sensitive data
                detected_type = detect_sensitive_data(sample_value)

                # Save column metadata
                column_entry = DatasetColumn(
                    dataset_id=dataset.id,
                    column_name=f"{sheet_name}.{column}",
                    detected_type=detected_type,
                    Category=category
                )

                db.add(column_entry)

                columns_result.append({
                    "sheet": sheet_name,
                    "column_name": column,
                    "category": category,
                    "detected_type": detected_type,
                    "sample_value": str(sample_value)
                })

    # =============================
    # SQL FILE PROCESSING
    # =============================
    elif file.filename.endswith(".sql"):

        with open(file_path, "r", encoding="utf-8") as f:
            sql_content = f.read()

        # Extract column definitions
        matches = re.findall(r"\((.*?)\)", sql_content, re.DOTALL)

        if matches:

            columns_block = matches[0]
            columns = columns_block.split(",")

            for col in columns:

                column = col.strip().split()[0]

                # Detect category
                category = classify_column(column)

                # SQL files don't have sample values
                sample_value = None

                # Detect sensitive type based on column name
                detected_type = detect_sensitive_data(column)

                column_entry = DatasetColumn(
                    dataset_id=dataset.id,
                    column_name=column,
                    detected_type=detected_type,
                    Category=category
                )

                db.add(column_entry)

                columns_result.append({
                    "column_name": column,
                    "category": category,
                    "detected_type": detected_type,
                    "sample_value": None
                })

    else:
        return {"error": "Unsupported file format"}


    # -----------------------------
    # STEP 6: Commit all column data
    # -----------------------------
    db.commit()

    # -----------------------------
    # STEP 7: Return response
    # -----------------------------
    return {
        "message": "Dataset uploaded successfully",
        "dataset_id": dataset.id,
        "columns": columns_result
    }
# Additional endpoints for dataset management (e.g., listing datasets, deleting datasets) would be implemented here.








    
















