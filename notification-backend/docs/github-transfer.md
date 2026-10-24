# GitHub Repository Transfer — Day 15

## Transfer to @ZethetaIntern

1. Open the GitHub repository.
2. Go to **Settings → General**.
3. Scroll to **Danger Zone**.
4. Select **Transfer ownership**.
5. Enter `ZethetaIntern` as the new owner.
6. Type the repository name to confirm.
7. Select **I understand, transfer this repository**.

## Alternative: Add as maintainer first

1. Go to **Settings → Collaborators and teams**.
2. Click **Add people**.
3. Enter `ZethetaIntern`.
4. Assign the **Maintain** role initially.
5. After validation, transfer ownership using the steps above.

## Post-transfer checklist

- Confirm `@ZethetaIntern` can access **Settings**.
- Update branch protection rules.
- Rotate deploy keys and personal access tokens.
- Update CI/CD secrets and environment protection rules.
- Update repository description and topics.
- Verify GitHub Actions permissions.
- Remove former owner's direct write access if no longer required.

## Recommended repository settings

| Setting | Value |
|---|---|
| Default branch | `main` |
| Visibility | Private |
| Merge method | Squash and merge |
| Branch protection | Require pull request and status checks |
| Required check | `test` |
| Actions permission | Read and write for deployment workflows |
| Secret scanning | Enabled |
| Dependabot | Enabled |
