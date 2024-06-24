import io
import os
import argparse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from omniparse import load_omnimodel
from omniparse.documents.router import document_router
from omniparse.media.router import media_router
from omniparse.image.router import image_router
from omniparse.web.router import website_router
# logging.basicConfig(level=logging.DEBUG)

# app = FastAPI(lifespan=lifespan)
app = FastAPI()

def add(app: FastAPI):
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

# Include routers in the main app
app.include_router(document_router, prefix="/parse_document", tags=["Documents"])
app.include_router(image_router, prefix="/parse_image" ,tags=["Images"] )
app.include_router(media_router, prefix="/parse_media", tags=["Media"])
app.include_router(website_router, prefix="/parse_website", tags=["Website"])

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run the marker-api server.")
    parser.add_argument("--host", default="0.0.0.0", help="Host IP address")
    parser.add_argument("--port", type=int, default=8000, help="Port number")
    parser.add_argument("--documents", action='store_true', help="Load document models")
    parser.add_argument("--media", action='store_true', help="Load media models")
    parser.add_argument("--web", action='store_true', help="Load web models")
    args = parser.parse_args()

    # Set global variables based on parsed arguments
    load_omnimodel(args.documents, args.media, args.web)
    
    # Conditionally include routers based on arguments
    app.include_router(document_router, prefix="/parse_document", tags=["Documents"] ,include_in_schema=args.documents)
    app.include_router(image_router, prefix="/parse_image", tags=["Images"] , include_in_schema=args.documents)
    app.include_router(media_router, prefix="/parse_media", tags=["Media"], include_in_schema=args.media)
    app.include_router(website_router, prefix="/parse_website", tags=["Website"], include_in_schema=args.web)
    # Start the server
    import uvicorn
    uvicorn.run("server:app", host=args.host, port=args.port)

if __name__ == "__main__":
    main()