"""Github communication instance"""

from typing import List
import netrc
import requests

from .graphql_objects import PullRequest, Repository


def escape_characters_graphql(text: str) -> str:
    """Adds escapting characters to text to ensure that
    the graph-ql call is not invalid

    Args:
        text (str): The incoming text

    Returns:
        str: The adapted text
    """
    if not text:
        return text
    text = text.replace('"', r'\"')

    return text


class Github:
    """Instance communicating with Github"""

    def __init__(self, url: str = "https://api.github.com/graphql", token: str = ""):
        self.url = url

        if token:
            self.token = token
        else:
            self.token = netrc.netrc().authenticators(url)[2]

        self.session = requests.Session()
        self.session.headers = {
            "Authorization": f"token {self.token}",
            "Content-type": "application/json; charset=utf-8;",
            "Accept": "application/json;",
        }

    def _call(self, data: str):
        response = self.session.post(url=self.url, json={"query": data})
        return response.json()["data"]

    def query(self, querydata: str):
        """Call Github using a query

        Args:
            querydata (str): GraphQl Query

        Returns:
            dict: Json return object
        """
        return self._call(f"query {{{querydata}}}")

    def mutation(self, mutationdata):
        """Call Github using a query

        Args:
            mutationdata (str): GraphQl mutation

        Returns:
            dict: Json return object
        """
        return self._call(f"mutation {{{mutationdata}}}")

    def pull_request(self, owner: str, repo: str, number: int, querydata: str) -> PullRequest:
        """Queries Pull Request Information

        Args:
            owner (str): The owner of the repository
            repo (str): The repository name
            number (int): The pull request number
            query (str): The requested GraphQL query data

        Returns:
            PullRequest: The pull request object
        """
        res = self.query((
            f'repository(owner:"{owner}", name:"{repo}")'
            f'{{ pullRequest(number:{number}) {{ {querydata} }} }}'
        ))
        return PullRequest.parse_obj(res['repository']['pullRequest'])

    def search_pull_requests(self, search_query: str, querydata: str) -> List[PullRequest]:
        """Search Pull Requests on Github

        Args:
            search_query (str): The query to search for
            querydata (str): The pull request graphql query data

        Returns:
            List[PullRequest]: List of found pull requests
        """
        has_next_page = True
        end_cursor = None
        results = []

        while has_next_page:
            after_content = f'after:"{end_cursor}"' if end_cursor else ''
            res = self.query((
                'search('
                f'type: ISSUE, first: 100, query: "{search_query}",'
                f'{after_content}'
                '){'
                'issueCount '
                'pageInfo { endCursor hasNextPage } '
                f'nodes {{ ...on PullRequest {{ {querydata} }} }}'
                '}'
            ))

            total_count = res['search']['issueCount']
            assert total_count <= 1000, \
                (
                    f'Cannot retrieve more than 1000 pull request but "{total_count}" were found! '
                    'Please narrow down your search!'
                )

            results.extend(res['search']['nodes'])
            has_next_page = res['search']['pageInfo']['hasNextPage']
            end_cursor = res['search']['pageInfo']['endCursor']
        return list(map(PullRequest.parse_obj, results))

    def create_pull_request(  # pylint: disable=too-many-arguments
        self,
        repository_id: str,
        head_ref_name: str,
        base_ref_name: str,
        title: str,
        body: str = None,
        draft: bool = False,
        querydata: str = None
    ) -> PullRequest:
        """Creates a pull request in a repository

        Args:
            repository_id (str): Id of the repository
            head_ref_name (str): Name of the feature / bugfix / ... branch to be merged
            base_ref_name (str): Name of the branch being merged into
            title (str): Title of the pull request
            body (str, optional): Body of the pull request. Defaults to None.
            draft (bool, optional): Whether the pull request shall be created as draft.
                Defaults to false.
            querydata (str, optional): Data to be returend. Defaults to None.

        Returns:
            PullRequest: PullRequest object of the newly created pull request
        """
        title = escape_characters_graphql(title)
        body = escape_characters_graphql(body)

        body_content = f'body: "{body}",' if body else ''
        draft_content = f'draft: {draft},' if draft else ''
        query_data_content = f'pullRequest {{ {querydata} }}' if querydata else ''
        res = self.mutation((
            'createPullRequest(input: {'
            f'repositoryId: "{repository_id}",'
            f'headRefName: "{head_ref_name}",'
            f'baseRefName: "{base_ref_name}",'
            f'title: "{title}",'
            f'{body_content}'
            f'{draft_content}'
            '}){'
            'clientMutationId,'
            f'{query_data_content}'
            '}'
        ))

        if not querydata:
            return None

        if res['createPullRequest']['pullRequest']:
            return PullRequest.parse_obj(res['createPullRequest']['pullRequest'])

        return None

    def update_pull_request(
        self,
        pull_request_id: str,
        title: str = None,
        body: str = None,
        querydata: str = None,
    ) -> PullRequest:
        """Update Existing Pull Request

        Args:
            pull_request_id (str): The id of the pull request to be updated
            title (str, optional): If set update the title. Defaults to None.
            body (str, optional): If set update the body. Defaults to None.
            querydata (str, optional): Specify which data to be returned
                from the pull request. Defaults to None.

        Returns:
            PullRequest: _description_
        """
        title = escape_characters_graphql(title)
        body = escape_characters_graphql(body)

        body_content = f'body: "{body}",' if body else ''
        title_content = f'title: "{title}",' if title else ''
        query_data_content = f'pullRequest {{ {querydata} }}' if querydata else ''
        res = self.mutation((
            'updatePullRequest(input: {'
            f'pullRequestId: "{pull_request_id}",'
            f'{title_content}'
            f'{body_content}'
            '}){'
            'clientMutationId,'
            f'{query_data_content}'
            '}'
        ))

        if querydata:
            return PullRequest.parse_obj(res['updatePullRequest']['pullRequest'])

        return None

    # def add_pull_request_review(self, pull_request_id, event='APPROVE', body=''):
    #     raise NotImplementedError

    # def dismiss_pull_request_review(self, review_id, message):
    #     raise NotImplementedError

    def add_comment(self, subject_id: str, body: str):
        """Adds a comment to an issue or pull request

        Args:
            subject_id (str): The id of the issue or pull request
            body (str): The body of the comment (can be markdown)
        """
        self.mutation((
            f'addComment(input: {{body: "{body}", subjectId: "{subject_id}"}})'
            '{ clientMutationId }'
        ))

    # def get_file_content(self, owner, repo, ref, rel_file_path):
    #     raise NotImplementedError

    def get_repository(self, owner: str, repo: str, querydata: str):
        """Returns the repository object

        Args:
            owner (str): Name of the repository owner
            repo (str): Name of the repository
            querydata (str): Data to be queried from the repository (graph-ql)

        Returns:
            str: ID of the repository
        """
        res = self.query((
            f'repository(owner:"{owner}", name:"{repo}")'
            f'{{ {querydata} }}'
        ))
        return Repository.parse_obj(res['repository'])

    # def get_commit_date_for_sha(self, owner, repo, sha):
    #     # maybe instead use commits?! -> date -> get_commit_for_expression
    #     raise NotImplementedError

    # def get_first_sha_before_date(self, owner, repo, ref, commit_date_time):
    #     # instead use get_last_commit_before_date
    #     raise NotImplementedError

    # def all_label_to_labelable(self, labelable_id, label_ids):
    #     raise NotImplementedError

    # def remove_label_from_labelable(self, labelable_id, label_ids):
    #     raise NotImplementedError

    # def create_branch(self, owner, repo, base_oid, branch_name):
    #     raise NotImplementedError

    # def create_tag(self, owner, repo, base_oid, tag_name):
    #     raise NotImplementedError

    # def create_commit_on_branch(self, owner, repo, branch_name, head_sha, message_headline,
    # message_body, additions, deletions):
    #     raise NotImplementedError

    # def unsure___(self):
    #     # get_file_commit_history
    #     # get_file_pull_request_history
    #     # get_submodules
    #     raise NotImplementedError
