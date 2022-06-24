from devind_helpers.permissions import ModelPermission


AddDocument = ModelPermission('dcis.add_document')
ChangeDocument = ModelPermission('dcis.change_document')
DeleteDocument = ModelPermission('dcis.delete_document')

AddDocumentStatus = ModelPermission('dcis.add_documentstatus')
DeleteDocumentStatus = ModelPermission('dcis.delete_documentstatus')
