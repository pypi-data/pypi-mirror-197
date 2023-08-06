from supextend.core import MetastoreConnManager
from supextend.models.workspaces import Workspace
from supextend.resources.internal.workspace_extension import WorkspaceExtension
from supextend.loggers.config import LoggingConfig


class WorkspaceIntern(WorkspaceExtension):

    @staticmethod
    def list_intern_resource():
        return Workspace.query.all()

    def delete_intern_resource(self, pk):
        workspace = self.get_intern_resource(pk)
        title = workspace.title
        with MetastoreConnManager() as session:
            session.delete(workspace)
            session.commit()
            LoggingConfig.logger.success(f"Removed the workspace: {title}.")

    @staticmethod
    def create_intern_resource(title: str,
                               color: str,
                               created_by: str,
                               description: str
                               ):
        workspace = Workspace(
            title=title,
            color=color,
            created_by=created_by,
            description=description
        )
        with MetastoreConnManager() as session:
            session.add(workspace)
            session.commit()
            LoggingConfig.logger.success(f"Added the workspace: {title}.")
            return workspace

    @staticmethod
    def update_intern_resource(pk,
                               title: str,
                               color: str,
                               created_by: str,
                               description: str
                               ):
        workspace = Workspace.query.get_or_404(pk)
        workspace.title = title
        workspace.color = color
        workspace.created_by = created_by
        workspace.description = description

        with MetastoreConnManager() as session:
            session.commit()
            LoggingConfig.logger.success(f"Updated the workspace: {title}.")

    @staticmethod
    def get_intern_resource(pk):
        return Workspace.query.get(pk)

    def add_dashboards(self, workspace, dashboards):
        with MetastoreConnManager() as session:
            for dash in dashboards:
                print("TTTTTTTTTTTTTTTTTTTT", type(dash))
                workspace.dashboards.append(dash)
            session.commit()
            LoggingConfig.logger.success(f"Updated the workspace "
                                         f"with the following "
                                         f"dashboards: {dashboards}.")
