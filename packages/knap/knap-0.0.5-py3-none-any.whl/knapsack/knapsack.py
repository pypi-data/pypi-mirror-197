from typing import Any, Dict, List

import typer
from requests.exceptions import JSONDecodeError
from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from knapsack.api import Api


app = typer.Typer()
api = Api()


def _display_tables(tables: List[Dict[str, Any]]) -> None:
    for display_table in tables:
        table = Table(
            title=display_table.get("title", ""),
            box=box.MINIMAL_DOUBLE_HEAD
        )

        columns = display_table.get("columns", [])
        for column in columns:
            table.add_column(
                column.get("title", ""),
                justify=column.get("justify", ""),
                style=column.get("style", ""),
                no_wrap=False
            )

        rows = display_table.get("rows", [])
        for row in rows:
            row_data = row.get("data", [])
            table.add_row(*row_data)

        console = Console()
        console.print(table)


def _display_tree(display_trees: List[Dict[str, Any]]) -> None:
    for display_tree in display_trees:
        tree = Tree(
            Text.assemble((display_tree.get("title", ""), "white")),
            guide_style="bold purple"
        )
        start_dataset = display_tree.get("start_dataset", {})
        data = display_tree.get("data", {})

        repro_tag = start_dataset.get("repro_tag", "")

        repro_tag_to_branch = {}
        next_tags = []
        if repro_tag != "":
            branch = tree.add(
                Text.assemble((repro_tag, "white"))
            )
            repro_tag_to_branch[repro_tag] = branch
            parent_data_list = data.get(repro_tag, [])
            next_tags.append((repro_tag, parent_data_list))

        while len(next_tags) > 0:
            (repro_tag, parent_data_list) = next_tags.pop()
            branch = repro_tag_to_branch[repro_tag]
            for i, parent_data in enumerate(parent_data_list):
                parent_repro_tag = parent_data.get("repro_tag", None)
                truncated_repro_tag = parent_repro_tag[:8]
                num_data_points = parent_data.get("num_data_points", 0)
                storage_used = parent_data.get("storage_used", 0.0)
                created_at = parent_data.get("created_at", "")
                new_branch = branch.add(
                    Text.assemble(
                        (f"{truncated_repro_tag} -- ", "white"),
                        (f"samples: +{num_data_points} ", "light_steel_blue"),
                        (" - ", "white"),
                        (f"storage(GB): +{storage_used}", "light_steel_blue1"),
                        (" - ", "white"),
                        (f"committed: {created_at}", "honeydew2"),
                    )
                )
                repro_tag_to_branch[parent_repro_tag] = new_branch
                next_tags.append((parent_repro_tag, data.get(parent_repro_tag, [])))

        console = Console()
        console.print(tree)


@app.command()
def me():
    table = {"title": "My orgs"}
    table["columns"] = [
        {
            "title": "Org name",
            "justify": "right",
            "style": "magenta",
        },
        {
            "title": "API key filename",
            "justify": "right",
            "style": "chartreuse1",
        },
    ]
    table["rows"] = []
    for org_name, _ in api.org_names_to_api_keys.items():
        if org_name:
            key_filename = api.org_names_to_key_filenames[org_name]
            table["rows"].append(
                {"data": [org_name, key_filename]}
            )
    _display_tables([table])


@app.command()
def ls(
    repro_tag: str = typer.Option(
        "", "--repro_tag", "-r",
        help="List information related to the dataset identified by '<REPRO_TAG>'."
    ),
    dataset_name: str = typer.Option(
        "", "--name", "-n",
        help="List information related to all datasets identified by '<DATASET_NAME>'."
    ),
    org_name: str = typer.Option(
        "", "--org", "-o",
        help="List information related to the datasets owned by '<ORG_NAME>'."
    ),
) -> None:
    info = {}
    if repro_tag != "":
        info["repro_tag"] = repro_tag
    if dataset_name != "":
        info["dataset_name"] = dataset_name
    if org_name != "":
        info["org_name"] = org_name

    response = api.ls(info=info)
    try:
        response_json = response.json()
    except JSONDecodeError as e:
        print("Unable to process response from Knap. Check that your API keys are valid.")
        print("JSON decode error: ", e)
        raise typer.Exit()

    if response_json and response_json.get("status", -1) == 0:
        if "tree" in response_json:
            _display_tree(response_json["tree"])
        elif "table" in response_json:
            _display_tables(response_json["table"])

    raise typer.Exit()


if __name__ == "__main__":
    app()
