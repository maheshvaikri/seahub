# Copyright (c) 2012-2016 Seafile Ltd.

from django.db import models


class SharePermissionManager(models.Manager):
    def get_user_permission(self, repo_id, username):
        record_list = super(SharePermissionManager, self).filter(
            repo_id=repo_id, share_to=username
        )
        if len(record_list) > 0:
            return record_list[0].permission
        else:
            return None

    def can_delete_or_update_shared_records(self, repo_id, share_from, share_to):
        share_records = super(SharePermissionManager, self).filter(
            repo_id=repo_id, share_from=share_from, share_to=share_to
        )
        if len(share_records) > 0:
            return True
        else:
            return False

    def get_shared_repos_share_from_by_shared_with_admin(self, username):
        shared_repos = super(SharePermissionManager, self).filter(
            share_to=username, permission='admin'
        )
        res_shared_repos = {}
        for e in shared_repos:
            res_shared_repos[e.repo_id] = e.share_from
        return res_shared_repos

    def get_shared_repos_share_from_by_shared_with_preview(self, username):
        shared_repos = super(SharePermissionManager, self).filter(
            share_to=username, permission='preview'
        )
        res_shared_repos = {}
        for e in shared_repos:
            res_shared_repos[e.repo_id] = e.share_from
        return res_shared_repos

    def get_permission_by_owner_shared(self, repo_id, username):
        shared_repos = super(SharePermissionManager, self).filter(
            repo_id=repo_id, share_from=username
        )
        shared_repos = [(e.share_to, e.permission) for e in shared_repos]
        return shared_repos

    def create_share_permission(self, repo_id, share_from, username, permission):
        self.model(repo_id=repo_id, share_from=share_from, share_to=username, 
                   permission=permission).save()

    def delete_user_shared_repo(self, repo_id, share_from, share_to):
        super(SharePermissionManager, self).filter(repo_id=repo_id, 
                                                   share_from=share_from, 
                                                   share_to=share_to).delete()

    def update_share_permission(self, repo_id, share_from, share_to, permission):
        super(SharePermissionManager, self).filter(repo_id=repo_id, 
                                                   share_from=share_from, 
                                                   share_to=share_to).delete()
        self.create_share_permission(repo_id, share_from, share_to, permission)


class SharePermission(models.Model):
    repo_id = models.CharField(max_length=36, db_index=True)
    share_from = models.CharField(max_length=255, db_index=True)
    share_to = models.CharField(max_length=255, db_index=True)
    permission = models.CharField(max_length=30)
    objects = SharePermissionManager()
