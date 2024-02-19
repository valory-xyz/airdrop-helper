olas_space_query = """
{
  space(id: "autonolas.eth") {
    id
    name
    about
    network
    symbol
    members
  }
}
"""

olas_proposals_query = """
query Proposals(
  $first: Int
  $skip: Int
  $state: String
  $space_in: [String]
) {
  proposals (
    first: $first,
    skip: $skip,
    where: {
      state: $state,
      space_in: $space_in
    }
  ) {
    id
    network
    title
    snapshot
    state
  }
}
"""

olas_votes_query = """
query Votes(
  $first: Int
  $skip: Int
  $space_in: [String]
) {
  votes (
    first: $first,
    skip: $skip,
    where: {
      space_in: $space_in
    }
    orderBy: "created"
    orderDirection: desc
  ) {
    id
    voter
    vp
    proposal {
      id
    }
    space {
      id
    }
  }
}
"""
