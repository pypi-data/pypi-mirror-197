"""
Document API.
"""
from algora.api.service.documents.asynchronous import (
    async_get_document,
    async_search_documents,
    async_create_document,
    async_update_document,
    async_delete_document,
)
from algora.api.service.documents.synchronous import (
    get_document,
    search_documents,
    create_document,
    update_document,
    delete_document,
)
