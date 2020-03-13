from azure.devops.connection import Connection
from azure.devops.credentials import BasicAuthentication
from azure.devops.v6_0.work_item_tracking.models import Wiql, JsonPatchOperation

import argparse
import datetime
import os
import pprint


def main():

    # extract arguments
    parser = argparse.ArgumentParser(
        description='push characteristics from parent work items to children')
    parser.add_argument("-o", "--org", required=True, dest="url",
                        help="Azure DevOps Organization URL")
    parser.add_argument("-p", "--project", required=True, dest="project",
                        help="Azure DevOps Project")
    parser.add_argument("-t", "--pat", required=True, dest="pat",
                        help="Azure DevOps Personal Access Token")
    parser.add_argument("--parent-type", required=True, dest="parent_type", 
                        help="work item parent type to filter for (Bug,Feature,...)")
    parser.add_argument("--child-type", required=True, dest="child_type", 
                        help="work item child type to filter for (Task,Product Backlog Item,...)")
    parser.add_argument("--field-list", required=True, dest="field_list", 
                        help="comma separated list of field names to compare e.g. System.AreaPath,System.IterationPath")
    parser.add_argument("--age", required=False, dest="age", default=120, type=int,
                        help="age in days when last change of work item happened")
    parser.add_argument("--update", required=False, action='store_true',
                        dest="update", help="commit update to Azure DevOps")
    args = parser.parse_args()

    # create a connection to the org
    credentials = BasicAuthentication('', args.pat)
    connection = Connection(base_url=args.url, creds=credentials)

    # get a client
    wit_client = connection.clients.get_work_item_tracking_client()

    # query relations
    wiql = Wiql(
        query=f"""SELECT *
            FROM workitemLinks
            WHERE [Source].[System.TeamProject] = '{args.project}'
            AND [Source].[System.WorkItemType] = '{args.parent_type}'
            AND [Target].[System.WorkItemType] = '{args.child_type}'
            AND [Source].[System.ChangedDate] >= @today - {args.age}
            AND [System.Links.LinkType] = 'Child'
            MODE (MustContain)
        """
    )

    wi_relations = wit_client.query_by_wiql(wiql, top=1000).work_item_relations
    print(f'Results: {len(wi_relations)}')

    # process relations
    if wi_relations:

        fields_to_check = args.field_list.split(',')

        for wir in wi_relations:
            if wir.source and wir.target:

                # for each source (parent) / target (child) pair check field list
                wis = wit_client.get_work_item(wir.source.id)
                wit = wit_client.get_work_item(wir.target.id)

                print(f"{wis.fields['System.WorkItemType']} {wir.source.id} -> {wit.fields['System.WorkItemType']} {wir.target.id}")

                fields_to_check = args.field_list.split(',')
                operations = []

                for field in fields_to_check:
                    if wis.fields[field] != wit.fields[field]:
                        print(f' =>{field}')
                        operations.append(JsonPatchOperation(
                            op='replace', path=f'/fields/{field}', value=wis.fields[field]))
                
                if len(operations) > 0 and args.update:
                    resp = wit_client.update_work_item(document=operations, id=wir.target.id)                    
                    print(resp)


if __name__ == '__main__':
    main()
