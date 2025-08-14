# ✅ Use a minimal, secure Python base image
FROM python:3.11-slim

# ✅ Set working directory inside container
WORKDIR /app

# ✅ Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# ✅ Install dependencies (disable cache for smaller image)
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy the full source code AFTER dependencies
COPY . .

# ✅ Expose the app port (Uvicorn default)
EXPOSE 8000

# ✅ Run FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
