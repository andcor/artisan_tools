import typer
from typing_extensions import Annotated
from typing import Optional

import artisan_tools.vcs.main

import artisan_tools


def factory(app):
    """
    Create CLI for vcs extension.
    """
    cli = typer.Typer(name="vcs", help="Tools for version control system")

    @cli.command()
    def check_no_tag(
        tag: str = typer.Argument(  # noqa: B008
            ..., help="The tag to check in the remote repository."
        ),
    ):
        """
        Check if a specific tag exists in the remote Git repository.
        """
        if artisan_tools.vcs.main.check_tag(tag):
            typer.secho(
                f"Tag '{tag}' already exists in the remote repository.",
                fg=typer.colors.RED,
                bold=True,
            )
            raise typer.Exit(code=1)


    @cli.command()
    def check_clean():
        """
        Check if the current working directory is clean (no uncommitted changes).
        """
        if artisan_tools.vcs.main.check_clean():
            print("Working directory is clean.")
            raise typer.Exit(code=0)
        else:
            print("Working directory is not clean.")
            raise typer.Exit(code=1)


    @cli.command()
    def check_not_ahead():
        """
        Check if the current branch is not ahead of the remote branch.
        """
        if artisan_tools.vcs.main.check_not_ahead():
            print("Current branch is not ahead of the remote branch.")
            raise typer.Exit(code=0)
        else:
            print("Current branch is ahead of the remote branch.")
            raise typer.Exit(code=1)


    @cli.command()
    def check_branch(
        expected_branch: str = typer.Argument(  # noqa: B008
            ..., help="The branch name to check."
        ),
    ):
        """
        Check if the current Git branch is the specified branch.
        """
        if artisan_tools.vcs.main.check_current_branch(expected_branch):
            print(f"Current branch is '{expected_branch}'.")
            raise typer.Exit(code=0)
        else:
            print(f"Current branch is not '{expected_branch}'.")
            raise typer.Exit(code=1)

    @cli.command()
    def add_tag(tag: Annotated[Optional[str], typer.Argument()] = "v@version"):
        """
        Add a tag to the current commit and push it to remote git repository.

        Parameters
        ----------
        tag : str
            The tag to add. The tag is parsed by the parser extension. Default
            is 'v@version', which will render as e.g. 'v1.0.0'.

        """
        parser = app.get_extension("parser")
        tag = parser.parse(app, tag)
        check_no_tag(tag)

        artisan_tools.vcs.main.add_and_push_tag(
            app.config["vcs"], tag_name=tag, message=f"Add tag '{tag}'"
        )
        typer.echo(
            f"Tagged current changeset as '{tag}' and pushed to remote repository."
        )

    return cli
