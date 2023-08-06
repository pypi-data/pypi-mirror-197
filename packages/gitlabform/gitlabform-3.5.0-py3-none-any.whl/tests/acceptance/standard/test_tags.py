import pytest

from gitlabform.gitlab import AccessLevel
from tests.acceptance import (
    run_gitlabform,
)


@pytest.fixture(scope="function")
def tags(request, gitlab, group_and_project):
    tags = [
        "tag1",
        "tag2",
        "tag3",
    ]
    for tag in tags:
        gitlab.create_tag(group_and_project, tag, "main")

    def fin():
        protected_tags = gitlab.get_protected_tags(group_and_project)
        for protected_tag in protected_tags:
            gitlab.unprotect_tag(group_and_project, protected_tag["name"])
        for tag in tags:
            gitlab.delete_tag(group_and_project, tag)

    request.addfinalizer(fin)


class TestTags:
    def test__protect_single_tag(self, gitlab, group_and_project, tags):
        config = f"""
        projects_and_groups:
          {group_and_project}:
            tags:
              tag1:
                protected: true
                create_access_level: {AccessLevel.MAINTAINER.value}
        """

        run_gitlabform(config, group_and_project)

        tags = gitlab.get_tags(group_and_project)
        for tag in tags:
            if tag["name"] == "tag1":
                assert tag["protected"]
            else:
                assert not tag["protected"]

        protected_tags = gitlab.get_protected_tags(group_and_project)
        assert len(protected_tags) == 1
        assert protected_tags[0]["name"] == "tag1"
        assert (
            protected_tags[0]["create_access_levels"][0]["access_level"]
            == AccessLevel.MAINTAINER.value
        )

    def test__protect_wildcard_tag(self, gitlab, group_and_project, tags):
        config = f"""
        projects_and_groups:
          {group_and_project}:
            tags:
              "tag*":
                protected: true
                create_access_level: {AccessLevel.MAINTAINER.value}
        """

        run_gitlabform(config, group_and_project)

        tags = gitlab.get_tags(group_and_project)
        for tag in tags:
            assert tag["protected"]

        protected_tags = gitlab.get_protected_tags(group_and_project)
        assert len(protected_tags) == 1
        assert protected_tags[0]["name"] == "tag*"
        assert (
            protected_tags[0]["create_access_levels"][0]["access_level"]
            == AccessLevel.MAINTAINER.value
        )

    def test__unprotect_the_same_tag(self, gitlab, group_and_project, tags):
        config = f"""
        projects_and_groups:
          {group_and_project}:
            tags:
              "tag*":
                protected: true
                create_access_level: {AccessLevel.MAINTAINER.value}
        """

        run_gitlabform(config, group_and_project)

        tags = gitlab.get_tags(group_and_project)
        for tag in tags:
            assert tag["protected"]

        protected_tags = gitlab.get_protected_tags(group_and_project)
        assert len(protected_tags) == 1
        assert protected_tags[0]["name"] == "tag*"
        assert (
            protected_tags[0]["create_access_levels"][0]["access_level"]
            == AccessLevel.MAINTAINER.value
        )

        config = f"""
        projects_and_groups:
          {group_and_project}:
            tags:
              "tag*":
                protected: false
        """

        run_gitlabform(config, group_and_project)

        tags = gitlab.get_tags(group_and_project)
        for tag in tags:
            assert not tag["protected"]

        protected_tags = gitlab.get_protected_tags(group_and_project)
        assert len(protected_tags) == 0

    def test__protect_single_tag_no_access(self, gitlab, group_and_project, tags):
        config = f"""
            projects_and_groups:
              {group_and_project}:
                tags:
                  tag1:
                    protected: true
                    create_access_level: {AccessLevel.NO_ACCESS.value}
            """

        run_gitlabform(config, group_and_project)

        tags = gitlab.get_tags(group_and_project)
        for tag in tags:
            if tag["name"] == "tag1":
                assert tag["protected"]
            else:
                assert not tag["protected"]

        protected_tags = gitlab.get_protected_tags(group_and_project)
        assert len(protected_tags) == 1
        assert protected_tags[0]["name"] == "tag1"
        assert (
            protected_tags[0]["create_access_levels"][0]["access_level"]
            == AccessLevel.NO_ACCESS.value
        )

    def test__protect_single_tag_with_access_level_names(
        self, gitlab, group_and_project, tags
    ):
        config = f"""
            projects_and_groups:
              {group_and_project}:
                tags:
                  tag1:
                    protected: true
                    create_access_level: maintainer
            """

        run_gitlabform(config, group_and_project)

        tags = gitlab.get_tags(group_and_project)
        for tag in tags:
            if tag["name"] == "tag1":
                assert tag["protected"]
            else:
                assert not tag["protected"]

        protected_tags = gitlab.get_protected_tags(group_and_project)
        assert len(protected_tags) == 1
        assert protected_tags[0]["name"] == "tag1"
        assert (
            protected_tags[0]["create_access_levels"][0]["access_level"]
            == AccessLevel.MAINTAINER.value
        )
