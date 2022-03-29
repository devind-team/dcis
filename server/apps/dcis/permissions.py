"""Модуль, описывающий доступные привилегии приложения."""

from devind_helpers.permissions import ModelPermission


AddProject = ModelPermission('dcis.add_project')
ChangeProject = ModelPermission('dcis.change_project')
DeleteProject = ModelPermission('dcis.delete_project')

AddPeriod = ModelPermission('dcis.add_period')
ChangePeriod = ModelPermission('dcis.change_period')
DeletePeriod = ModelPermission('dcis.delete_period')

AddDocument = ModelPermission('dcis.add_document')
ChangeDocument = ModelPermission('dcis.change_document')
DeleteDocument = ModelPermission('dcis.delete_document')

AddDocumentStatus = ModelPermission('dcis.add_documentstatus')
DeleteDocumentStatus = ModelPermission('dcis.delete_documentstatus')
