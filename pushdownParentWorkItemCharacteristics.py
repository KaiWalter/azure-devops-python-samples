from azure.devops.connection import Connection
from azure.devops.credentials import BasicAuthentication
from azure.devops.v6_0.work_item_tracking.models import Wiql, JsonPatchOperation

import argparse
import datetime
import os
import pprint


def emit(msg, *args):
    print(msg % args)


def main():

    # extract arguments
    parser = argparse.ArgumentParser(
        description='push characteristics from parent work items to childs')
    parser.add_argument("-o", "--org", required=True, dest="url",
                        help="Azure DevOps Organization URL")
    parser.add_argument("-p", "--project", required=True, dest="project",
                        help="Azure DevOps Project")
    parser.add_argument("-t", "--pat", required=True, dest="pat",
                        help="Azure DevOps Personal Access Token")
    parser.add_argument("--age", required=False, dest="age", default=120, type=int,
                        help="age in days when last change of work item happened")
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
            AND [Source].[System.WorkItemType] = 'Bug'
            AND [Source].[System.ChangedDate] >= @today - {args.age}
            AND [System.Links.LinkType] = 'Child'
            MODE (MustContain)
        """
    )

    wi_relations = wit_client.query_by_wiql(wiql, top=1000).work_item_relations
    emit("Results: {0}".format(len(wi_relations)))

    # process relations
    if wi_relations:

        for wir in wi_relations:
            if wir.source and wir.target:

                # for each source (parent) / target (child) pair check field list
                print(f'{wir.source.id}->{wir.target.id}')

                wis = wit_client.get_work_item(wir.source.id)
                wit = wit_client.get_work_item(wir.target.id)

                fields_to_check = ['System.AreaPath', 'System.IterationPath']
                operations = []

                for field in fields_to_check:
                    if wis.fields[field] != wit.fields[field]:
                        print(f' =>{field}')
                        operations.append(JsonPatchOperation(
                            op='replace', path=f'/fields/{field}', value=wis.fields[field]))
                
                if len(operations) > 0:
                    resp = wit_client.update_work_item(document=operations, id=wir.target.id)                    
                    print(resp)


if __name__ == '__main__':
    main()
