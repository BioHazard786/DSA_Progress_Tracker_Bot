API = "https://leetcode.com/graphql"

USER_PROGRESS_QUERY = """
query userSessionProgress($username: String!) {
    allQuestionsCount {
        difficulty
        count
    }
    matchedUser(username: $username) {
        submitStats {
            acSubmissionNum {
                difficulty
                count
            }
        }
    }
}
"""

USER_PROFILE_QUERY = """
query getUserProfile($username: String!) {
    matchedUser(username: $username) {
        username
        profile {
            realName
        }
    }
}
"""
