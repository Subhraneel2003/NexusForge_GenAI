# database/db_manager.py
import os
import chromadb
from chromadb.config import Settings

class DatabaseManager:
    def __init__(self, collection_name="dev_pod"):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(name=collection_name)
        
    def store_artifact(self, artifact_id, artifact_content, metadata=None):
        """Store an artifact in the database"""
        if metadata is None:
            metadata = {}
            
        self.collection.add(
            documents=[str(artifact_content)],
            metadatas=[metadata],
            ids=[artifact_id]
        )
        return artifact_id
        
    def get_artifact(self, artifact_id):
        """Retrieve an artifact from the database"""
        results = self.collection.get(ids=[artifact_id])
        if results and results['documents']:
            return results['documents'][0]
        return None
        
    def get_artifacts_by_type(self, artifact_type):
        """Get all artifacts of a specific type"""
        results = self.collection.query(
            query_texts=[""],
            where={"type": artifact_type},
            include=["documents", "metadatas"]
        )
        return results
        
    def update_artifact(self, artifact_id, artifact_content, metadata=None):
        """Update an existing artifact"""
        # First delete the existing entry
        self.collection.delete([artifact_id])
        # Then add the updated version
        return self.store_artifact(artifact_id, artifact_content, metadata)
        
    def get_all_artifacts(self):
        """Get all artifacts in the database"""
        results = self.collection.get()
        return results