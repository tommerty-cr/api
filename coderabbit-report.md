# CodeRabbit Changelog Generator

This GitHub Action automatically generates and updates a CHANGELOG.md file using CodeRabbit's AI-powered code analysis.

## Features

- 🤖 Automatically triggers on PR creation and updates
- 📝 Generates structured changelog entries from CodeRabbit analysis
- 🔄 Updates existing CHANGELOG.md or creates a new one
- 💬 Posts a confirmation comment on the PR
- 🎯 Can be manually triggered for specific PRs

## Setup

### 1. Get Your CodeRabbit API Key

1. Log in to [CodeRabbit](https://coderabbit.ai)
2. Navigate to Settings → API Keys
3. Generate a new API key

### 2. Add API Key to GitHub Secrets

1. Go to your repository settings
2. Navigate to **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `CODERABBIT_API_KEY`
5. Value: Your CodeRabbit API key
6. Click **Add secret**

### 3. Add the Workflow

1. Create `.github/workflows/` directory in your repository if it doesn't exist
2. Copy the workflow file to `.github/workflows/coderabbit-changelog.yml`
3. Commit and push

## Usage

### Automatic Trigger

The workflow runs automatically when:
- A new pull request is opened
- An existing pull request is updated (new commits)

### Manual Trigger

You can manually generate a changelog for any PR:

1. Go to **Actions** tab in your repository
2. Select **Generate Changelog from CodeRabbit** workflow
3. Click **Run workflow**
4. Enter the PR number
5. Click **Run workflow**

## Customization

### Change Report Type

The workflow requests a "changelog" report type. You can modify the report request to use different types:

```yaml
-d '{
  "repository": "${{ github.repository }}",
  "pull_number": ${{ steps.pr-number.outputs.pr_number }},
  "report_type": "summary",  # or "security", "performance", etc.
  "format": "markdown"
}'
```

### Custom Report Template

For more control, you can use custom reports with templates:

```yaml
- name: Request CodeRabbit Custom Report
  run: |
    curl -X POST https://api.coderabbit.ai/api/v1/reports/custom \
      -H "api-key: ${{ secrets.CODERABBIT_API_KEY }}" \
      -H "Content-Type: application/json" \
      -d '{
        "repository": "${{ github.repository }}",
        "pull_number": ${{ github.event.pull_request.number }},
        "template": "Your custom markdown template here with {{variables}}",
        "format": "markdown"
      }'
```

### Adjust Polling Settings

Modify the wait time and number of attempts:

```yaml
MAX_ATTEMPTS=30  # Maximum number of polling attempts
sleep 10         # Wait 10 seconds between attempts
```

### Change Changelog Format

Customize the changelog entry format in the "Create/Update CHANGELOG.md" step:

```yaml
echo "## PR #$PR_NUMBER - $PR_TITLE"
echo ""
echo "**Date:** $DATE"
echo "**Author:** @$PR_AUTHOR"
echo ""
echo "$CONTENT"
```

## Example Output

The generated CHANGELOG.md will look like:

```markdown
# Changelog

## PR #123 - Add user authentication feature

**Date:** 2025-01-15
**Author:** @username

### Changes
- Implemented JWT-based authentication
- Added login and registration endpoints
- Created user session management

### Security Improvements
- Password hashing with bcrypt
- Rate limiting on auth endpoints

---

## PR #122 - Fix database connection pool

**Date:** 2025-01-14
**Author:** @contributor

...
```

## Troubleshooting

### API Key Issues

If you see authentication errors:
- Verify `CODERABBIT_API_KEY` is correctly set in repository secrets
- Check that the API key hasn't expired
- Ensure the API key has the necessary permissions

### Timeout Issues

If the report generation times out:
- Increase `MAX_ATTEMPTS` in the workflow
- Increase the `sleep` duration between checks
- Check CodeRabbit's status page for API issues

### No Changes Detected

If the workflow runs but doesn't commit changes:
- Verify the report was generated successfully (check workflow logs)
- Ensure the report contains content
- Check git permissions and branch protection rules

## Permissions Required

The workflow needs these permissions:
- `contents: write` - To commit CHANGELOG.md
- `pull-requests: write` - To comment on PRs

These are set in the workflow file but may need adjustment based on your repository settings.

## Advanced: Using with Conventional Commits

You can enhance the changelog by parsing conventional commits:

```yaml
- name: Parse Conventional Commits
  run: |
    # Extract commit messages and categorize
    git log --format="%s" origin/main..HEAD | while read msg; do
      if [[ $msg =~ ^feat: ]]; then
        echo "### Features" >> /tmp/conventional.md
        echo "- ${msg#feat: }" >> /tmp/conventional.md
      elif [[ $msg =~ ^fix: ]]; then
        echo "### Bug Fixes" >> /tmp/conventional.md
        echo "- ${msg#fix: }" >> /tmp/conventional.md
      fi
    done
```

## License

This workflow is provided as-is for use with CodeRabbit's API. Refer to CodeRabbit's terms of service for API usage guidelines.
