import requests

def get_leetcode_problem_api(title_slug: str):
    url = "https://leetcode.com/graphql"
    
    query = """
    query getQuestionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        title
        content
      }
    }
    """
    
    variables = {"titleSlug": title_slug}
    
    response = requests.post(
        url, 
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        return data["data"]["question"]["content"] # Returns raw HTML content of the description
    else:
        return f"Failed with status code: {response.status_code}"

# Example usage for 'two-sum'
print(get_leetcode_problem_api("reverse-nodes-in-k-group"))